"""
Resume Engine — Crash recovery for batch processing.

Ported directly from parts-agent v2.
"""

import json
from datetime import datetime
from pathlib import Path


class ResumeEngine:
    """Tracks batch progress and enables crash recovery."""

    def __init__(self, log_fn, output_dir):
        self.log = log_fn
        self.output_dir = Path(output_dir)
        self.progress_file = None
        self._progress = None

    def check_for_incomplete_run(self, auto_resume=False):
        """Check for any incomplete progress files from a previous run."""
        progress_files = sorted(self.output_dir.glob(".progress_*.json"))
        if not progress_files:
            return None

        latest = progress_files[-1]
        try:
            with open(latest, "r") as f:
                progress = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.log(f"Corrupt progress file {latest.name} — ignoring.")
            latest.unlink(missing_ok=True)
            return None

        completed = len(progress.get("completed", []))
        total = progress.get("total", 0)
        started = progress.get("started_at", "unknown")

        if completed >= total:
            self.log(f"Previous run completed fully. Cleaning up {latest.name}.")
            latest.unlink(missing_ok=True)
            return None

        self.log(
            f"Found incomplete run from {started}: "
            f"{completed}/{total} parts completed."
        )

        if auto_resume:
            resume = True
            self.log("Auto-resume enabled. Continuing previous run.")
        else:
            answer = input(f"Resume this run? (y/n): ").strip().lower()
            resume = answer in ("y", "yes")

        if resume:
            self.progress_file = latest
            self._progress = progress
            return progress
        else:
            self.log("Discarding incomplete run. Starting fresh.")
            latest.unlink(missing_ok=True)
            return None

    def start_new_run(self, part_numbers, source_description="PrtsPrcs"):
        """Create a new progress file for a fresh run."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.progress_file = self.output_dir / f".progress_{timestamp}.json"

        self._progress = {
            "started_at": datetime.now().isoformat(),
            "total": len(part_numbers),
            "part_numbers": part_numbers,
            "source": source_description,
            "completed": [],
            "failed": [],
            "last_updated": datetime.now().isoformat(),
        }
        self._save()
        self.log(f"Progress tracking started: {self.progress_file.name}")

    def get_completed_parts(self):
        if not self._progress:
            return set()
        return set(self._progress.get("completed", []))

    def get_remaining_parts(self):
        if not self._progress:
            return []
        completed = set(self._progress.get("completed", []))
        return [p for p in self._progress["part_numbers"] if p not in completed]

    def mark_completed(self, part_number):
        if self._progress is None:
            return
        if part_number not in self._progress["completed"]:
            self._progress["completed"].append(part_number)
        self._progress["last_updated"] = datetime.now().isoformat()
        self._save()

    def mark_failed(self, part_number):
        if self._progress is None:
            return
        if part_number not in self._progress["failed"]:
            self._progress["failed"].append(part_number)
        if part_number not in self._progress["completed"]:
            self._progress["completed"].append(part_number)
        self._progress["last_updated"] = datetime.now().isoformat()
        self._save()

    def finish(self):
        if self.progress_file and self.progress_file.exists():
            self.progress_file.unlink()
            self.log("Run complete. Progress file cleaned up.")
        self._progress = None

    def _save(self):
        if self.progress_file and self._progress:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            with open(self.progress_file, "w") as f:
                json.dump(self._progress, f, indent=2)
