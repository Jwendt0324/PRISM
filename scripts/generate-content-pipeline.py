#!/usr/bin/env python3
"""
Claude PRISM — Content Pipeline Status Generator
Scans content production across all clients from session logs and content directories.

Usage:
    python3 generate-content-pipeline.py              # Current status
    python3 generate-content-pipeline.py 2026-03-21   # Specific date
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

PRISM_DIR = os.path.expanduser("~/Documents/Claude/PRISM")


def scan_session_logs(lookback_days=7):
    """Scan recent session logs for content-related work."""
    now = datetime.now()
    content_sessions = []
    seen_sessions = set()

    for days_back in range(lookback_days):
        date = now - timedelta(days=days_back)
        year_month = date.strftime("%Y-%m")
        sessions_dir = os.path.join(PRISM_DIR, "logs", "sessions", year_month)

        if not os.path.isdir(sessions_dir):
            continue

        for f in os.listdir(sessions_dir):
            if not f.endswith(".jsonl"):
                continue
            filepath = os.path.join(sessions_dir, f)
            try:
                with open(filepath, "r") as fh:
                    first_line = fh.readline().strip()
                    if not first_line:
                        continue
                    data = json.loads(first_line)
                    cat = data.get("category", "")
                    task = data.get("task_description", "")
                    # Clean task description: take first line only, strip script headers
                    task_clean = task.split("\n")[0].strip() if task else ""
                    if task_clean.startswith("#!") or task_clean.startswith('"""'):
                        task_clean = task_clean.lstrip("#!/usr/bin/env python3").strip().strip('"').strip()
                    if not task_clean:
                        task_clean = "(no description)"
                    if cat in ("content", "article", "batch-content") or \
                       any(kw in task.lower() for kw in ["article", "content", "transcript", "qa", "batch"]):
                        entry = {
                            "date": data.get("end_ts", data.get("start_ts", ""))[:10],
                            "task": task_clean[:120],
                            "files_created": data.get("files_created", []),
                            "files_modified": data.get("files_modified", []),
                            "category": cat,
                        }
                        # Deduplicate by date+task combo
                        dedup_key = f"{entry['date']}:{entry['task'][:60]}"
                        if dedup_key not in seen_sessions:
                            seen_sessions.add(dedup_key)
                            content_sessions.append(entry)
            except (json.JSONDecodeError, Exception):
                continue

    return content_sessions


def scan_content_directories():
    """Find content files across the PRISM and common output dirs."""
    content_files = defaultdict(list)
    search_dirs = [
        PRISM_DIR,
        os.path.expanduser("~/Documents/Claude"),
    ]

    for base in search_dirs:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            # Skip logs, scripts, hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("logs", "scripts", "__pycache__", ".backups", "node_modules")]
            for f in files:
                if not f.endswith((".md", ".docx")):
                    continue
                fpath = os.path.join(root, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                age = datetime.now() - mtime
                if age.days <= 7:
                    # Try to guess client from path
                    lower_path = fpath.lower()
                    client = "Unknown"
                    client_markers = {
                        "acoustic": "[Client — Local Retail Business]",
                        "discover-strength": "[Client — Fitness Brand]",
                        "[client-id]": "[Client — Appliance Repair]",
                        "sloan": "[Client — Appliance Repair]",
                        "ryan": "[Client Name]",
                        "blitz": "[Methodology Partner]",
                        "hri": "[Your Agency]",
                    }
                    for marker, name in client_markers.items():
                        if marker in lower_path:
                            client = name
                            break
                    # Deduplicate by filename
                    if f not in [x["name"] for x in content_files[client]]:
                        content_files[client].append({
                            "file": fpath,
                            "name": f,
                            "modified": mtime.strftime("%Y-%m-%d"),
                            "age_days": age.days,
                        })

    return content_files


def scan_action_logs(lookback_days=7):
    """Count content-related tool calls from action logs."""
    now = datetime.now()
    content_actions = 0
    total_actions = 0

    for days_back in range(lookback_days):
        date = now - timedelta(days=days_back)
        date_str = date.strftime("%Y-%m-%d")
        action_file = os.path.join(PRISM_DIR, "logs", "actions", f"{date_str}.jsonl")
        if not os.path.exists(action_file):
            continue
        with open(action_file, "r") as fh:
            for line in fh:
                total_actions += 1
                line_lower = line.lower()
                if any(kw in line_lower for kw in ["article", "content", "transcript", "docx", "qa"]):
                    content_actions += 1

    return content_actions, total_actions


def generate_report(date_str):
    """Generate the content pipeline status report."""
    sessions = scan_session_logs()
    content_files = scan_content_directories()
    content_actions, total_actions = scan_action_logs()

    # Group sessions by client (rough heuristic)
    client_sessions = defaultdict(list)
    for s in sessions:
        task_lower = s["task"].lower()
        client = "General"
        client_markers = {
            "acoustic": "[Client — Local Retail Business]",
            "discover": "[Client — Fitness Brand]",
            "[client-id]": "[Client — Appliance Repair]",
            "sloan": "[Client — Appliance Repair]",
            "ryan": "[Client Name]",
            "blitz": "[Methodology Partner]",
        }
        for marker, name in client_markers.items():
            if marker in task_lower:
                client = name
                break
        client_sessions[client].append(s)

    # Merge client lists
    all_clients = set(list(content_files.keys()) + list(client_sessions.keys()))
    all_clients.discard("Unknown")
    all_clients.discard("General")

    report = f"""# Content Pipeline Status — {date_str}

## Overview (Last 7 Days)
- Content sessions: {len(sessions)}
- Content-related actions: {content_actions} / {total_actions} total
- Clients with activity: {len(all_clients)}

## By Client
"""

    for client in sorted(all_clients):
        files = content_files.get(client, [])
        sess = client_sessions.get(client, [])
        report += f"\n### {client}\n"
        if sess:
            report += f"- Sessions: {len(sess)}\n"
            for s in sess[:5]:
                report += f"  - [{s['date']}] {s['task']}\n"
        if files:
            report += f"- Recent files: {len(files)}\n"
            for f in files[:5]:
                report += f"  - [{f['modified']}] {f['name']}\n"
        if not sess and not files:
            report += "- No activity\n"

    # Uncategorized
    general_sessions = client_sessions.get("General", [])
    unknown_files = content_files.get("Unknown", [])
    if general_sessions or unknown_files:
        report += "\n### Uncategorized\n"
        for s in general_sessions[:5]:
            report += f"- [{s['date']}] {s['task']}\n"
        for f in unknown_files[:5]:
            report += f"- [{f['modified']}] {f['name']}\n"

    report += f"""
## Pipeline Gaps
- Clients without recent content: Check CONTEXT.md client list against active clients above
- No automated QA tracking yet — manual /qa runs only

## Recommendations
1. Review any client missing from the "By Client" section above
2. Run /batch-content for clients with content gaps
3. Run /qa on any recently completed articles

---
*Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}*
"""

    reports_dir = os.path.join(PRISM_DIR, "logs", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, f"content-pipeline-{date_str}.md")

    with open(report_file, "w") as f:
        f.write(report)

    print(f"Content pipeline report written to {report_file}")
    return report_file


if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    generate_report(date_str)
