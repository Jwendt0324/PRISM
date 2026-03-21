#!/usr/bin/env python3
"""
Claude Mainframe — Session Transcript Parser v3
Produces two outputs per session:
  1. logs/sessions/YYYY-MM/session-{session_id}.jsonl  (machine-readable audit trail)
  2. logs/sessions/YYYY-MM/session-{session_id}.md     (human-readable summary)

Key changes from v2:
  - Dual output (JSONL + markdown)
  - Enriches from daily action logs (logs/actions/YYYY-MM-DD.jsonl)
  - Filters raw terminal output, task notifications, login banners
  - Skips trivial sessions (under 10 messages, no file changes)
  - NEVER writes placeholder stubs for "What Was Learned"
  - Logs session end event to session-events.jsonl
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

MAINFRAME_DIR = os.path.expanduser("~/Documents/Claude/Mainframe")


def parse_hook_input():
    """Read and parse the hook JSON from stdin."""
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        return json.loads(raw)
    except (json.JSONDecodeError, Exception):
        return {}


def is_noise(text):
    """Check if a user prompt is noise (terminal output, task notifications, etc.)."""
    if not text:
        return True
    noise_patterns = [
        "Last login:",
        "jackwendt@",
        "<task-notification>",
        "Claude Code v",
        "Opus 4",
        "Sonnet 4",
        "Claude Max",
        "<system-reminder>",
    ]
    stripped = text.strip()
    for pattern in noise_patterns:
        if stripped.startswith(pattern) or pattern in stripped[:100]:
            return True
    # Skip very short non-questions
    if len(stripped) < 3:
        return True
    return False


def parse_transcript(transcript_path):
    """Parse a JSONL transcript file and extract structured data."""
    if not transcript_path or not os.path.exists(transcript_path):
        return None

    entries = []
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception:
        return None

    if not entries:
        return None

    # Extract user prompts (filtered)
    user_prompts_raw = []
    user_prompts_clean = []
    for entry in entries:
        if entry.get("type") == "user":
            msg = entry.get("message", {})
            content = msg.get("content", "")
            texts = []
            if isinstance(content, str) and content.strip():
                texts.append(content.strip())
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "").strip()
                        if text:
                            texts.append(text)
            for t in texts:
                user_prompts_raw.append(t[:500])
                if not is_noise(t):
                    user_prompts_clean.append(t[:500])

    # Extract tool uses from assistant messages
    tool_uses = []
    for entry in entries:
        if entry.get("type") == "assistant":
            msg = entry.get("message", {})
            content = msg.get("content", [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tool_name = block.get("name", "unknown")
                        tool_input = block.get("input", {})

                        tool_info = {"name": tool_name}

                        if tool_name in ("Write", "Read"):
                            tool_info["file"] = tool_input.get("file_path", "")
                        elif tool_name == "Edit":
                            tool_info["file"] = tool_input.get("file_path", "")
                        elif tool_name == "Bash":
                            cmd = tool_input.get("command", "")
                            tool_info["command"] = cmd[:200]
                        elif tool_name == "Grep":
                            tool_info["target"] = f"pattern={tool_input.get('pattern', '')[:100]} path={tool_input.get('path', '')}"
                        elif tool_name == "Glob":
                            tool_info["target"] = f"pattern={tool_input.get('pattern', '')} path={tool_input.get('path', '')}"
                        elif tool_name == "WebFetch":
                            tool_info["target"] = tool_input.get("url", "")[:200]
                        elif tool_name == "WebSearch":
                            tool_info["target"] = tool_input.get("query", "")[:200]
                        elif tool_name == "Agent":
                            tool_info["target"] = tool_input.get("description", "")[:200]

                        tool_uses.append(tool_info)

    # Extract assistant text responses (first meaningful one for summary)
    assistant_texts = []
    for entry in entries:
        if entry.get("type") == "assistant":
            msg = entry.get("message", {})
            content = msg.get("content", [])
            if isinstance(content, str):
                assistant_texts.append(content[:1000])
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "").strip()
                        if text:
                            assistant_texts.append(text[:1000])

    # Analyze
    tool_counts = Counter(t["name"] for t in tool_uses)
    files_created = sorted(set(t["file"] for t in tool_uses if t.get("file") and t["name"] == "Write"))
    files_modified = sorted(set(t["file"] for t in tool_uses if t.get("file") and t["name"] == "Edit"))
    files_read = sorted(set(t["file"] for t in tool_uses if t.get("file") and t["name"] == "Read"))
    bash_commands = [t["command"] for t in tool_uses if t.get("command") and t["name"] == "Bash"]
    web_searches = [t["target"] for t in tool_uses if t.get("target") and t["name"] == "WebSearch"]
    web_fetches = [t["target"] for t in tool_uses if t.get("target") and t["name"] == "WebFetch"]
    agent_tasks = [t["target"] for t in tool_uses if t.get("target") and t["name"] == "Agent"]

    # Build task description from first CLEAN user prompt (not noise)
    task_description = user_prompts_clean[0] if user_prompts_clean else "[No user prompt captured]"

    # First meaningful assistant response
    first_response = ""
    for text in assistant_texts:
        if len(text) > 50 and not text.startswith("MAINFRAME"):
            first_response = text[:500]
            break

    return {
        "user_prompts_raw": user_prompts_raw,
        "user_prompts_clean": user_prompts_clean,
        "tool_counts": dict(tool_counts),
        "total_tool_uses": len(tool_uses),
        "files_created": files_created[:50],
        "files_modified": files_modified[:50],
        "files_read": files_read[:50],
        "bash_commands": bash_commands[:30],
        "web_searches": web_searches[:20],
        "web_fetches": web_fetches[:20],
        "agent_tasks": agent_tasks[:20],
        "task_description": task_description,
        "first_response": first_response,
        "message_count": len(entries),
        "user_message_count": len(user_prompts_raw),
        "user_message_count_clean": len(user_prompts_clean),
        "assistant_response_count": len(assistant_texts),
    }


def determine_category(data):
    """Guess the session category based on files and content."""
    all_files = (data.get("files_created", []) +
                 data.get("files_modified", []) +
                 data.get("files_read", []))
    all_files_str = " ".join(all_files).lower()
    task_str = data.get("task_description", "").lower()

    if "content-pipeline" in all_files_str or "article" in task_str or "transcript" in task_str:
        return "client-work"
    if "client" in all_files_str or "client" in task_str:
        return "client-work"
    if "team-ops" in all_files_str or "onboard" in task_str:
        return "business-ops"
    if "memory-bank" in all_files_str or "gmail" in task_str:
        return "business-ops"
    if "sop" in all_files_str or "sop" in task_str:
        return "business-ops"
    if "parts-agent" in all_files_str or "scheduling-agent" in all_files_str:
        return "dev"
    if ".py" in all_files_str or ".js" in all_files_str or ".sh" in all_files_str:
        return "dev"
    if "mainframe" in task_str or "hook" in task_str or "log" in task_str:
        return "system"
    return "general"


def is_trivial_session(data):
    """Check if a session is too trivial to log."""
    if not data:
        return True
    # Under 10 messages AND no files created or modified
    if (data["user_message_count"] < 3 and
        data["total_tool_uses"] < 5 and
        len(data["files_created"]) == 0 and
        len(data["files_modified"]) == 0):
        return True
    return False


def enrich_from_actions_log(session_id):
    """Pull additional action data from the daily JSONL actions log."""
    actions_dir = os.path.join(MAINFRAME_DIR, "logs", "actions")
    if not os.path.isdir(actions_dir):
        return []

    actions = []
    # Check today's and yesterday's logs (session might span midnight)
    for days_back in range(2):
        from datetime import timedelta
        check_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        log_file = os.path.join(actions_dir, check_date.strftime("%Y-%m-%d") + ".jsonl")
        if not os.path.exists(log_file):
            continue
        try:
            with open(log_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        if entry.get("sid") == session_id:
                            actions.append(entry)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            continue

    return actions


def write_session_jsonl(session_id, hook_data, transcript_data, actions, category):
    """Write machine-readable session data as JSONL."""
    now = datetime.now(timezone.utc)
    log_dir = os.path.join(MAINFRAME_DIR, "logs", "sessions", now.strftime("%Y-%m"))
    os.makedirs(log_dir, exist_ok=True)

    # Use short session_id for filename (first 8 chars)
    short_id = session_id[:8] if len(session_id) > 8 else session_id
    log_file = os.path.join(log_dir, f"session-{short_id}.jsonl")

    session_data = {
        "session_id": session_id,
        "start_ts": actions[0]["ts"] if actions else now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cwd": hook_data.get("cwd", "unknown"),
        "category": category,
        "user_messages": transcript_data["user_message_count"],
        "user_messages_clean": transcript_data["user_message_count_clean"],
        "total_tool_uses": transcript_data["total_tool_uses"],
        "tool_counts": transcript_data["tool_counts"],
        "files_created": transcript_data["files_created"],
        "files_modified": transcript_data["files_modified"],
        "files_read": transcript_data["files_read"][:30],
        "bash_commands": transcript_data["bash_commands"][:20],
        "web_searches": transcript_data["web_searches"][:10],
        "agent_tasks": transcript_data["agent_tasks"][:10],
        "task_description": transcript_data["task_description"][:300],
        "transcript_path": hook_data.get("transcript_path", ""),
        "needs_learnings": True,
    }

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(session_data, indent=None, ensure_ascii=False) + "\n")
        # Also write each action as a separate line for forensic trace
        for action in actions:
            f.write(json.dumps(action, indent=None, ensure_ascii=False) + "\n")

    return log_file


def write_session_markdown(session_id, hook_data, transcript_data, category):
    """Write human-readable session summary."""
    now = datetime.now(timezone.utc)
    date_slug = now.strftime("%Y%m%d-%H%M%S")
    log_dir = os.path.join(MAINFRAME_DIR, "logs", "sessions", now.strftime("%Y-%m"))
    os.makedirs(log_dir, exist_ok=True)

    short_id = session_id[:8] if len(session_id) > 8 else session_id
    log_file = os.path.join(log_dir, f"session-{short_id}.md")

    timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    cwd = hook_data.get("cwd", "unknown")

    tool_counts = transcript_data["tool_counts"]
    tool_summary = ", ".join(f"{name}: {count}" for name, count in
                              sorted(tool_counts.items(), key=lambda x: -x[1]))
    if not tool_summary:
        tool_summary = "None"

    files_created_list = "\n".join(f"- {f}" for f in transcript_data["files_created"]) or "None"
    files_modified_list = "\n".join(f"- {f}" for f in transcript_data["files_modified"]) or "None"
    files_read_list = "\n".join(f"- {f}" for f in transcript_data["files_read"][:30]) or "None"
    bash_list = "\n".join(f"- `{cmd}`" for cmd in transcript_data["bash_commands"][:15]) or "None"

    # Clean user prompts for display
    prompts_section = ""
    for i, prompt in enumerate(transcript_data["user_prompts_clean"][:8], 1):
        clean_prompt = prompt.replace("\n", " ").strip()
        if len(clean_prompt) > 300:
            clean_prompt = clean_prompt[:300] + "..."
        prompts_section += f"{i}. {clean_prompt}\n"
    if not prompts_section:
        prompts_section = "[No user prompts captured]\n"

    # Web activity
    web_section = ""
    if transcript_data["web_searches"]:
        web_section += "\n## Web Searches\n"
        for q in transcript_data["web_searches"][:10]:
            web_section += f"- {q}\n"
    if transcript_data["web_fetches"]:
        web_section += "\n## URLs Fetched\n"
        for u in transcript_data["web_fetches"][:10]:
            web_section += f"- {u}\n"

    # Agent sub-tasks
    agent_section = ""
    if transcript_data["agent_tasks"]:
        agent_section = "\n## Sub-Agent Tasks\n"
        for a in transcript_data["agent_tasks"][:10]:
            agent_section += f"- {a}\n"

    content = f"""---
