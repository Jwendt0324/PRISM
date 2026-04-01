"""
Dashboard Server — Serves the parts agent web dashboard.

Provides a REST API for the frontend to consume results from JSON output
files, plus serves the static HTML/JS dashboard.

Runs on configurable port (default 8050).
"""

import csv
import json
import os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote


class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves static files and JSON API endpoints."""

    # Set by DashboardServer before starting
    project_root = None
    config = None
    distributor = None

    def do_GET(self):
        """Route GET requests to API endpoints or static files."""
        if self.path == "/api/runs":
            self._api_runs()
        elif self.path.startswith("/api/run/"):
            filename = unquote(self.path[9:])
            self._api_run_detail(filename)
        elif self.path == "/api/config":
            self._api_config()
        elif self.path == "/api/status":
            self._api_status()
        else:
            # Serve static files from static/ directory
            super().do_GET()

    def translate_path(self, path):
        """Override to serve from static/ directory."""
        if path == "/" or path == "/index.html":
            return str(self.project_root / "static" / "index.html")
        # Strip leading / and serve from static/
        clean = path.lstrip("/")
        return str(self.project_root / "static" / clean)

    def _api_runs(self):
        """Return list of all result files with summaries."""
        output_dir = self.project_root / "data" / "output"
        runs = []

        # Find all JSON result files
        json_files = sorted(output_dir.glob("results_*.json"), reverse=True)
        for jf in json_files:
            try:
                with open(jf, "r") as f:
                    data = json.load(f)

                summary = data.get("summary", {})
                run_ts = data.get("run_timestamp", "")

                # Parse timestamp for display
                display_time = jf.stem.replace("results_", "")
                try:
                    dt = datetime.strptime(display_time, "%Y%m%d_%H%M%S")
                    display_time = dt.strftime("%b %d, %Y %I:%M %p")
                except ValueError:
                    pass

                runs.append({
                    "filename": jf.name,
                    "display_time": display_time,
                    "total": summary.get("total", 0),
                    "found": summary.get("found", 0),
                    "not_found": summary.get("not_found", 0),
                    "errors": summary.get("errors", 0),
                })
            except (json.JSONDecodeError, IOError):
                continue

        # Also check CSV files that don't have matching JSON
        csv_files = sorted(output_dir.glob("results_*.csv"), reverse=True)
        json_stems = {jf.stem for jf in json_files}
        for cf in csv_files:
            if cf.stem in json_stems:
                continue

            try:
                with open(cf, "r") as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                total = len(rows)
                found = sum(1 for r in rows if r.get("status") == "FOUND")
                not_found = sum(1 for r in rows if r.get("status") == "NOT FOUND")
                errors = sum(1 for r in rows if "ERROR" in r.get("status", ""))

                display_time = cf.stem.replace("results_", "")
                try:
                    dt = datetime.strptime(display_time, "%Y%m%d_%H%M%S")
                    display_time = dt.strftime("%b %d, %Y %I:%M %p")
                except ValueError:
                    pass

                runs.append({
                    "filename": cf.name,
                    "display_time": display_time,
                    "total": total,
                    "found": found,
                    "not_found": not_found,
                    "errors": errors,
                })
            except (IOError, csv.Error):
                continue

        self._json_response(runs)

    def _api_run_detail(self, filename):
        """Return full data for a specific run."""
        output_dir = self.project_root / "data" / "output"
        filepath = output_dir / filename

        if not filepath.exists():
            self._json_response({"error": "File not found"}, 404)
            return

        try:
            if filename.endswith(".json"):
                with open(filepath, "r") as f:
                    data = json.load(f)
                self._json_response(data)
            elif filename.endswith(".csv"):
                with open(filepath, "r") as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                total = len(rows)
                found = sum(1 for r in rows if r.get("status") == "FOUND")
                not_found = sum(1 for r in rows if r.get("status") == "NOT FOUND")
                errors = sum(1 for r in rows if "ERROR" in r.get("status", ""))

                display_time = filepath.stem.replace("results_", "")
                try:
                    dt = datetime.strptime(display_time, "%Y%m%d_%H%M%S")
                    display_time = dt.strftime("%b %d, %Y %I:%M %p")
                except ValueError:
                    pass

                self._json_response({
                    "summary": {
                        "total": total,
                        "found": found,
                        "not_found": not_found,
                        "errors": errors,
                        "display_time": display_time,
                    },
                    "rows": rows,
                })
            else:
                self._json_response({"error": "Unsupported file type"}, 400)
        except Exception as e:
            self._json_response({"error": str(e)}, 500)

    def _api_config(self):
        """Return sanitized config info for the dashboard header."""
        self._json_response({
            "distributor": self.config.get("distributor", ""),
            "distributor_name": self.distributor.get("name", ""),
            "username": self.config.get("username", ""),
        })

    def _api_status(self):
        """Return current agent status."""
        output_dir = self.project_root / "data" / "output"

        # Check for active progress files
        progress_files = list(output_dir.glob(".progress_*.json"))
        is_running = len(progress_files) > 0

        progress = None
        if is_running and progress_files:
            try:
                with open(progress_files[-1], "r") as f:
                    progress = json.load(f)
            except Exception:
                pass

        self._json_response({
            "running": is_running,
            "progress": progress,
        })

    def _json_response(self, data, status=200):
        """Send a JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Suppress default access logging to keep console clean."""
        pass


class DashboardServer:
    """Configures and runs the dashboard HTTP server."""

    def __init__(self, project_root, port=8050):
        self.project_root = Path(project_root)
        self.port = port

        # Load configs for the handler
        config_path = self.project_root / "config" / "config.json"
        with open(config_path, "r") as f:
            self.config = json.load(f)

        dist_name = self.config.get("distributor", "distributor")
        dist_path = self.project_root / "config" / "distributors" / f"{dist_name}.json"
        with open(dist_path, "r") as f:
            self.distributor = json.load(f)

    def start(self):
        """Start the dashboard server (blocking)."""
        # Configure handler class
        DashboardHandler.project_root = self.project_root
        DashboardHandler.config = self.config
        DashboardHandler.distributor = self.distributor

        server = HTTPServer(("0.0.0.0", self.port), DashboardHandler)
        print(f"Dashboard running at http://localhost:{self.port}")
        print(f"Press Ctrl+C to stop.")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard stopped.")
            server.server_close()

    def start_background(self):
        """Start the dashboard server in a background thread."""
        import threading

        DashboardHandler.project_root = self.project_root
        DashboardHandler.config = self.config
        DashboardHandler.distributor = self.distributor

        server = HTTPServer(("0.0.0.0", self.port), DashboardHandler)

        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        print(f"Dashboard running at http://localhost:{self.port}")
        return server
