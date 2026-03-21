#!/usr/bin/env python3
"""
Claude Mainframe — Weekly Report Generator
Aggregates 7 days of action logs and session data into a weekly rollup.

Usage:
    python3 generate-weekly-report.py              # Current week (Mon-Sun)
    python3 generate-weekly-report.py 2026-03-17    # Week starting on this Monday
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter

MAINFRAME_DIR = os.path.expanduser("~/Documents/Claude/Mainframe")


def get_week_dates(start_date_str=None):
    """Get Monday-Sunday dates for the week."""
    if start_date_str:
        monday = datetime.strptime(start_date_str, "%Y-%m-%d")
    else:
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())

    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]


def load_all_actions(dates):
    """Load actions across multiple dates."""
    all_actions = []
    for date_str in dates:
        actions_file = os.path.join(MAINFRAME_DIR, "logs", "actions", f"{date_str}.jsonl")
        if not os.path.exists(actions_file):
            # Check for compressed version
            gz_file = actions_file + ".gz"
            if os.path.exists(gz_file):
                import gzip
                with gzip.open(gz_file, "rt") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                action = json.loads(line)
                                action["_date"] = date_str
                                all_actions.append(action)
                            except json.JSONDecodeError:
                                continue
            continue
        with open(actions_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        action = json.loads(line)
                        action["_date"] = date_str
                        all_actions.append(action)
                    except json.JSONDecodeError:
                        continue
    return all_actions


def load_all_sessions(dates):
    """Load session summaries across the date range."""
    months_seen = set()
    for d in dates:
        months_seen.add(d[:7])

    all_sessions = []
    for month in months_seen:
        sessions_dir = os.path.join(MAINFRAME_DIR, "logs", "sessions", month)
        if not os.path.isdir(sessions_dir):
            continue
        for f in sorted(os.listdir(sessions_dir)):
            if not f.endswith(".jsonl"):
                continue
            filepath = os.path.join(sessions_dir, f)
            try:
                with open(filepath, "r") as fh:
                    first_line = fh.readline().strip()
                    if first_line:
                        data = json.loads(first_line)
                        end_date = data.get("end_ts", "")[:10]
                        if end_date in dates:
                            all_sessions.append(data)
            except (json.JSONDecodeError, Exception):
                continue
    return all_sessions


def load_learnings(dates):
    """Extract learnings from session markdown files."""
    months_seen = set()
    for d in dates:
        months_seen.add(d[:7])

    learnings = []
    for month in months_seen:
        sessions_dir = os.path.join(MAINFRAME_DIR, "logs", "sessions", month)
        if not os.path.isdir(sessions_dir):
            continue
        for f in sorted(os.listdir(sessions_dir)):
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(sessions_dir, f)
            try:
                with open(filepath, "r") as fh:
                    content = fh.read()
                    if "[NEEDS LEARNINGS]" in content:
                        continue
                    # Extract the learnings section
                    if "## What Was Learned" in content:
                        start = content.index("## What Was Learned")
                        end = content.index("##", start + 20) if "##" in content[start + 20:] else len(content)
                        section = content[start:start + (end - start) if end > start else len(content)]
                        # Only include if it has real content
                        lines = [l.strip() for l in section.split("\n") if l.strip() and not l.startswith("##")]
                        if lines:
                            learnings.append({"file": f, "content": "\n".join(lines[:5])})
            except Exception:
                continue

    return learnings


def generate_report(start_date_str=None):
    """Generate the weekly report."""
    dates = get_week_dates(start_date_str)
    week_start = dates[0]
    week_end = dates[-1]

    actions = load_all_actions(dates)
    sessions = load_all_sessions(dates)
    learnings = load_learnings(dates)

    # Aggregate
    total_tool_calls = len(actions)
    sessions_by_day = Counter()
    tool_counts = Counter()
    category_counts = Counter()
    total_files_created = 0
    total_files_modified = 0
    all_files_created = []

    for a in actions:
        tool_counts[a.get("tool", "")] += 1
        sessions_by_day[a.get("_date", "")] += 0  # just track days

    unique_sessions = set()
    for s in sessions:
        sid = s.get("session_id", "")
        unique_sessions.add(sid)
        cat = s.get("category", "general")
        category_counts[cat] += 1
        fc = s.get("files_created", [])
        fm = s.get("files_modified", [])
        total_files_created += len(fc)
        total_files_modified += len(fm)
        all_files_created.extend(fc)
        end_date = s.get("end_ts", "")[:10]
        sessions_by_day[end_date] += 1

    # Calculate active days
    active_days = len(set(a.get("_date") for a in actions if a.get("_date")))

    # ISO week number
    week_num = datetime.strptime(week_start, "%Y-%m-%d").isocalendar()[1]

    report = f"""# Weekly Report — Week {week_num}, {week_start[:4]}
**{week_start} to {week_end}**

## Overview
- **Sessions:** {len(sessions)}
- **Active days:** {active_days}/7
- **Total tool calls:** {total_tool_calls}
- **Files created:** {total_files_created}
- **Files modified:** {total_files_modified}

## By Category
| Category | Sessions |
|----------|----------|
"""
    for cat, count in category_counts.most_common():
        report += f"| {cat} | {count} |\n"

    report += "\n## Daily Breakdown\n| Date | Tool Calls |\n|------|------------|\n"
    for date in dates:
        day_actions = len([a for a in actions if a.get("_date") == date])
        if day_actions > 0:
            report += f"| {date} | {day_actions} |\n"

    report += "\n## Top Tools\n"
    for tool, count in tool_counts.most_common(10):
        report += f"- {tool}: {count}\n"

    if all_files_created:
        report += "\n## Key Deliverables\n"
        # Group by directory
        from collections import defaultdict
        by_dir = defaultdict(list)
        for f in all_files_created:
            parts = f.rsplit("/", 1)
            dir_name = parts[0] if len(parts) > 1 else "."
            filename = parts[1] if len(parts) > 1 else f
            by_dir[dir_name].append(filename)

        for dir_path, files in sorted(by_dir.items()):
            # Shorten path for display
            short_dir = dir_path.replace(os.path.expanduser("~"), "~")
            report += f"\n**{short_dir}/**\n"
            for fname in sorted(files)[:10]:
                report += f"- {fname}\n"
            if len(files) > 10:
                report += f"- ... and {len(files) - 10} more\n"

    if learnings:
        report += "\n## Learnings Summary\n"
        for l in learnings[:15]:
            report += f"\n**{l['file']}:**\n{l['content']}\n"

    incomplete = [s for s in sessions if s.get("needs_learnings")]
    if incomplete:
        report += f"\n## Sessions Missing Learnings: {len(incomplete)}\n"
        for s in incomplete:
            report += f"- `{s.get('session_id', 'unknown')[:8]}`: {s.get('task_description', 'Unknown')[:80]}\n"

    report += f"\n---\n*Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}*\n"

    # Write report
    reports_dir = os.path.join(MAINFRAME_DIR, "logs", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, f"weekly-{week_start[:4]}-W{week_num:02d}.md")

    with open(report_file, "w") as f:
        f.write(report)

    print(f"Weekly report written to {report_file}")
    return report_file


if __name__ == "__main__":
    start_date = sys.argv[1] if len(sys.argv) > 1 else None
    generate_report(start_date)
