#!/usr/bin/env python3
"""
Parts Agent Dashboard — Local web server for viewing run results.

Standard library only. No pip installs required.
Serves a web dashboard on http://localhost:8050.
"""

import csv
import json
import os
import re
import webbrowser
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, unquote

PROJECT_ROOT = Path(__file__).parent
DATA_OUTPUT = PROJECT_ROOT / "data" / "output"
CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"
DISTRIBUTOR_DIR = PROJECT_ROOT / "config" / "distributors"
STATIC_DIR = PROJECT_ROOT / "static"

# Lazy-loaded NetData instance
_netdata_instance = None

PORT = 8050


def parse_results_csv(filepath):
    """Parse a results CSV file and return rows as list of dicts."""
    rows = []
    try:
        with open(filepath, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    except Exception:
        pass
    return rows


def summarize_run(filepath, rows):
    """Build a summary dict for a single run file."""
    filename = filepath.name
    # Extract timestamp from filename: results_YYYYMMDD_HHMMSS.csv
    match = re.search(r"results_(\d{8}_\d{6})", filename)
    if match:
        ts_str = match.group(1)
        try:
            ts = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
            timestamp = ts.isoformat()
            display_time = ts.strftime("%b %d, %Y %I:%M %p")
        except ValueError:
            timestamp = ""
            display_time = filename
    else:
        timestamp = ""
        display_time = filename

    total = len(rows)
    found = sum(1 for r in rows if r.get("status") == "FOUND")
    not_found = sum(1 for r in rows if r.get("status") == "NOT FOUND")
    errors = sum(1 for r in rows if "ERROR" in r.get("status", ""))

    return {
        "filename": filename,
        "timestamp": timestamp,
        "display_time": display_time,
        "total": total,
        "found": found,
        "not_found": not_found,
        "errors": errors,
        "success_rate": round((found / total) * 100, 1) if total > 0 else 0,
    }


def get_all_runs():
    """Scan data/output/ for results CSVs, return summaries sorted newest first."""
    runs = []
    if not DATA_OUTPUT.exists():
        return runs

    for filepath in sorted(DATA_OUTPUT.glob("results_*.csv"), reverse=True):
        rows = parse_results_csv(filepath)
        summary = summarize_run(filepath, rows)
        runs.append(summary)

    return runs


def get_netdata_instance():
    """Lazy-load the NetData module for dashboard enrichment."""
    global _netdata_instance
    if _netdata_instance is None:
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
            netdata_path = config.get("netdata_path", "")
            if netdata_path and Path(netdata_path).exists():
                import sys
                sys.path.insert(0, str(PROJECT_ROOT))
                from src.netdata import NetData
                _netdata_instance = NetData(netdata_path, lambda msg: None)
        except Exception:
            _netdata_instance = False  # Mark as failed so we don't retry
    return _netdata_instance if _netdata_instance else None


def get_netdata_stats():
    """Return NetData status and stats for the dashboard."""
    nd = get_netdata_instance()
    if not nd:
        return {"available": False}
    stats = nd.get_stats()
    stats["vendors"] = nd.get_vendor_list()
    return stats


def get_model_recommendation(model_number):
    """Look up a model recommendation from NetData."""
    nd = get_netdata_instance()
    if not nd:
        return {"model": model_number, "recommendation": "", "found": False}
    rec = nd.get_model_recommendation(model_number)
    return {"model": model_number, "recommendation": rec, "found": bool(rec)}


def get_config_safe():
    """Return config data with password redacted."""
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except Exception:
        return {"error": "Could not load config"}

    # Redact password
    safe = {k: v for k, v in config.items() if k != "password"}
    safe["password"] = "••••••••"

    # Load distributor name
    dist_name = config.get("distributor", "unknown")
    dist_path = DISTRIBUTOR_DIR / f"{dist_name}.json"
    if dist_path.exists():
        try:
            with open(dist_path, "r") as f:
                dist = json.load(f)
            safe["distributor_name"] = dist.get("name", dist_name)
        except Exception:
            safe["distributor_name"] = dist_name

    return safe


class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for the dashboard API and static files."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/" or path == "/index.html":
            self._serve_static("index.html")
        elif path == "/api/runs":
            self._json_response(get_all_runs())
        elif path.startswith("/api/run/"):
            filename = path[len("/api/run/"):]
            self._serve_run(filename)
        elif path == "/api/latest":
            self._serve_latest()
        elif path == "/api/config":
            self._json_response(get_config_safe())
        elif path == "/api/netdata":
            self._json_response(get_netdata_stats())
        elif path.startswith("/api/model/"):
            model = path[len("/api/model/"):]
            self._json_response(get_model_recommendation(unquote(model)))
        elif path.startswith("/static/"):
            # Serve files from static/ directory
            rel = path[len("/static/"):]
            self._serve_static(rel)
        else:
            self.send_error(404, "Not found")

    def _json_response(self, data, status=200):
        """Send a JSON response."""
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _serve_run(self, filename):
        """Serve full CSV data for a specific run."""
        # Sanitize filename to prevent path traversal
        filename = Path(filename).name
        filepath = DATA_OUTPUT / filename
        if not filepath.exists() or not filepath.name.startswith("results_"):
            self.send_error(404, "Run not found")
            return
        rows = parse_results_csv(filepath)
        summary = summarize_run(filepath, rows)
        self._json_response({"summary": summary, "rows": rows})

    def _serve_latest(self):
        """Serve the most recent run."""
        runs = get_all_runs()
        if not runs:
            self._json_response({"summary": None, "rows": []})
            return
        latest = runs[0]
        filepath = DATA_OUTPUT / latest["filename"]
        rows = parse_results_csv(filepath)
        self._json_response({"summary": latest, "rows": rows})

    def _serve_static(self, filename):
        """Serve a file from the static/ directory."""
        filepath = STATIC_DIR / filename
        if not filepath.exists():
            self.send_error(404, f"File not found: {filename}")
            return

        ext = filepath.suffix.lower()
        content_types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        ctype = content_types.get(ext, "application/octet-stream")

        with open(filepath, "rb") as f:
            body = f.read()

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Suppress default request logging for cleaner terminal output."""
        pass


def main():
    # Ensure static directory exists
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

    # Check for index.html
    index = STATIC_DIR / "index.html"
    if not index.exists():
        print(f"WARNING: {index} does not exist yet.")
        print("The dashboard will show a 404 until static/index.html is created.")
        print()

    server = HTTPServer(("localhost", PORT), DashboardHandler)
    url = f"http://localhost:{PORT}"

    print(f"Parts Agent Dashboard running at {url}")
    print(f"Serving results from: {DATA_OUTPUT}")
    print("Press Ctrl+C to stop.\n")

    # Auto-open browser
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
