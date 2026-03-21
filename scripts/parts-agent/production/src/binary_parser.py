"""
Binary Parser — Reads PrtsPrcs binary files from Rossware ServiceDesk.

PrtsPrcs is a fixed-width binary file with 256-byte records containing
parts queue data. The record layout (discovered through hex analysis):

  Bytes 0-5:     Record header (binary ID)
  Bytes 6-21:    Status type (16 bytes): "Ship if I/SMA", "CORE", "P&A Only", etc.
  Bytes 22-31:   Binary date/float data (not decoded)
  Bytes 32-39:   Padding (typically "@" + spaces)
  Bytes 40-64:   PART NUMBER + STATUS CODE (the real manufacturer part number
                 is here, spanning these bytes, followed by EXCR/status suffixes)
  Bytes 64-96:   Binary data (pricing/dates)
  Bytes 96-112:  Phone number (with binary prefix)
  Bytes 112-176: Notes/comments (64 bytes, with binary prefix)
  Bytes 176-192: Vendor action code (16 bytes): "RtToVndr", "MvdToStk", etc.
  Bytes 192-256: Batch/date reference code (64 bytes): "91420-2", "91620-1", etc.
"""

import csv
import re
from datetime import datetime
from pathlib import Path


class BinaryParser:
    """Parses PrtsPrcs binary files into structured parts data."""

    RECORD_SIZE = 256

    # Known status code suffixes that appear after the part number
    # These get stripped when extracting the clean part number
    STATUS_SUFFIXES = re.compile(
        r'(EXCR|RETURN|APPROVED|SUBMITTE|SUBMITTED|SUBMIT|PENDING|'
        r'approv|return|submit|pending|CANCELED|COMPLETE|RECEIVED|'
        r'received|canceled|complete)\b.*$',
        re.IGNORECASE
    )

    def __init__(self, log_fn):
        self.log = log_fn

    def parse_file(self, filepath, filter_active=True):
        """Parse a PrtsPrcs binary file and return parts records.

        Args:
            filepath: Path to the PrtsPrcs binary file.
            filter_active: If True, only return records that need pricing.

        Returns:
            list of dicts with keys: part_number, work_order, status_type,
            approval_status, vendor_action, notes, phone, batch_ref
        """
        filepath = Path(filepath)
        if not filepath.exists():
            self.log(f"PrtsPrcs file not found: {filepath}")
            return []

        data = filepath.read_bytes()
        total_size = len(data)
        num_records = total_size // self.RECORD_SIZE

        if total_size % self.RECORD_SIZE != 0:
            self.log(
                f"WARNING: File size {total_size} is not evenly divisible "
                f"by record size {self.RECORD_SIZE}. "
                f"Truncating to {num_records} complete records."
            )

        self.log(f"Parsing PrtsPrcs: {total_size:,} bytes, {num_records} records")

        all_records = []
        for i in range(num_records):
            offset = i * self.RECORD_SIZE
            rec = data[offset:offset + self.RECORD_SIZE]
            record = self._parse_record(rec, i)
            if record:
                all_records.append(record)

        self.log(f"Parsed {len(all_records)} valid records from {num_records} total")

        if filter_active:
            active = self._filter_active_parts(all_records)
            self.log(f"Active parts needing pricing: {len(active)}")
            return active

        return all_records

    def get_unique_part_numbers(self, records):
        """Extract unique, non-empty part numbers from parsed records.

        Returns:
            tuple of (unique_parts_list, parts_to_records_map)
        """
        seen = set()
        unique = []
        parts_map = {}

        for rec in records:
            pn = rec["part_number"]
            if not pn:
                continue

            if pn not in seen:
                seen.add(pn)
                unique.append(pn)
                parts_map[pn] = []

            parts_map[pn].append(rec)

        self.log(f"Unique part numbers to look up: {len(unique)}")
        return unique, parts_map

    def save_parsed_csv(self, records, output_path):
        """Save parsed records to CSV for debugging/auditing."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "part_number", "status_type", "approval_status",
            "vendor_action", "notes", "phone", "batch_ref"
        ]

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        self.log(f"Parsed records saved to: {output_path}")

    def _parse_record(self, rec, index):
        """Parse a single 256-byte record into a dict."""

        # Status type: bytes 6-22
        status_type = self._decode_field(rec, 6, 22)

        # Part number: bytes 40-64 (spans two original fields)
        # The part number sits after 8 bytes of "@" padding at bytes 32-39
        raw_pn_area = self._decode_field(rec, 40, 64)

        # Extract the clean part number by stripping status suffixes
        part_number, approval_status = self._extract_part_number(raw_pn_area)

        # Phone: bytes 96-112 (has binary prefix, extract digits)
        phone_raw = self._decode_field(rec, 96, 112)
        phone = self._extract_phone(phone_raw)

        # Notes: bytes 112-176 (has binary prefix, extract readable text)
        notes_raw = self._decode_field(rec, 112, 176)
        notes = self._extract_readable_text(notes_raw)

        # Vendor action: bytes 176-192
        vendor_action = self._decode_field(rec, 176, 192)

        # Batch reference: bytes 192-256 (the date-like codes)
        batch_ref = self._decode_field(rec, 192, 256)

        # Skip completely empty records
        if not part_number and not status_type:
            return None

        return {
            "part_number": part_number,
            "status_type": status_type,
            "approval_status": approval_status,
            "vendor_action": vendor_action,
            "notes": notes,
            "phone": phone,
            "batch_ref": batch_ref,
        }

    def _decode_field(self, rec, start, end):
        """Decode a byte range as ASCII, stripping garbage."""
        raw = rec[start:end]
        try:
            text = raw.decode("ascii", errors="replace")
            # Remove null bytes and replacement characters
            text = text.replace("\x00", "").replace("\ufffd", "")
            return text.strip()
        except Exception:
            return ""

    def _extract_part_number(self, raw_text):
        """Extract a clean part number from the combined part+status field.

        The raw text looks like:
            "W11171748EXCR   APPROVED"
            "EBR76261816"
            "WPW10624574EXCR SUBMITTE"
            "W10812421       approved"
            "242058232"
            "W11419215       emailed"
            "WB27X39968      GET CRED"

        Strategy:
        1. Strip known status code suffixes (EXCR, APPROVED, etc.)
        2. Take only the first whitespace-delimited token as the part number
           (anything after spaces is status notes, not part of the PN)

        Returns:
            tuple of (part_number, approval_status)
        """
        if not raw_text:
            return "", ""

        # First pass: strip known status suffixes that may be concatenated
        # directly to the part number (e.g. "WPW10624574EXCR")
        match = self.STATUS_SUFFIXES.search(raw_text)
        if match:
            cleaned = raw_text[:match.start()].strip()
            approval_status = raw_text[match.start():].strip()
        else:
            cleaned = raw_text.strip()
            approval_status = ""

        # Second pass: take only the first token (split on whitespace)
        # Anything after spaces is status notes, not the part number
        tokens = cleaned.split()
        if tokens:
            part_number = tokens[0]
            # If there were extra tokens, they're part of the status
            if len(tokens) > 1:
                extra = " ".join(tokens[1:])
                approval_status = (extra + " " + approval_status).strip()
        else:
            part_number = ""

        # Clean up: remove non-printable chars
        part_number = re.sub(r'[^\x20-\x7E]', '', part_number).strip()

        # Validate: part number should be at least 4 chars and contain
        # at least one digit to be a real manufacturer part number
        if len(part_number) < 4 or not re.search(r'\d', part_number):
            return "", approval_status

        return part_number, approval_status

    def _extract_phone(self, raw_text):
        """Extract a phone number from a field that may have binary prefix."""
        digits = re.findall(r'\d', raw_text)
        phone = "".join(digits)
        if len(phone) >= 7:
            return phone
        return ""

    def _extract_readable_text(self, raw_text):
        """Extract readable ASCII text from a field with binary prefix."""
        # Find the longest run of printable ASCII
        readable = re.findall(r'[\x20-\x7E]{3,}', raw_text)
        if readable:
            # Join all readable segments and clean up
            text = " ".join(readable).strip()
            # Remove known garbage prefixes
            text = re.sub(r'^[^A-Za-z0-9]*', '', text)
            return text
        return ""

    def _filter_active_parts(self, records):
        """Filter to records that likely need pricing lookup.

        Keeps records where:
        - part_number is non-empty
        - approval_status is not RETURN
        - vendor_action is not a terminal state
        - status_type is not CORE (core returns)
        """
        active = []
        skipped_reasons = {"no_pn": 0, "return": 0, "core": 0, "terminal": 0}

        for rec in records:
            pn = rec["part_number"]
            if not pn:
                skipped_reasons["no_pn"] += 1
                continue

            # Skip CORE records (these are core returns, not parts needing pricing)
            status = rec.get("status_type", "")
            if "CORE" in status.upper():
                skipped_reasons["core"] += 1
                continue

            # Skip explicit RETURN approval status
            approval = rec.get("approval_status", "")
            if "RETURN" in approval.upper():
                skipped_reasons["return"] += 1
                continue

            # Skip terminal vendor actions
            action = rec.get("vendor_action", "")
            if action in ("RtToVndr", "MvdToStk", "Cancelled", "CrdtRcvd"):
                skipped_reasons["terminal"] += 1
                continue

            active.append(rec)

        self.log(
            f"Filtering: {skipped_reasons['no_pn']} empty, "
            f"{skipped_reasons['core']} core returns, "
            f"{skipped_reasons['return']} returned, "
            f"{skipped_reasons['terminal']} terminal actions"
        )
        return active
