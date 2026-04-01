#!/usr/bin/env python3
"""
parser.py — Reads ServiceDesk file formats into clean CSVs.
Handles: TechList.txt, ZoneList.txt, WhchTechToWhchZone.CSV,
         SchdList (binary), PrtsPrcs (binary), JobTracker.MDB
Output goes to data/parsed/
"""

import csv
import os
import struct
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PARSED_DIR = BASE_DIR / "data" / "parsed"


def parse_techlist():
    """TechList.txt → techs.csv"""
    src = RAW_DIR / "TechList.txt"
    dst = PARSED_DIR / "techs.csv"
    rows = []
    with open(src, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            rows.append({
                "name": r.get("TechName", "").strip(),
                "short_name": r.get("ShortName", "").strip(),
                "code": r.get("TwoLttrCd", "").strip(),
                "phone": r.get("TelNmbr", "").strip(),
                "email": r.get("EmailAddress", "").strip(),
                "address": f'{r.get("AddrsLn1", "").strip()}, {r.get("AddrsLn2", "").strip()}',
                "lat": r.get("Latitude", "").strip(),
                "lon": r.get("Longitude", "").strip(),
                "capacity": r.get("JobCapacity", "").strip(),
                "avg_minutes": r.get("AvgMnsOnJb", "").strip(),
                "target_miles": r.get("TargetMiles", "").strip(),
                "start_node": r.get("StartNode", "").strip(),
                "end_node": r.get("EndNode", "").strip(),
                "truck_number": r.get("TruckNumber", "").strip(),
                "is_fake": r.get("IsTechFake", "").strip(),
                "tech_id": r.get("TechID", "").strip(),
                "focus_group": r.get("FocusGroup", "").strip(),
                "using_sdm": r.get("UsingSdm?", "").strip(),
                "vector_style": r.get("VectorStyle", "").strip(),
            })
    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"  techs.csv: {len(rows)} technicians")
    return rows


def parse_zonelist():
    """ZoneList.txt → zones.csv"""
    src = RAW_DIR / "ZoneList.txt"
    dst = PARSED_DIR / "zones.csv"
    rows = []
    with open(src, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                rows.append({"zip_code": parts[0].strip(), "zone": parts[1].strip()})
    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["zip_code", "zone"])
        w.writeheader()
        w.writerows(rows)
    print(f"  zones.csv: {len(rows)} zip-to-zone mappings")
    return rows


def parse_tech_zones():
    """WhchTechToWhchZone.CSV → tech_zones.csv"""
    src = RAW_DIR / "WhchTechToWhchZone.CSV"
    dst = PARSED_DIR / "tech_zones.csv"
    rows = []
    with open(src, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) >= 2:
                zone = r[0].strip()
                techs = r[1].strip()
                rows.append({"zone": zone, "tech_codes": techs})
    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["zone", "tech_codes"])
        w.writeheader()
        w.writerows(rows)
    print(f"  tech_zones.csv: {len(rows)} zone assignments")
    return rows


def parse_schdlist():
    """SchdList binary (96-byte fixed records) → schedule.csv"""
    src = RAW_DIR / "SchdList"
    dst = PARSED_DIR / "schedule.csv"
    if not src.exists():
        print("  SchdList not found, skipping")
        return []

    data = src.read_bytes()
    record_size = 96
    num_records = len(data) // record_size
    rows = []

    for i in range(num_records):
        rec = data[i * record_size:(i + 1) * record_size]

        record_id = struct.unpack("<I", rec[0:4])[0]
        customer = rec[4:16].decode("ascii", errors="replace").strip()
        zip_code = rec[16:28].decode("ascii", errors="replace").strip()
        city_abbr = rec[28:31].decode("ascii", errors="replace").strip()
        date_time_raw = rec[31:47].decode("ascii", errors="replace").strip()
        # Tech code is at bytes 47-48, route info from 49 onward
        tech_code = rec[47:49].decode("ascii", errors="replace").strip().upper()
        tech_route = rec[49:62].decode("ascii", errors="replace").strip()

        # Parse date/time: "3/23 MON 8-12" or "3/27 FRI 8-1"
        date_str = ""
        day_of_week = ""
        time_window = ""
        dt_parts = date_time_raw.split()
        if len(dt_parts) >= 1:
            date_str = dt_parts[0]
        if len(dt_parts) >= 2:
            day_of_week = dt_parts[1]
        if len(dt_parts) >= 3:
            time_window = dt_parts[2]

        # Date stamp near end of record
        date_stamp = ""
        tail = rec[78:90].decode("ascii", errors="replace")
        digits = "".join(c for c in tail if c.isdigit())
        if len(digits) >= 6:
            date_stamp = digits[:6]

        rows.append({
            "record_id": record_id,
            "customer": customer,
            "zip_code": zip_code,
            "city": city_abbr,
            "date": date_str,
            "day": day_of_week,
            "time_window": time_window,
            "tech_code": tech_code,
            "route_info": tech_route,
            "date_stamp": date_stamp,
        })

    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        w.writeheader()
        w.writerows(rows)
    print(f"  schedule.csv: {len(rows)} scheduled jobs")
    return rows


