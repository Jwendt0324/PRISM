"""
Rate Limiter — Configurable delays, exponential backoff, and error recovery.

Controls the pace of searches to avoid overloading distributor sites,
handles transient errors with retries, and aborts runs that are clearly broken.
"""

import time


class RateLimitDetected(Exception):
    """Raised when the distributor site is rate limiting us."""
    pass


class RunAborted(Exception):
    """Raised when error rate exceeds the abort threshold."""
    pass


class RateLimiter:
    """Controls search pacing, retries, and error thresholds."""

    # Backoff schedule: (attempt_number, wait_seconds)
    DEFAULT_BACKOFF = [5, 15, 60]

    def __init__(self, config, log_fn):
        """
        Args:
            config: dict from config/config.json
            log_fn: callable for logging (message) -> None
        """
        self.log = log_fn
        self.delay = config.get("[google-doc-id]", 2)
        self.max_retries = config.get("max_retries", 4)
        self.abort_threshold_pct = config.get("error_abort_threshold_pct", 50)
        self.rate_limit_pause_minutes = config.get("rate_limit_pause_minutes", 5)

        # Run-level counters
        self.total_attempted = 0
        self.total_errors = 0
        self.total_rate_limits = 0

    def wait_between_searches(self):
        """Enforce the configured delay between consecutive searches."""
        if self.delay > 0:
            time.sleep(self.delay)

    def execute_with_retry(self, search_fn, part_number):
        """Execute a search function with exponential backoff on failure.

        Args:
            search_fn: callable() -> result dict. Should raise Exception on failure,
                       or raise RateLimitDetected if rate limiting is detected.
            part_number: str, for logging only.

        Returns:
            The result dict from search_fn on success.

        Raises:
            RunAborted: if error rate exceeds the abort threshold.
        """
        self.total_attempted += 1
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                result = search_fn()

                # If the result indicates a rate limit, raise so we handle it
                if isinstance(result, dict) and result.get("status", "").startswith("ERROR - RATE"):
                    raise RateLimitDetected(result.get("status", "Rate limited"))

                return result

            except RateLimitDetected as e:
                self.total_rate_limits += 1
                pause_seconds = self.rate_limit_pause_minutes * 60
                self.log(
                    f"  RATE LIMITED on {part_number}. "
                    f"Pausing for {self.rate_limit_pause_minutes} minutes..."
                )
                time.sleep(pause_seconds)
                self.log(f"  Resuming after rate limit pause.")
                last_error = e
                # Don't count rate limits toward the backoff schedule — just pause and retry
                continue

            except Exception as e:
                last_error = e
                if attempt < self.max_retries:
                    backoff_index = min(attempt - 1, len(self.DEFAULT_BACKOFF) - 1)
                    wait = self.DEFAULT_BACKOFF[backoff_index]
                    self.log(
                        f"  ERROR on {part_number} (attempt {attempt}/{self.max_retries}): {e}"
                    )
                    self.log(f"  Retrying in {wait} seconds...")
                    time.sleep(wait)
                else:
                    self.log(
                        f"  FAILED {part_number} after {self.max_retries} attempts: {e}"
                    )

        # All retries exhausted
        self.total_errors += 1
        self._check_abort_threshold()

        return {
            "marcone_name": "",
            "price": "",
            "availability": "",
            "status": f"ERROR - {str(last_error)[:100]}"
        }

    def _check_abort_threshold(self):
        """Abort the run if the error rate is too high.

        Only checks after at least 5 attempts to avoid aborting on the
        first couple of errors at the start of a run.
        """
        if self.total_attempted < 5:
            return

        error_pct = (self.total_errors / self.total_attempted) * 100
        if error_pct >= self.abort_threshold_pct:
            msg = (
                f"ABORTING RUN: Error rate {error_pct:.0f}% "
                f"({self.total_errors}/{self.total_attempted}) "
                f"exceeds threshold of {self.abort_threshold_pct}%. "
                f"Something is wrong — check the site or session."
            )
            self.log(msg)
            raise RunAborted(msg)

    def get_stats(self):
        """Return a summary dict of rate limiter activity for this run."""
        return {
            "total_attempted": self.total_attempted,
            "total_errors": self.total_errors,
            "total_rate_limits": self.total_rate_limits,
            "error_rate_pct": (
                round((self.total_errors / self.total_attempted) * 100, 1)
                if self.total_attempted > 0 else 0
            ),
        }