date: {timestamp}
session_id: {session_id}
cwd: {cwd}
category: {category}
message_count: {transcript_data['message_count']}
user_messages: {transcript_data['user_message_count_clean']}
total_tool_uses: {transcript_data['total_tool_uses']}
needs_learnings: true
version: 3.0
---

# Session Log — {short_id}

## Task Summary
{transcript_data['task_description'][:500]}

## User Prompts
{prompts_section}
## Tool Usage
{tool_summary}

Total tool calls: {transcript_data['total_tool_uses']}

## Files Created
{files_created_list}

## Files Modified
{files_modified_list}

## Files Read
{files_read_list}

## Commands Run
{bash_list}
{web_section}{agent_section}
## Session Stats
- Messages: {transcript_data['message_count']}
- User prompts: {transcript_data['user_message_count_clean']} (filtered from {transcript_data['user_message_count']} raw)
- Tool calls: {transcript_data['total_tool_uses']}
- Working directory: {cwd}
- Transcript: {hook_data.get('transcript_path', 'N/A')}

## What Was Learned
**[NEEDS LEARNINGS]** — Claude should fill this in before session ends.
Minimum 2 actionable learnings in Discovery/Insight/Action format.
If Claude didn't fill this in, a human should review the transcript and extract learnings.

## Related SOPs
**[NEEDS REVIEW]** — List SOPs consulted or that should be updated.
"""

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(content)

    return log_file


def log_session_event(session_id, cwd, transcript_data):
    """Write session end event to session-events.jsonl."""
    now = datetime.now(timezone.utc)
    events_log = os.path.join(MAINFRAME_DIR, "logs", "session-events.jsonl")

    event = {
        "ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "event": "end",
        "sid": session_id,
        "cwd": cwd,
        "tools": transcript_data["total_tool_uses"] if transcript_data else 0,
        "msgs": transcript_data["message_count"] if transcript_data else 0,
        "user_msgs": transcript_data["user_message_count_clean"] if transcript_data else 0,
        "files_created": len(transcript_data["files_created"]) if transcript_data else 0,
        "files_modified": len(transcript_data["files_modified"]) if transcript_data else 0,
    }

    with open(events_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main():
    hook_data = parse_hook_input()
    session_id = hook_data.get("session_id", "unknown")
    cwd = hook_data.get("cwd", "unknown")

    # Parse transcript
    transcript_path = hook_data.get("transcript_path", "")
    transcript_data = parse_transcript(transcript_path) if transcript_path else None

    # Always log the session event
    log_session_event(session_id, cwd, transcript_data)

    # Skip trivial sessions
    if is_trivial_session(transcript_data):
        return

    category = determine_category(transcript_data)

    # Enrich from daily actions log
    actions = enrich_from_actions_log(session_id)

    # Write both outputs
    write_session_jsonl(session_id, hook_data, transcript_data, actions, category)
    write_session_markdown(session_id, hook_data, transcript_data, category)


if __name__ == "__main__":
    main()
