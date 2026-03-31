#!/usr/bin/env python3
"""
Claude PRISM — Session Metrics Extractor
Extracts real metrics from session/action logs for meta-article generation.

Usage:
    python3 extract-session-metrics.py                    # Latest session today
    python3 extract-session-metrics.py SESSION_ID         # Specific session
    python3 extract-session-metrics.py --date 2026-03-30  # All sessions on date
    python3 extract-session-metrics.py --monthly          # Monthly cumulative stats

Output: JSON to stdout (consumed by meta-article skill)
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter

PRISM_DIR = os.path.expanduser("~/Documents/Claude/PRISM")
LOG_DIR = os.path.join(PRISM_DIR, "logs")

# Claude pricing (per million tokens)
PRICING = {
    "opus_input": 15.0,
    "opus_output": 75.0,
    "sonnet_input": 3.0,
    "sonnet_output": 15.0,
}

# Average tokens per tool call (empirical from [Methodology Partner] sessions)
AVG_TOKENS_PER_TOOL_CALL = {
    "Read": 800,
    "Write": 1200,
    "Edit": 600,
    "Bash": 500,
    "Grep": 400,
    "Glob": 200,
    "WebFetch": 1500,
    "WebSearch": 800,
    "Agent": 3000,
    "default": 500,
}

# Human time estimates per task type (hours)
HUMAN_TIME = {
    "research": 2.0,
    "writing": 4.0,
    "formatting": 1.0,
    "seo": 0.5,
    "qa": 1.5,
    "publishing": 0.5,
}

HUMAN_RATES = {
    "us_marketer": 35.0,
    "trained_va": 8.0,
}


def load_actions_for_session(session_id=None, date_str=None):
    """Load actions filtered by session ID or date."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    actions_file = os.path.join(LOG_DIR, "actions", f"{date_str}.jsonl")
    if not os.path.exists(actions_file):
        return []

    actions = []
    with open(actions_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                action = json.loads(line)
                if session_id and action.get("sid", "") != session_id:
                    continue
                actions.append(action)
            except json.JSONDecodeError:
                continue
    return actions


def load_session_summary(session_id):
    """Load session summary JSONL for a specific session."""
    # Search recent months
    now = datetime.now()
    for months_back in range(3):
        d = now - timedelta(days=months_back * 30)
        year_month = d.strftime("%Y-%m")
        sessions_dir = os.path.join(LOG_DIR, "sessions", year_month)
        if not os.path.isdir(sessions_dir):
            continue
        for f in os.listdir(sessions_dir):
            if f.endswith(".jsonl") and session_id[:8] in f:
                filepath = os.path.join(sessions_dir, f)
                try:
                    with open(filepath, "r") as fh:
                        return json.loads(fh.readline().strip())
                except (json.JSONDecodeError, Exception):
                    continue
    return None


def find_latest_session(date_str=None):
    """Find the most recent session ID from session events."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    events_file = os.path.join(LOG_DIR, "session-events.jsonl")
    if not os.path.exists(events_file):
        return None

    latest = None
    with open(events_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("ts", "").startswith(date_str) and event.get("event") == "start":
                    latest = event.get("sid")
            except json.JSONDecodeError:
                continue
    return latest


def estimate_tokens(actions):
    """Estimate total tokens from action log entries."""
    total_input = 0
    total_output = 0
    for action in actions:
        tool = action.get("tool", "default")
        tokens = AVG_TOKENS_PER_TOOL_CALL.get(tool, AVG_TOKENS_PER_TOOL_CALL["default"])
        # Input is roughly 60% of token usage, output 40%
        total_input += int(tokens * 0.6)
        total_output += int(tokens * 0.4)
    return total_input, total_output


def calculate_cost(input_tokens, output_tokens, model="opus"):
    """Calculate cost from token counts."""
    if model == "opus":
        return (input_tokens / 1_000_000 * PRICING["opus_input"]) + \
               (output_tokens / 1_000_000 * PRICING["opus_output"])
    else:
        return (input_tokens / 1_000_000 * PRICING["sonnet_input"]) + \
               (output_tokens / 1_000_000 * PRICING["sonnet_output"])


def extract_metrics(session_id=None, date_str=None):
    """Extract comprehensive metrics for meta-article generation."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # If no session_id specified, load ALL actions for the date
    actions = load_actions_for_session(session_id, date_str)
    summary = load_session_summary(session_id) if session_id else None

    # Tool usage breakdown
    tool_counts = Counter()
    files_read = set()
    files_written = set()
    files_edited = set()
    web_fetches = []
    searches = []
    agents_spawned = 0

    for action in actions:
        tool = action.get("tool", "unknown")
        tool_counts[tool] += 1
        target = action.get("target", "") or action.get("file", "")

        if tool == "Read" and target:
            files_read.add(target)
        elif tool == "Write" and target:
            files_written.add(target)
        elif tool == "Edit" and target:
            files_edited.add(target)
        elif tool == "WebFetch" and target:
            web_fetches.append(target)
        elif tool in ("Grep", "Glob"):
            searches.append(target)
        elif tool == "Agent":
            agents_spawned += 1

    # Token and cost estimates
    input_tokens, output_tokens = estimate_tokens(actions)
    total_tokens = input_tokens + output_tokens
    agent_cost = calculate_cost(input_tokens, output_tokens)

    # Time estimate (from timestamps)
    agent_minutes = 0
    if actions:
        try:
            first_ts = actions[0].get("ts", "")
            last_ts = actions[-1].get("ts", "")
            if first_ts and last_ts:
                t1 = datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
                t2 = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
                agent_minutes = max(1, int((t2 - t1).total_seconds() / 60))
        except (ValueError, TypeError):
            agent_minutes = len(actions)  # rough fallback: 1 min per tool call

    # Human comparison
    human_hours = sum(HUMAN_TIME.values())
    human_cost_marketer = human_hours * HUMAN_RATES["us_marketer"]
    human_cost_va = human_hours * HUMAN_RATES["trained_va"]

    # Session metadata
    task_description = ""
    category = "general"
    files_created_list = []
    files_modified_list = []

    if summary:
        task_description = summary.get("task_description", "")
        category = summary.get("category", "general")
        files_created_list = summary.get("files_created", [])
        files_modified_list = summary.get("files_modified", [])

    metrics = {
        "session_id": session_id or "unknown",
        "date": date_str,
        "task_description": task_description,
        "category": category,
        "tool_calls": {
            "total": len(actions),
            "breakdown": dict(tool_counts.most_common()),
        },
        "files": {
            "read": list(files_read),
            "written": list(files_written),
            "edited": list(files_edited),
            "created": files_created_list,
            "modified": files_modified_list,
            "total_unique": len(files_read | files_written | files_edited),
        },
        "web": {
            "fetches": web_fetches,
            "searches": searches,
            "agents_spawned": agents_spawned,
        },
        "tokens": {
            "estimated_input": input_tokens,
            "estimated_output": output_tokens,
            "estimated_total": total_tokens,
        },
        "cost": {
            "agent_cost_usd": round(agent_cost, 2),
            "agent_minutes": agent_minutes,
            "human_hours_equivalent": human_hours,
            "human_cost_marketer_usd": round(human_cost_marketer, 2),
            "human_cost_va_usd": round(human_cost_va, 2),
            "savings_vs_marketer_pct": round((1 - agent_cost / human_cost_marketer) * 100, 1) if human_cost_marketer > 0 else 0,
        },
        "effort_table": [
            {"task": "Research", "agent_min": max(1, agent_minutes // 4), "human_hrs": HUMAN_TIME["research"], "agent_cost": round(agent_cost * 0.25, 2), "human_cost": round(HUMAN_TIME["research"] * HUMAN_RATES["us_marketer"], 2)},
            {"task": "Writing", "agent_min": max(1, agent_minutes // 3), "human_hrs": HUMAN_TIME["writing"], "agent_cost": round(agent_cost * 0.35, 2), "human_cost": round(HUMAN_TIME["writing"] * HUMAN_RATES["us_marketer"], 2)},
            {"task": "Formatting", "agent_min": max(1, agent_minutes // 6), "human_hrs": HUMAN_TIME["formatting"], "agent_cost": round(agent_cost * 0.10, 2), "human_cost": round(HUMAN_TIME["formatting"] * HUMAN_RATES["us_marketer"], 2)},
            {"task": "SEO Optimization", "agent_min": max(1, agent_minutes // 8), "human_hrs": HUMAN_TIME["seo"], "agent_cost": round(agent_cost * 0.10, 2), "human_cost": round(HUMAN_TIME["seo"] * HUMAN_RATES["us_marketer"], 2)},
            {"task": "QA", "agent_min": max(1, agent_minutes // 5), "human_hrs": HUMAN_TIME["qa"], "agent_cost": round(agent_cost * 0.15, 2), "human_cost": round(HUMAN_TIME["qa"] * HUMAN_RATES["us_marketer"], 2)},
            {"task": "Publishing Prep", "agent_min": max(1, agent_minutes // 10), "human_hrs": HUMAN_TIME["publishing"], "agent_cost": round(agent_cost * 0.05, 2), "human_cost": round(HUMAN_TIME["publishing"] * HUMAN_RATES["us_marketer"], 2)},
        ],
    }

    return metrics


def monthly_cumulative(year_month=None):
    """Generate cumulative stats for the month."""
    if year_month is None:
        year_month = datetime.now().strftime("%Y-%m")

    sessions_dir = os.path.join(LOG_DIR, "sessions", year_month)
    if not os.path.isdir(sessions_dir):
        return {"error": "No sessions found for " + year_month}

    total_sessions = 0
    total_tool_calls = 0
    total_files_created = 0
    total_files_modified = 0
    categories = Counter()
    total_tokens = 0

    for f in os.listdir(sessions_dir):
        if not f.endswith(".jsonl"):
            continue
        filepath = os.path.join(sessions_dir, f)
        try:
            with open(filepath, "r") as fh:
                data = json.loads(fh.readline().strip())
                total_sessions += 1
                total_tool_calls += data.get("total_tool_uses", 0)
                total_files_created += len(data.get("files_created", []))
                total_files_modified += len(data.get("files_modified", []))
                categories[data.get("category", "general")] += 1
        except (json.JSONDecodeError, Exception):
            continue

    # Estimate monthly tokens and cost from action logs
    year, month = year_month.split("-")
    for day in range(1, 32):
        try:
            date_str = f"{year}-{month}-{day:02d}"
            actions_file = os.path.join(LOG_DIR, "actions", f"{date_str}.jsonl")
            if os.path.exists(actions_file):
                with open(actions_file) as af:
                    day_actions = sum(1 for _ in af)
                total_tokens += day_actions * 600  # avg tokens per action
        except (ValueError, Exception):
            continue

    monthly_cost = (total_tokens / 1_000_000) * ((PRICING["opus_input"] + PRICING["opus_output"]) / 2)

    return {
        "month": year_month,
        "total_sessions": total_sessions,
        "total_tool_calls": total_tool_calls,
        "total_files_created": total_files_created,
        "total_files_modified": total_files_modified,
        "categories": dict(categories.most_common()),
        "estimated_tokens": total_tokens,
        "estimated_cost_usd": round(monthly_cost, 2),
        "[google-doc-id]": round(total_sessions * 1.5, 1),
        "estimated_human_cost_usd": round(total_sessions * 1.5 * HUMAN_RATES["us_marketer"], 2),
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--monthly":
            year_month = sys.argv[2] if len(sys.argv) > 2 else None
            result = monthly_cumulative(year_month)
        elif sys.argv[1] == "--date":
            date_str = sys.argv[2] if len(sys.argv) > 2 else None
            result = extract_metrics(date_str=date_str)
        else:
            result = extract_metrics(session_id=sys.argv[1])
    else:
        result = extract_metrics()

    print(json.dumps(result, indent=2))