def parse_prtsprcs():
    """PrtsPrcs binary (256-byte fixed records) → parts_queue.csv"""
    src = RAW_DIR / "PrtsPrcs"
    dst = PARSED_DIR / "parts_queue.csv"
    if not src.exists():
        print("  PrtsPrcs not found, skipping")
        return []

    data = src.read_bytes()
    record_size = 256
    num_records = len(data) // record_size
    rows = []

    for i in range(num_records):
        rec = data[i * record_size:(i + 1) * record_size]

        status_type = rec[6:22].decode("ascii", errors="replace").strip()
        work_order = rec[32:48].decode("ascii", errors="replace").strip()
        approval = rec[48:62].decode("ascii", errors="replace").strip()
        phone = rec[96:112].decode("ascii", errors="replace").strip()
        notes = rec[112:176].decode("ascii", errors="replace").strip()
        vendor_action = rec[176:192].decode("ascii", errors="replace").strip()
        part_number = rec[192:256].decode("ascii", errors="replace").strip()

        phone_digits = "".join(c for c in phone if c.isdigit())
        if len(phone_digits) < 7:
            phone = ""

        rows.append({
            "status_type": status_type,
            "work_order": work_order,
            "approval_status": approval,
            "phone": phone,
            "notes": notes,
            "vendor_action": vendor_action,
            "part_number": part_number,
        })

    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        w.writeheader()
        w.writerows(rows)
    print(f"  parts_queue.csv: {len(rows)} parts records")
    return rows


def parse_jobtracker():
    """JobTracker.MDB → jobs.csv using mdb-export"""
    src = RAW_DIR / "JobTracker.MDB"
    dst = PARSED_DIR / "jobs.csv"
    if not src.exists():
        print("  JobTracker.MDB not found, skipping")
        return 0

    try:
        result = subprocess.run(
            ["mdb-export", str(src), "Items"],
            capture_output=True, text=True, timeout=120,
            env={**os.environ, "MDB_JET3_CHARSET": "cp1252"}
        )
        if result.returncode != 0:
            print(f"  JobTracker.MDB: mdb-export failed: {result.stderr[:200]}")
            return 0

        dst.write_text(result.stdout)
        line_count = result.stdout.count("\n") - 1
        print(f"  jobs.csv: {line_count} job records")

        _extract_recent_jobs(result.stdout)
        return line_count

    except FileNotFoundError:
        print("  mdb-export not found. Install: brew install mdbtools")
        return 0
    except subprocess.TimeoutExpired:
        print("  JobTracker.MDB: export timed out")
        return 0


def _extract_recent_jobs(csv_text):
    """Extract recent jobs with addresses for scheduling."""
    import io
    dst = PARSED_DIR / "recent_jobs.csv"
    reader = csv.DictReader(io.StringIO(csv_text))

    rows = []
    for r in reader:
        rows.append({
            "item_id": r.get("ItemID", "").strip(),
            "po_number": r.get("PoNmbr", "").strip(),
            "hvac_abbrev": r.get("HvcAbbrv", "").strip(),
            "invoice": r.get("InvNmbr", "").strip(),
            "address": r.get("Address", "").strip(),
            "phone": r.get("Phone", "").strip(),
            "email": r.get("Email", "").strip(),
            "date_created": r.get("DtCrtd", "").strip(),
        })

    recent = rows[-5000:] if len(rows) > 5000 else rows
    with open(dst, "w", newline="") as f:
        if recent:
            w = csv.DictWriter(f, fieldnames=recent[0].keys())
            w.writeheader()
            w.writerows(recent)
    print(f"  recent_jobs.csv: {len(recent)} recent jobs extracted")


def run_all():
    """Parse all available data files."""
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    print("Parsing ServiceDesk data files...")
    print()

    techs = parse_techlist()
    zones = parse_zonelist()
    tech_zones = parse_tech_zones()
    schedule = parse_schdlist()
    parts = parse_prtsprcs()
    jobs_count = parse_jobtracker()

    print()
    print(f"All parsed CSVs written to {PARSED_DIR}/")
    return {
        "techs": techs,
        "zones": zones,
        "tech_zones": tech_zones,
        "schedule": schedule,
        "parts": parts,
        "jobs_count": jobs_count,
    }


if __name__ == "__main__":
    run_all()
