"""
RSS Key Authenticator — Authenticates with Rossware's RSS Key service.

The RSS Key (key.rossware.com) is Rossware's IP-based access control.
When you authenticate, it whitelists your current IP address so you
can RDP into the Rossware hosting server.

Auth flow (reverse-engineered from the React SPA):
1. GET /v3/getbusinesstoken?business_id=X&business_password=Y&no_expire=true
   → Returns JSON: {"token": "..."}
2. GET /v4/syncrsskey?friendly_name=browser&force=true
   with header Authorization: Bearer {token}
   → Whitelists the calling IP for RDP access
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error


API_BASE = "https://api.rossware.com"


class RSSKeyAuth:
    """Handles RSS Key authentication to whitelist IP for Rossware RDP."""

    def __init__(self, config, log_fn):
        """
        Args:
            config: dict with keys: url, username, password
            log_fn: logging function
        """
        self.config = config
        self.log = log_fn
        self.token = None

    def authenticate(self):
        """Full auth flow: get token → sync key (whitelist IP).

        Returns:
            True if successful, False otherwise.
        """
        self.log("RSS Key: Authenticating...")

        # Step 1: Get business token
        token = self._get_business_token()
        if not token:
            self.log("RSS Key: Failed to get business token.")
            return False

        self.token = token
        self.log(f"RSS Key: Got token ({token[:8]}...)")

        # Step 2: Sync RSS Key (whitelist IP)
        success = self._sync_rss_key(token)
        if success:
            self.log("RSS Key: IP whitelisted successfully. RDP access enabled.")
        else:
            self.log("RSS Key: Failed to sync/whitelist IP.")

        return success

    def _get_business_token(self):
        """Get a bearer token from the Rossware API.

        GET /v3/getbusinesstoken?business_id=X&business_password=Y&no_expire=true
        """
        params = urllib.parse.urlencode({
            "business_id": self.config["username"],
            "business_password": self.config["password"],
            "no_expire": "true",
        })
        url = f"{API_BASE}/v3/getbusinesstoken?{params}"

        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("User-Agent", "RSSKey/1.0")

            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status != 200:
                    self.log(f"RSS Key: Token request returned {resp.status}")
                    return None

                data = json.loads(resp.read().decode("utf-8"))
                return data.get("token")

        except urllib.error.HTTPError as e:
            self.log(f"RSS Key: HTTP error getting token: {e.code} {e.reason}")
            return None
        except urllib.error.URLError as e:
            self.log(f"RSS Key: Network error getting token: {e.reason}")
            return None
        except Exception as e:
            self.log(f"RSS Key: Unexpected error getting token: {e}")
            return None

    def _sync_rss_key(self, token):
        """Sync the RSS key to whitelist the current IP.

        Tries port 3389 first (direct), falls back to port 443 (standard HTTPS).
        GET /v4/syncrsskey?friendly_name=hri-worker&force=true
        Authorization: Bearer {token}
        """
        params = urllib.parse.urlencode({
            "friendly_name": "hri-worker-01",
            "force": "true",
        })

        # Try port 3389 first (same as the web app does)
        endpoints = [
            f"{API_BASE}:3389/v4/syncrsskey?{params}",
            f"{API_BASE}/v4/syncrsskey?{params}",
        ]

        for url in endpoints:
            try:
                req = urllib.request.Request(url, method="GET")
                req.add_header("Authorization", f"Bearer {token}")
                req.add_header("User-Agent", "RSSKey/1.0")

                with urllib.request.urlopen(req, timeout=10) as resp:
                    body = resp.read().decode("utf-8")

                    if resp.status < 400:
                        self.log(f"RSS Key: Sync successful via {url.split('/v4')[0]}")
                        return True
                    else:
                        self.log(f"RSS Key: Sync returned {resp.status}: {body[:200]}")

            except urllib.error.HTTPError as e:
                if 400 <= e.code < 500:
                    self.log(f"RSS Key: Auth error on sync: {e.code}. Token may be expired.")
                    return False
                self.log(f"RSS Key: HTTP {e.code} on {url.split('?')[0]}, trying next...")
            except (urllib.error.URLError, TimeoutError):
                self.log(f"RSS Key: Timeout/unreachable on {url.split('?')[0]}, trying next...")
            except Exception as e:
                self.log(f"RSS Key: Error on sync: {e}, trying next...")

        return False

    def keep_alive(self, interval_minutes=10):
        """Re-sync periodically to keep the IP whitelisted.

        Call this in a background thread if running long jobs.
        """
        if not self.token:
            self.log("RSS Key: No token available for keep-alive.")
            return

        while True:
            time.sleep(interval_minutes * 60)
            self.log("RSS Key: Keep-alive sync...")
            success = self._sync_rss_key(self.token)
            if not success:
                self.log("RSS Key: Keep-alive failed. Re-authenticating...")
                self.authenticate()
