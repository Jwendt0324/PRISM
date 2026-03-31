#!/usr/bin/env python3
"""
Claude PRISM — Health Check Generator
Checks hooks, logs, rules, good-examples, stale files, and disk usage.

Usage:
    python3 generate-health-check.py              # Today's check
    python3 generate-health-check.py 2026-03-21   # Specific date
"""

import os
import sys
import stat
from datetime import datetime, timezone, timedelta
from pathlib import Path

PRISM_DIR = os.path.expanduser("~/Documents/Claude/PRISM")
CLAUDE_DIR = os.path.expanduser("~/.claude")


def check_hooks():
    """Check each hook script exists and is executable."""
    hooks_dir = os.path.join(PRISM_DIR, "claude-code", "hooks")
    expected = [
        "session-start.sh", "pre-tool-guard.sh", "enforce-naming.sh",
        "post-tool.sh", "post-tool-backup.sh", "prompt-guard.sh",
        "auto-skill-router.sh", "notify-telegram.sh", "task-completed.sh",
        "stop-summary.sh", "session-end.sh", "post-compact.sh",
    ]
    results = []
    for script in expected:
        path = os.path.join(hooks_dir, script)
        if not os.path.exists(path):
            results.append((script, "RED", "missing"))
        elif not os.access(path, os.X_OK):
            results.append((script, "YELLOW", "not executable"))
        else:
            results.append((script, "GREEN", "ok"))
    return results


def check_logs(date_str):
    """Check logging health."""
    results = []
    log_dir = os.path.join(PRISM_DIR, "logs")

    # Action log
    action_file = os.path.join(log_dir, "actions", f"{date_str}.jsonl")
    if os.path.exists(action_file):
        lines = sum(1 for _ in open(action_file))
        results.append(("Action log", "GREEN", f"{lines} entries"))
    else:
        results.append(("Action log", "YELLOW", "no entries yet today"))

    # Session events
    events_file = os.path.join(log_dir, "session-events.jsonl")
    if os.path.exists(events_file):
        size = os.path.getsize(events_file)
        results.append(("Session events", "GREEN", f"{size / 1024:.1f} KB"))
    else:
        results.append(("Session events", "RED", "missing"))

    # Conversation exports
    year_month = date_str[:7]
    convos_dir = os.path.join(log_dir, "conversations", year_month)
    if os.path.isdir(convos_dir):
        count = len([f for f in os.listdir(convos_dir) if f.endswith(".md")])
        results.append(("Conversations", "GREEN", f"{count} this month"))
    else:
        results.append(("Conversations", "YELLOW", "no exports this month"))

    # Session summaries
    sessions_dir = os.path.join(log_dir, "sessions", year_month)
    if os.path.isdir(sessions_dir):
        md_count = len([f for f in os.listdir(sessions_dir) if f.endswith(".md")])
        results.append(("Session logs", "GREEN", f"{md_count} this month"))
    else:
        results.append(("Session logs", "YELLOW", "none this month"))

    return results


def check_rules():
    """Check rules are present."""
    rules_dir = os.path.join(CLAUDE_DIR, "rules")
    results = []
    if not os.path.isdir(rules_dir):
        return [("Rules dir", "RED", "missing")]
    rules = [f for f in os.listdir(rules_dir) if f.endswith(".md")]
    if len(rules) >= 5:
        results.append(("Rules", "GREEN", f"{len(rules)} loaded"))
    elif len(rules) > 0:
        results.append(("Rules", "YELLOW", f"only {len(rules)} found"))
    else:
        results.append(("Rules", "RED", "none found"))
    return results


def check_good_examples():
    """Count files in good-examples subfolders."""
    examples_dir = os.path.join(PRISM_DIR, "skills", "good-examples")
    results = []
    if not os.path.isdir(examples_dir):
        return [("Good examples", "YELLOW", "directory not found")]
    total = 0
    for subdir in sorted(os.listdir(examples_dir)):
        subpath = os.path.join(examples_dir, subdir)
        if os.path.isdir(subpath):
            count = len([f for f in os.listdir(subpath) if not f.startswith(".")])
            total += count
    if total > 0:
        results.append(("Good examples", "GREEN", f"{total} examples"))
    else:
        results.append(("Good examples", "YELLOW", "empty"))
    return results


def check_stale_files():
    """Check if critical files are older than 7 days."""
    results = []
    now = datetime.now()
    threshold = timedelta(days=7)

    critical_files = {
        "CONTEXT.md": os.path.join(PRISM_DIR, "CONTEXT.md"),
        "INDEX.md": os.path.join(PRISM_DIR, "INDEX.md"),
    }

    # Add memory bank files
    mb_dir = os.path.join(PRISM_DIR, "memory-bank")
    if os.path.isdir(mb_dir):
        for f in os.listdir(mb_dir):
            if f.endswith(".md"):
                critical_files[f"memory-bank/{f}"] = os.path.join(mb_dir, f)

    for name, path in critical_files.items():
        if not os.path.exists(path):
            results.append((name, "RED", "missing"))
            continue
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        age = now - mtime
        if age > threshold:
            results.append((name, "YELLOW", f"{age.days}d old"))
        else:
            results.append((name, "GREEN", f"{age.days}d old"))

    return results


def check_disk():
    """Show total size of logs directory."""
    log_dir = os.path.join(PRISM_DIR, "logs")
    total = 0
    for dirpath, dirnames, filenames in os.walk(log_dir):
        for f in filenames:
            total += os.path.getsize(os.path.join(dirpath, f))
    return total


def generate_report(date_str):
    """Generate the health check report."""
    hooks = check_hooks()
    logs = check_logs(date_str)
    rules = check_rules()
    examples = check_good_examples()
    stale = check_stale_files()
    disk_bytes = check_disk()

    # Count statuses
    all_checks = hooks + logs + rules + examples + stale
    green = sum(1 for _, s, _ in all_checks if s == "GREEN")
    yellow = sum(1 for _, s, _ in all_checks if s == "YELLOW")
    red = sum(1 for _, s, _ in all_checks if s == "RED")

    if red > 0:
        overall = "RED"
    elif yellow > 2:
        overall = "YELLOW"
    else:
        overall = "GREEN"

    def table(items):
        lines = ["| Component | Status | Detail |", "|-----------|--------|--------|"]
        for name, status, detail in items:
            emoji = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}[status]
            lines.append(f"| {name} | {emoji} {status} | {detail} |")
        return "\n".join(lines)

    report = f"""# PRISM Health Check — {date_str}

**Overall: {overall}** ({green} green, {yellow} yellow, {red} red)

## Hooks
{table(hooks)}

## Logging
{table(logs)}

## Rules
{table(rules)}

## Good Examples
{table(examples)}

## Stale Files
{table(stale)}

## Disk Usage
- Logs directory: {disk_bytes / (1024*1024):.1f} MB

---
*Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}*
"""

    reports_dir = os.path.join(PRISM_DIR, "logs", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, f"health-{date_str}.md")

    with open(report_file, "w") as f:
        f.write(report)

    print(f"Health check written to {report_file}")
    return report_file


if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    generate_report(date_str)
