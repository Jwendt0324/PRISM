"""
CSV Handler — Input reading, output writing, archiving, and deduplication.

Handles flexible input formats, writes ServiceDesk-compatible output,
archives processed files, and deduplicates part numbers.
"""

import csv
import shutil
from datetime import datetime
from pathlib import Path


class CSVHandler:
    """Reads input CSVs, writes results, archives processed files."""

    # Columns we look for in input files (case-insensitive matching)
    KNOWN_COLUMNS = {
        "part_number", "description", "vendor", "job_number", "status",
        "model_number", "model"
    }

    # Output columns in ServiceDesk-compatible format
    OUTPUT_COLUMNS = [
        "part_number",
        "marcone_part_number",
        "marcone_name",
        "wholesale_price",
        "availability",
        "vendor",
        "lookup_timestamp",
        "status",
        "original_description",
        "original_job_number",
        "original_model_number",
        "warehouse_location",
        "quality_return",
        "model_recommendation",
        "alternate_vendors",
    ]

    def __init__(self, log_fn, project_root, vendor_code="MC"):
        """
        Args:
            log_fn: callable for logging
            project_root: Path to parts-agent/
            vendor_code: distributor code for output (e.g. "MC" for Marcone)
        """
        self.log = log_fn
        self.project_root = Path(project_root)
        self.input_dir = self.project_root / "data" / "input"
        self.output_dir = self.project_root / "data" / "output"
        self.archive_dir = self.project_root / "data" / "archive"
        self.vendor_code = vendor_code

    def scan_input_files(self):
        """Find all CSV files in data/input/.

        Returns:
            list of Path objects for each CSV file found.
        """
        files = sorted(self.input_dir.glob("*.csv"))
        if files:
            self.log(f"Found {len(files)} input file(s): {', '.join(f.name for f in files)}")
        return files

    def load_parts(self, input_files):
        """Load part numbers from one or more input CSVs.

        Auto-detects column names. Minimum requirement: a column whose
        name contains 'part' (case-insensitive).

        Args:
            input_files: list of Path objects.

        Returns:
            tuple of (unique_parts, all_rows)
            - unique_parts: list of unique part number strings (preserving order)
            - all_rows: list of dicts with all input data per row
        """
        all_rows = []
        seen_parts = set()
        unique_parts = []

        for filepath in input_files:
            self.log(f"Reading {filepath.name}...")
            with open(filepath, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                # Find the part number column (flexible matching)
                part_col = self._find_part_column(reader.fieldnames)
                if not part_col:
                    self.log(f"  WARNING: No 'part_number' column found in {filepath.name}. Skipping.")
                    continue

                desc_col = self._find_column(reader.fieldnames, "description", "desc")
                job_col = self._find_column(reader.fieldnames, "job_number", "job", "wo")
                model_col = self._find_column(reader.fieldnames, "model_number", "model")

                row_count = 0
                for row in reader:
                    part_number = row.get(part_col, "").strip()
                    if not part_number:
                        continue

                    row_data = {
                        "part_number": part_number,
                        "original_description": row.get(desc_col, "").strip() if desc_col else "",
                        "original_job_number": row.get(job_col, "").strip() if job_col else "",
                        "original_model_number": row.get(model_col, "").strip() if model_col else "",
                        "source_file": filepath.name,
                    }
                    all_rows.append(row_data)
                    row_count += 1

                    if part_number not in seen_parts:
                        seen_parts.add(part_number)
                        unique_parts.append(part_number)

                self.log(f"  Loaded {row_count} rows, {len(seen_parts)} unique parts so far.")

        duplicates = len(all_rows) - len(unique_parts)
        if duplicates > 0:
            self.log(f"Deduplication: {duplicates} duplicate part numbers will be looked up once.")

        self.log(f"Total: {len(all_rows)} rows, {len(unique_parts)} unique parts to look up.")
        return unique_parts, all_rows

    def init_output(self):
        """Create a new timestamped output CSV and return its path.

        Returns:
            Path to the output CSV file.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"results_{timestamp}.csv"

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.OUTPUT_COLUMNS)
            writer.writeheader()

        self.log(f"Output file created: {output_path.name}")
        return output_path

    def write_results(self, output_path, all_rows, results_by_part):
        """Write all results to the output CSV.

        Each input row gets its own output row. Duplicate part numbers
        share the same lookup result.

        Args:
            output_path: Path to the output CSV.
            all_rows: list of input row dicts.
            results_by_part: dict mapping part_number -> result dict.
        """
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.OUTPUT_COLUMNS)
            writer.writeheader()

            for row in all_rows:
                part = row["part_number"]
                result = results_by_part.get(part, {})

                enrichment = result.get("netdata", {})
                qr = enrichment.get("quality_return", False)
                writer.writerow({
                    "part_number": part,
                    "marcone_part_number": result.get("marcone_part_number", ""),
                    "marcone_name": result.get("marcone_name", ""),
                    "wholesale_price": result.get("price", ""),
                    "availability": result.get("availability", ""),
                    "vendor": self.vendor_code,
                    "lookup_timestamp": result.get("lookup_timestamp", ""),
                    "status": result.get("status", "NOT PROCESSED"),
                    "original_description": row.get("original_description", ""),
                    "original_job_number": row.get("original_job_number", ""),
                    "original_model_number": row.get("original_model_number", ""),
                    "warehouse_location": enrichment.get("warehouse_location", ""),
                    "quality_return": "YES" if qr else "",
                    "model_recommendation": enrichment.get("model_recommendation", ""),
                    "alternate_vendors": enrichment.get("alternate_vendors", ""),
                })

        self.log(f"Results written: {output_path.name} ({len(all_rows)} rows)")

    def archive_inputs(self, input_files):
        """Move processed input files to data/archive/ with timestamp suffix."""
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for filepath in input_files:
            archive_name = f"{filepath.stem}_{timestamp}{filepath.suffix}"
            dest = self.archive_dir / archive_name
            shutil.move(str(filepath), str(dest))
            self.log(f"Archived: {filepath.name} -> archive/{archive_name}")

    def print_summary(self, results_by_part, elapsed_seconds):
        """Print a human-readable summary of the run."""
        total = len(results_by_part)
        found = sum(1 for r in results_by_part.values() if r.get("status") == "FOUND")
        not_found = sum(1 for r in results_by_part.values() if r.get("status") == "NOT FOUND")
        errors = sum(1 for r in results_by_part.values() if "ERROR" in r.get("status", ""))

        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)
        avg = elapsed_seconds / total if total > 0 else 0

        self.log("=" * 60)
        self.log("RUN SUMMARY")
        self.log(f"  Total parts looked up:  {total}")
        self.log(f"  Found with pricing:     {found}")
        self.log(f"  Not found:              {not_found}")
        self.log(f"  Errors:                 {errors}")
        self.log(f"  Time elapsed:           {minutes}m {seconds}s")
        self.log(f"  Average per part:       {avg:.1f}s")
        self.log("=" * 60)

    # --- Private helpers ---

    def _find_part_column(self, fieldnames):
        """Find the column that contains part numbers."""
        if not fieldnames:
            return None
        for name in fieldnames:
            if "part" in name.lower() and "number" in name.lower():
                return name
        for name in fieldnames:
            if "part" in name.lower():
                return name
        return None

    def _find_column(self, fieldnames, *keywords):
        """Find a column by keyword matching."""
        if not fieldnames:
            return None
        for name in fieldnames:
            lower = name.lower()
            for kw in keywords:
                if kw in lower:
                    return name
        return None
