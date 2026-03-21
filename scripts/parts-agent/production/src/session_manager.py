"""
Session Manager — Cookie persistence for distributor logins.

Logs in once, saves browser cookies/state to disk, and reuses them
on subsequent runs. Re-authenticates automatically if the session expires.

Ported directly from parts-agent v2.
"""

import json
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class SessionManager:
    """Manages authenticated browser sessions with cookie persistence."""

    def __init__(self, config, distributor, log_fn, project_root):
        self.config = config
        self.distributor = distributor
        self.log = log_fn
        self.project_root = Path(project_root)
        self.session_dir = self.project_root / "data" / "session"
        self.session_file = self.session_dir / f"{config['distributor']}_session.json"

        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def get_authenticated_page(self):
        """Return a Playwright page that is logged in and ready to search."""
        self._launch_browser()

        if self.config.get("session_reuse", True) and self.session_file.exists():
            self.log("Found saved session. Attempting to reuse...")
            if self._try_restore_session():
                return self._page
            else:
                self.log("Saved session expired or invalid. Performing fresh login...")

        self._fresh_login()
        return self._page

    def close(self):
        """Clean up browser resources."""
        if self._browser:
            try:
                self._browser.close()
            except Exception:
                pass
        if self._playwright:
            try:
                self._playwright.stop()
            except Exception:
                pass
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None

    def _launch_browser(self):
        """Start Playwright and launch a Chromium browser."""
        if self._browser:
            return

        self.log("Launching browser...")
        self._playwright = sync_playwright().start()

        browser_cfg = self.distributor.get("browser", {})
        headless = self.config.get("headless", True)

        self._browser = self._playwright.chromium.launch(
            headless=headless,
            slow_mo=browser_cfg.get("slow_mo_ms", 500)
        )
        self.log(f"Browser launched (headless={headless}).")

    def _create_context(self, storage_state=None):
        """Create a new browser context, optionally restoring saved state."""
        browser_cfg = self.distributor.get("browser", {})

        context_opts = {
            "viewport": {
                "width": browser_cfg.get("viewport_width", 1280),
                "height": browser_cfg.get("viewport_height", 900),
            },
            "user_agent": browser_cfg.get(
                "user_agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        }

        if storage_state:
            context_opts["storage_state"] = storage_state

        if self._context:
            try:
                self._context.close()
            except Exception:
                pass

        self._context = self._browser.new_context(**context_opts)
        self._page = self._context.new_page()

    def _try_restore_session(self):
        """Attempt to restore a saved session and verify it's still valid."""
        try:
            self._create_context(storage_state=str(self.session_file))

            base_url = self.distributor["base_url"]
            self.log(f"Navigating to {base_url} with saved session...")
            self._page.goto(base_url, wait_until="domcontentloaded",
                           timeout=self.distributor["timeouts"].get("page_load_ms", 30000))

            time.sleep(2)

            ready_sel = self.distributor["dashboard"]["ready_selector"]
            ready_timeout = self.distributor["dashboard"].get("ready_timeout_ms", 10000)

            try:
                self._page.wait_for_selector(ready_sel, timeout=ready_timeout)
                self.log("Session restored successfully — dashboard is ready.")
                return True
            except PlaywrightTimeout:
                login_indicator = self.distributor["login"]["success_indicator"]["value"]
                if login_indicator.lower() in self._page.url.lower():
                    self.log("Session expired — redirected to login page.")
                else:
                    self.log(f"Session invalid — dashboard selector '{ready_sel}' not found.")
                return False

        except Exception as e:
            self.log(f"Session restore failed: {e}")
            return False

    def _fresh_login(self):
        """Perform a fresh login and save the session cookies."""
        self._create_context()

        login_cfg = self.distributor["login"]
        login_url = login_cfg["url"]
        selectors = login_cfg["selectors"]
        timeouts = self.distributor["timeouts"]

        self.log(f"Navigating to login page: {login_url}")
        self._page.goto(login_url, wait_until="domcontentloaded",
                       timeout=timeouts.get("page_load_ms", 30000))
        self.log(f"Login page loaded: {self._page.url}")

        username_field = self._page.locator(selectors["username_field"])
        password_field = self._page.locator(selectors["password_field"])

        if username_field.count() == 0 or password_field.count() == 0:
            raise RuntimeError(
                f"Login form not found. "
                f"Username selector '{selectors['username_field']}' count: {username_field.count()}, "
                f"Password selector '{selectors['password_field']}' count: {password_field.count()}"
            )

        self.log("Found login form. Entering credentials...")
        username_field.first.fill(self.config["username"])
        password_field.first.fill(self.config["password"])

        submit_btn = self._page.locator(selectors["submit_button"])
        if submit_btn.count() == 0:
            raise RuntimeError(f"Submit button '{selectors['submit_button']}' not found.")

        submit_btn.first.click()

        success = self.distributor["login"]["success_indicator"]
        if success["type"] == "url_not_contains":
            try:
                self._page.wait_for_url(
                    lambda url: success["value"] not in url,
                    timeout=timeouts.get("login_redirect_ms", 15000)
                )
            except PlaywrightTimeout:
                raise RuntimeError(
                    f"Login failed — still on login page after "
                    f"{timeouts.get('login_redirect_ms', 15000)}ms. "
                    f"Check credentials in config/config.json."
                )

        time.sleep(2)
        self._page.wait_for_load_state("domcontentloaded")
        self.log(f"Login successful. Current page: {self._page.url}")

        ready_sel = self.distributor["dashboard"]["ready_selector"]
        ready_timeout = self.distributor["dashboard"].get("ready_timeout_ms", 10000)

        self.log("Waiting for dashboard to fully load...")
        time.sleep(2)
        try:
            self._page.wait_for_selector(ready_sel, timeout=ready_timeout)
            self.log("Dashboard ready.")
        except PlaywrightTimeout:
            self.log(f"WARNING: Dashboard selector '{ready_sel}' not found after {ready_timeout}ms.")

        self._save_session()

    def _save_session(self):
        """Save current browser cookies and storage to disk."""
        self.session_dir.mkdir(parents=True, exist_ok=True)
        storage = self._context.storage_state(path=str(self.session_file))
        self.log(f"Session saved to {self.session_file}")
