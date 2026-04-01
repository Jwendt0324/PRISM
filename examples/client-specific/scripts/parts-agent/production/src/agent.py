"""
Production Agent — Main orchestrator for [Client — Appliance Repair] parts pricing.

Reads PrtsPrcs binary file → looks up parts on [Parts Distributor] → saves results
to CSV + JSON → serves dashboard on port 8050.
"""

import csv
import json
import time
from datetime import datetime
from pathlib import Path

from .binary_parser import BinaryParser
from .session_manager import SessionManager
from .scraper import Scraper
from .rate_limiter import RateLimiter, RunAborted
from .resume_engine import ResumeEngine


class ProductionAgent:
    """Orchestrates the full PrtsPrcs → [Parts Distributor] lookup pipeline."""

    # Output columns
    OUTPUT_COLUMNS = [
        "part_number",
        "marcone_part_number",
        "marcone_name",
        "wholesale_price",
        "availability",
        "vendor",
        "lookup_timestamp",
        "status",
        "batch_ref",
        "approval_status",
        "vendor_action",
        "notes",
    ]

    def __init__(self, project_root, prtsprcs_path=None, headless=None,
                 auto_resume=False, dry_run=False, test_limit=None):
        """
        Args:
            project_root: Path to the production/ directory.
            prtsprcs_path: Path to PrtsPrcs binary file (overrides config).
            headless: override headless setting (None = use config).
            auto_resume: if True, auto-resume incomplete runs.
            dry_run: if True, show what would be processed but don't run.
            test_limit: if set, only process this many parts.
        """
        self.project_root = Path(project_root)
        self.auto_resume = auto_resume
        self.dry_run = dry_run
        self.test_limit = test_limit

        # Set up logging
        self.logs_dir = self.project_root / "logs" / "runs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.error_log_dir = self.project_root / "logs" / "errors"
        self.error_log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_log_path = self.logs_dir / f"run_{timestamp}.log"
        self._log_file = open(self.run_log_path, "a")

        # Load configs
        self.config = self._load_json(self.project_root / "config" / "config.json")
        if headless is not None:
            self.config["headless"] = headless

        distributor_name = self.config.get("distributor", "distributor")
        self.distributor = self._load_json(
            self.project_root / "config" / "distributors" / f"{distributor_name}.json"
        )

        # Resolve PrtsPrcs path
        if prtsprcs_path:
            self.prtsprcs_path = Path(prtsprcs_path)
        elif self.config.get("prtsprcs_path"):
            self.prtsprcs_path = Path(self.config["prtsprcs_path"])
        else:
            # Default: look in data/input/
            self.prtsprcs_path = self.project_root / "data" / "input" / "PrtsPrcs"

        # Initialize modules
        self.parser = BinaryParser(self.log)
        self.rate_limiter = RateLimiter(self.config, self.log)
        self.resume_engine = ResumeEngine(
            self.log, self.project_root / "data" / "output"
        )
        self.scraper = Scraper(self.distributor, self.log)
        self.session_manager = SessionManager(
            self.config, self.distributor, self.log, self.project_root
        )

        # Output directories
        self.output_dir = self.project_root / "data" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        """Execute the full pipeline: parse → lookup → save → dashboard."""
        start_time = time.time()

        self.log("=" * 60)
        self.log("[Client — Appliance Repair] PARTS PRICING AGENT — PRODUCTION")
        self.log(f"Distributor: {self.distributor['name']}")
        self.log(f"PrtsPrcs: {self.prtsprcs_path}")
        self.log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.test_limit:
            self.log(f"TEST MODE: Limited to {self.test_limit} parts")
        self.log("=" * 60)

        try:
            # Step 1: Parse PrtsPrcs binary file
            self.log("")
            self.log("STEP 1: Parsing PrtsPrcs binary file...")
            records = self.parser.parse_file(self.prtsprcs_path, filter_active=True)

            if not records:
                self.log("No active parts found in PrtsPrcs. Nothing to do.")
                return

            # Save parsed records for auditing
            parsed_csv = self.output_dir / "parsed_parts_queue.csv"
            self.parser.save_parsed_csv(records, parsed_csv)

            # Step 2: Extract unique part numbers
            unique_parts, parts_map = self.parser.get_unique_part_numbers(records)

            if not unique_parts:
                self.log("No part numbers found to look up. Nothing to do.")
                return

            # Apply test limit
            if self.test_limit and self.test_limit < len(unique_parts):
                self.log(f"Test mode: trimming from {len(unique_parts)} to {self.test_limit} parts")
                unique_parts = unique_parts[:self.test_limit]

            # Step 3: Check for incomplete previous run
            self.log("")
            self.log("STEP 2: Checking for previous incomplete runs...")
            resumed = self.resume_engine.check_for_incomplete_run(self.auto_resume)
            if resumed:
                remaining = self.resume_engine.get_remaining_parts()
                self.log(f"Resuming: {len(remaining)} parts remaining.")
            else:
                self.resume_engine.start_new_run(unique_parts, str(self.prtsprcs_path))
                remaining = unique_parts

            # Estimate time
            est_seconds = len(remaining) * (self.config.get("[google-doc-id]", 2) + 5)
            est_minutes = est_seconds / 60
            self.log(f"Parts to process: {len(remaining)} (estimated {est_minutes:.0f} minutes)")
            self.log("-" * 60)

            # Dry run — stop here
            if self.dry_run:
                self.log("DRY RUN — would process these parts:")
                for i, p in enumerate(remaining, 1):
                    ref_list = [r["batch_ref"] for r in parts_map.get(p, []) if r.get("batch_ref")]
                    ref_str = f" (Ref: {', '.join(set(ref_list))})" if ref_list else ""
                    self.log(f"  {i}. {p}{ref_str}")
                self.log("Exiting dry run.")
                return

            # Step 4: Get authenticated browser session
            self.log("")
            self.log("STEP 3: Logging into [Parts Distributor]...")
            page = self.session_manager.get_authenticated_page()

            # Step 5: Process each part
            self.log("")
            self.log("STEP 4: Looking up parts...")
            results_by_part = {}
            completed_parts = self.resume_engine.get_completed_parts()
            total_remaining = len(remaining)

            for i, part_number in enumerate(remaining, 1):
                if part_number in completed_parts:
                    continue

                self.log(f"[{i}/{total_remaining}] Searching: {part_number}")

                def do_search(pn=part_number):
                    return self.scraper.search_part(page, pn)

                result = self.rate_limiter.execute_with_retry(do_search, part_number)
                results_by_part[part_number] = result

                # Log the result
                status = result.get("status", "UNKNOWN")
                if status == "FOUND":
                    self.log(
                        f"  FOUND — {result.get('marcone_name', '')}, "
                        f"{result.get('price', '')}, "
                        f"{result.get('availability', '')}"
                    )
                    self.resume_engine.mark_completed(part_number)
                elif "ERROR" in status:
                    self.log(f"  {status}")
                    self.resume_engine.mark_failed(part_number)
                    self._log_error(part_number, status)
                else:
                    self.log(f"  {status}")
                    self.resume_engine.mark_completed(part_number)

                # Rate limit delay (skip on last item)
                if i < total_remaining:
                    self.rate_limiter.wait_between_searches()

            # Step 6: Write output files
            self.log("")
            self.log("STEP 5: Saving results...")
            output_csv, output_json = self._write_results(
                records, results_by_part, parts_map
            )

            # Step 7: Clean up progress file
            self.resume_engine.finish()

            # Step 8: Summary
            elapsed = time.time() - start_time
            self._print_summary(results_by_part, elapsed)

            # Log rate limiter stats
            stats = self.rate_limiter.get_stats()
            if stats["total_rate_limits"] > 0:
                self.log(f"  Rate limit pauses: {stats['total_rate_limits']}")

            self.log(f"Results CSV: {output_csv}")
            self.log(f"Results JSON: {output_json}")
            self.log(f"Run log: {self.run_log_path}")

        except RunAborted as e:
            self.log(str(e))
            self.log("Run aborted. Progress saved — you can resume later.")
        except KeyboardInterrupt:
            self.log("Interrupted by user. Progress saved — you can resume later.")
        except Exception as e:
            self.log(f"FATAL ERROR: {e}")
            self._log_error("FATAL", str(e))
            raise
        finally:
            self.session_manager.close()
            self._log_file.close()

    def _write_results(self, records, results_by_part, parts_map):
        """Write results to both CSV and JSON formats."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = self.output_dir / f"results_{timestamp}.csv"
        output_json = self.output_dir / f"results_{timestamp}.json"

        # Build output rows — one row per original record
        output_rows = []
        for rec in records:
            pn = rec["part_number"]
            if not pn:
                continue

            result = results_by_part.get(pn, {})

            row = {
                "part_number": pn,
                "marcone_part_number": result.get("marcone_part_number", ""),
                "marcone_name": result.get("marcone_name", ""),
                "wholesale_price": result.get("price", ""),
                "availability": result.get("availability", ""),
                "vendor": self.distributor.get("code", "MC"),
                "lookup_timestamp": result.get("lookup_timestamp", ""),
                "status": result.get("status", "NOT PROCESSED"),
                "batch_ref": rec.get("batch_ref", ""),
                "approval_status": rec.get("approval_status", ""),
                "vendor_action": rec.get("vendor_action", ""),
                "notes": rec.get("notes", ""),
            }
            output_rows.append(row)

        # Write CSV
        with open(output_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(output_rows)

        self.log(f"CSV written: {output_csv.name} ({len(output_rows)} rows)")

        # Write JSON (dashboard-friendly format)
        json_data = {
            "run_timestamp": datetime.now().isoformat(),
            "source_file": str(self.prtsprcs_path),
            "distributor": self.distributor["name"],
            "summary": {
                "total": len(results_by_part),
                "found": sum(1 for r in results_by_part.values() if r.get("status") == "FOUND"),
                "not_found": sum(1 for r in results_by_part.values() if r.get("status") == "NOT FOUND"),
                "errors": sum(1 for r in results_by_part.values() if "ERROR" in r.get("status", "")),
            },
            "rows": output_rows,
        }

        with open(output_json, "w") as f:
            json.dump(json_data, f, indent=2)

        self.log(f"JSON written: {output_json.name}")

        return output_csv, output_json

    def _print_summary(self, results_by_part, elapsed_seconds):
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

    def log(self, message):
        """Print to terminal and write to run log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        if self._log_file and not self._log_file.closed:
            self._log_file.write(line + "\n")
            self._log_file.flush()

    def _log_error(self, part_number, error_msg):
        """Write a failed lookup to the error log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_file = self.error_log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        with open(error_file, "a") as f:
            f.write(f"[{timestamp}] {part_number}: {error_msg}\n")

    def _load_json(self, path):
        """Load a JSON config file."""
        with open(path, "r") as f:
            return json.load(f)
