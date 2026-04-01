"""
Batch Processing Agent — Main orchestrator.

Ties together all modules: session manager, scraper, rate limiter,
resume engine, and CSV handler into a single batch processing pipeline.
"""

import json
import time
from datetime import datetime
from pathlib import Path

from .session_manager import SessionManager
from .scraper import Scraper
from .rate_limiter import RateLimiter, RunAborted
from .resume_engine import ResumeEngine
from .csv_handler import CSVHandler
from .netdata import NetData


class BatchAgent:
    """Orchestrates the full batch parts lookup pipeline."""

    def __init__(self, project_root, headless=None, auto_resume=False, dry_run=False):
        """
        Args:
            project_root: Path to the parts-agent/ directory.
            headless: override headless setting (None = use config).
            auto_resume: if True, auto-resume incomplete runs.
            dry_run: if True, show what would be processed but don't run.
        """
        self.project_root = Path(project_root)
        self.auto_resume = auto_resume
        self.dry_run = dry_run

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

        distributor_name = self.config.get("distributor", "marcone")
        self.distributor = self._load_json(
            self.project_root / "config" / "distributors" / f"{distributor_name}.json"
        )

        # Initialize modules
        self.csv_handler = CSVHandler(
            self.log, self.project_root,
            vendor_code=self.distributor.get("code", "MC")
        )
        self.rate_limiter = RateLimiter(self.config, self.log)
        self.resume_engine = ResumeEngine(
            self.log, self.project_root / "data" / "output"
        )
        self.scraper = Scraper(self.distributor, self.log)
        self.session_manager = SessionManager(
            self.config, self.distributor, self.log, self.project_root
        )

        # NetData enrichment (optional — works without it)
        netdata_path = self.config.get("netdata_path", "")
        self.netdata = NetData(netdata_path, self.log) if netdata_path else None

    def run(self):
        """Execute the full batch processing pipeline."""
        start_time = time.time()

        self.log("=" * 60)
        self.log("PARTS LOOKUP AGENT v2 — BATCH PROCESSING")
        self.log(f"Distributor: {self.distributor['name']}")
        self.log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("=" * 60)

        try:
            # Step 1: Scan for input files
            input_files = self.csv_handler.scan_input_files()
            if not input_files:
                self.log("No CSV files found in data/input/. Nothing to do.")
                return

            # Step 2: Load and deduplicate parts
            unique_parts, all_rows = self.csv_handler.load_parts(input_files)
            if not unique_parts:
                self.log("No part numbers found in input files. Nothing to do.")
                return

            # Build model lookup for NetData enrichment
            self._model_by_part = {}
            for row in all_rows:
                pn = row["part_number"]
                model = row.get("original_model_number", "")
                if model and pn not in self._model_by_part:
                    self._model_by_part[pn] = model

            # Step 3: Check for incomplete previous run
            resumed = self.resume_engine.check_for_incomplete_run(self.auto_resume)
            if resumed:
                remaining = self.resume_engine.get_remaining_parts()
                self.log(f"Resuming: {len(remaining)} parts remaining.")
            else:
                self.resume_engine.start_new_run(unique_parts, input_files)
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
                    self.log(f"  {i}. {p}")
                self.log("Exiting dry run.")
                return

            # Step 4: Get authenticated browser session
            page = self.session_manager.get_authenticated_page()

            # Step 5: Process each part
            results_by_part = {}

            # Load any results from resumed run
            completed_parts = self.resume_engine.get_completed_parts()
            # We don't have the old results in memory — they're in the output file.
            # For resumed runs, we just skip completed parts.

            total_remaining = len(remaining)
            for i, part_number in enumerate(remaining, 1):
                if part_number in completed_parts:
                    continue

                self.log(f"[{i}/{total_remaining}] Searching: {part_number}")

                # Wrap the search in retry logic
                def do_search(pn=part_number):
                    return self.scraper.search_part(page, pn)

                result = self.rate_limiter.execute_with_retry(do_search, part_number)

                # Enrich with NetData intelligence
                if self.netdata and self.netdata.available:
                    model = self._model_by_part.get(part_number, "")
                    enrichment = self.netdata.enrich_result(part_number, model)
                    result["netdata"] = enrichment
                else:
                    result["netdata"] = {}

                results_by_part[part_number] = result

                # Log the result
                status = result.get("status", "UNKNOWN")
                netdata_extras = []
                nd = result.get("netdata", {})
                if nd.get("warehouse_location"):
                    netdata_extras.append(f"Bin: {nd['warehouse_location']}")
                if nd.get("quality_return"):
                    netdata_extras.append("QR FLAG")
                if nd.get("model_recommendation"):
                    netdata_extras.append("Model rec available")
                nd_str = f" | NetData: {', '.join(netdata_extras)}" if netdata_extras else ""

                if status == "FOUND":
                    self.log(
                        f"  FOUND — {result.get('marcone_name', '')}, "
                        f"{result.get('price', '')}, "
                        f"{result.get('availability', '')}{nd_str}"
                    )
                    self.resume_engine.mark_completed(part_number)
                elif "ERROR" in status:
                    self.log(f"  {status}{nd_str}")
                    self.resume_engine.mark_failed(part_number)
                    self._log_error(part_number, status)
                else:
                    self.log(f"  {status}{nd_str}")
                    self.resume_engine.mark_completed(part_number)

                # Rate limit delay (skip on last item)
                if i < total_remaining:
                    self.rate_limiter.wait_between_searches()

            # Step 6: Write output
            output_path = self.csv_handler.init_output()
            self.csv_handler.write_results(output_path, all_rows, results_by_part)

            # Step 7: Archive inputs
            self.csv_handler.archive_inputs(input_files)

            # Step 8: Clean up progress file
            self.resume_engine.finish()

            # Step 9: Summary
            elapsed = time.time() - start_time
            self.csv_handler.print_summary(results_by_part, elapsed)

            # Log rate limiter stats
            stats = self.rate_limiter.get_stats()
            if stats["total_rate_limits"] > 0:
                self.log(f"  Rate limit pauses: {stats['total_rate_limits']}")

            # Log NetData enrichment stats
            if self.netdata and self.netdata.available:
                nd_hits = {
                    "warehouse": sum(1 for r in results_by_part.values()
                                     if r.get("netdata", {}).get("warehouse_location")),
                    "qr_flags": sum(1 for r in results_by_part.values()
                                    if r.get("netdata", {}).get("quality_return")),
                    "model_recs": sum(1 for r in results_by_part.values()
                                      if r.get("netdata", {}).get("model_recommendation")),
                }
                self.log(f"  NetData enrichment: "
                         f"{nd_hits['warehouse']} warehouse locations, "
                         f"{nd_hits['qr_flags']} quality return flags, "
                         f"{nd_hits['model_recs']} model recommendations")

            self.log(f"Results saved to: {output_path}")
            self.log(f"Run log saved to: {self.run_log_path}")

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
