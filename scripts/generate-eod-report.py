#!/usr/bin/env python3
"""
Claude Mainframe — EOD Report Generator
Aggregates daily action logs and session data into a human-readable EOD report.

Usage:
    python3 generate-eod-report.py              # Today's report
    python3 generate-eod-report.py 2026-03-21   # Specific date
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

MAINFRAME_DIR = os.path.expanduser("~/Documents/Claude/Mainframe")


def load_actions(date_str):
    """Load all actions from the daily JSONL log."""
    actions_file = os.path.join(MAINFRAME_DIR, "logs", "actions", f"{date_str}.jsonl")
    if not os.path.exists(actions_file):
        return []
    actions = []
    with open(actions_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actions.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return actions


def load_session_events(date_str):
    """Load session start/end events for the given date."""
    events_file = os.path.join(MAINFRAME_DIR, "logs", "session-events.jsonl")
    if not os.path.exists(events_file):
        return []
    events = []
    with open(events_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("ts", "").startswith(date_str):
                    events.append(event)
            except json.JSONDecodeError:
                continue
    return events


def load_session_summaries(date_str):
    """Load session JSONL summaries for the date's month."""
    year_month = date_str[:7]  # "2026-03"
    sessions_dir = os.path.join(MAINFRAME_DIR, "logs", "sessions", year_month)
    if not os.path.isdir(sessions_dir):
        return []

    summaries = []
    for f in sorted(os.listdir(sessions_dir)):
        if f.endswith(".jsonl"):
            filepath = os.path.join(sessions_dir, f)
            try:
                with open(filepath, "r") as fh:
                    first_line = fh.readline().strip()
                    if first_line:
                        data = json.loads(first_line)
                        # Check if session is from our target date
                        if data.get("end_ts", "").startswith(date_str) or data.get("start_ts", "").startswith(date_str):
                            summaries.append(data)
            except (json.JSONDecodeError, Exception):
                continue
    return summaries


def check_learnings_status(date_str):
    """Check which session markdown files still need learnings."""
    year_month = date_str[:7]
    sessions_dir = os.path.join(MAINFRAME_DIR, "logs", "sessions", year_month)
    if not os.path.isdir(sessions_dir):
        return [], []

    complete = []
    needs_learnings = []

    for f in sorted(os.listdir(sessions_dir)):
        if not f.endswith(".md"):
            continue
        filepath = os.path.join(sessions_dir, f)
        try:
            with open(filepath, "r") as fh:
                content = fh.read()
                if "[NEEDS LEARNINGS]" in content:
                    needs_learnings.append(f)
                elif "## What Was Learned" in content:
                    complete.append(f)
        except Exception:
            continue

    return complete, needs_learnings


def generate_report(date_str):
    """Generate the EOD report."""
    actions = load_actions(date_str)
    events = load_session_events(date_str)
    summaries = load_session_summaries(date_str)
    complete_logs, incomplete_logs = check_learnings_status(date_str)

    # Aggregate from actions
    sessions_seen = set()
    tool_counts = Counter()
    files_touched = set()

    for action in actions:
        sessions_seen.add(action.get("sid", ""))
        tool_counts[action.get("tool", "")] += 1
        target = action.get("target", "")
        if target and action.get("tool") in ("Write", "Edit", "Read"):
            files_touched.add(target)

    total_tool_calls = len(actions)
    session_count = len(sessions_seen) if sessions_seen else len([e for e in events if e.get("event") == "start"])

    # Aggregate from session summaries
    total_files_created = 0
    total_files_modified = 0
    category_counts = Counter()
    session_details = []

    for s in summaries:
        total_files_created += len(s.get("files_created", []))
        total_files_modified += len(s.get("files_modified", []))
        cat = s.get("category", "general")
        category_counts[cat] += 1
        session_details.append({
            "id": s.get("session_id", "unknown")[:8],
            "task": s.get("task_description", "Unknown")[:100],
            "tools": s.get("total_tool_uses", 0),
            "files_created": len(s.get("files_created", [])),
            "files_modified": len(s.get("files_modified", [])),
            "category": cat,
        })

    # Build report
    report = f"""# EOD Report — {date_str}

## Summary
- **Sessions:** {max(session_count, len(summaries))}
- **Total tool calls:** {total_tool_calls}
- **Files created:** {total_files_created}
- **Files modified:** {total_files_modified}

## Tool Usage
"""
    for tool, count in tool_counts.most_common(15):
        report += f"- {tool}: {count}\n"

    if category_counts:
        report += "\n## By Category\n"
        report += "| Category | Sessions |\n|----------|----------|\n"
        for cat, count in category_counts.most_common():
            report += f"| {cat} | {count} |\n"

    if session_details:
        report += "\n## Sessions\n"
        for i, s in enumerate(session_details, 1):
            report += f"\n### {i}. {s['task']}\n"
            report += f"- ID: `{s['id']}` | Category: {s['category']}\n"
            report += f"- Tool calls: {s['tools']} | Created: {s['files_created']} | Modified: {s['files_modified']}\n"

    if incomplete_logs:
        report += "\n## Logs Missing Learnings\n"
        for log in incomplete_logs:
            report += f"- {log}\n"

    if complete_logs:
        report += f"\n## Complete Logs: {len(complete_logs)}\n"

    report += f"\n---\n*Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}*\n"

    # Write report
    reports_dir = os.path.join(MAINFRAME_DIR, "logs", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, f"eod-{date_str}.md")

    with open(report_file, "w") as f:
        f.write(report)

    print(f"EOD report written to {report_file}")
    return report_file


if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    generate_report(date_str)
