#!/usr/bin/env python3
"""
scheduler.py — Main scheduling engine that ties parser + optimizer + metrics.
"""

import csv
import json
from pathlib import Path

from parser import run_all as parse_all
from optimizer import optimize_schedule, load_techs
from metrics import compute_comparison, save_metrics, print_summary

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "output"


def save_optimized_schedule(optimized_routes):
    """Write optimized schedule to CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dst = OUTPUT_DIR / "optimized_schedule.csv"

    rows = []
    for code, data in optimized_routes.items():
        tech = data["tech"]
        for stop in data["stats"].get("stops", []):
            rows.append({
                "tech_code": code,
                "tech_name": tech["name"],
                "stop_order": stop.get("day_stop", 1),
                "customer": stop["customer"],
                "zip_code": stop["zip_code"],
                "date": stop.get("date", ""),
                "day": stop.get("day", ""),
                "time_window": stop.get("time_window", ""),
                "lat": round(stop["lat"], 4),
                "lon": round(stop["lon"], 4),
                "arrive_time_min": round(stop["arrive_time"], 0),
                "arrive_time_display": _min_to_time(stop["arrive_time"]),
                "leg_miles": stop["leg_miles"],
                "leg_minutes": stop["leg_minutes"],
            })

    with open(dst, "w", newline="") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)

    print(f"  Optimized schedule: {len(rows)} stops → {dst}")
    return rows


def _min_to_time(minutes):
    """Convert minutes-since-midnight to readable time."""
    h = int(minutes // 60)
    m = int(minutes % 60)
    period = "AM" if h < 12 else "PM"
    display_h = h if h <= 12 else h - 12
    if display_h == 0:
        display_h = 12
    return f"{display_h}:{m:02d} {period}"


def run_full_pipeline():
    """Execute full parse → optimize → metrics pipeline."""
    print("=" * 60)
    print("  D3S SERVICE SCHEDULING AGENT")
    print("=" * 60)
    print()

    # Step 1: Parse
    print("[1/4] Parsing raw ServiceDesk data...")
    parse_all()
    print()

    # Step 2: Load and optimize
    print("[2/4] Running route optimization...")
    original_routes, optimized_routes, techs = optimize_schedule()
    print(f"  Processed {sum(r['stats']['jobs'] for r in original_routes.values())} jobs "
          f"across {len(original_routes)} techs")
    print()

    # Step 3: Save optimized schedule
    print("[3/4] Saving optimized schedule...")
    save_optimized_schedule(optimized_routes)
    print()

    # Step 4: Compute and save metrics
    print("[4/4] Computing metrics...")
    comparison = compute_comparison(original_routes, optimized_routes, techs)
    save_metrics(comparison)
    print_summary(comparison)

    return comparison


if __name__ == "__main__":
    run_full_pipeline()
