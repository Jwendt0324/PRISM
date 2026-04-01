#!/usr/bin/env python3
"""
Claude PRISM — Conversation Exporter v1.0
Converts Claude Code JSONL transcripts into readable markdown conversations.

Usage:
    python3 export-conversation.py <session_id>
    python3 export-conversation.py --all          # Export all unprocessed sessions
    python3 export-conversation.py --latest        # Export most recent session

Output: logs/conversations/YYYY-MM/conversation-{session_id_short}.md
"""

import json
import os
import sys
import glob
from datetime import datetime, timezone
from pathlib import Path

PRISM_DIR = os.path.expanduser("~/Documents/Claude/PRISM")
CLAUDE_PROJECTS = os.path.expanduser("~/.claude/projects/-Users-[your-username]")
OUTPUT_DIR = os.path.join(PRISM_DIR, "logs", "conversations")


def find_transcript(session_id):
    """Find a transcript file by session ID."""
    direct = os.path.join(CLAUDE_PROJECTS, f"{session_id}.jsonl")
    if os.path.exists(direct):
        return direct
    # Search other project dirs
    for path in glob.glob(os.path.expanduser(f"~/.claude/projects/*/{session_id}.jsonl")):
        return path
    return None


def find_all_transcripts():
    """Find all transcript JSONL files."""
    transcripts = []
    for path in glob.glob(os.path.join(CLAUDE_PROJECTS, "*.jsonl")):
        if "/subagents/" in path:
            continue
        transcripts.append(path)
    # Also check other project dirs
    for path in glob.glob(os.path.expanduser("~/.claude/projects/-sessions-*/*.jsonl")):
        if "/subagents/" in path:
            continue
        transcripts.append(path)
    return sorted(transcripts, key=os.path.getmtime, reverse=True)


def extract_text_from_content(content):
    """Extract readable text from message content (string or list of blocks)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text = block.get("text", "").strip()
                    if text:
                        texts.append(text)
                elif block.get("type") == "tool_use":
                    name = block.get("name", "unknown")
                    inp = block.get("input", {})
                    # Compact tool call description
                    if name == "Bash":
                        cmd = inp.get("command", "")[:200]
                        texts.append(f"*[Tool: Bash]* `{cmd}`")
                    elif name in ("Read", "Write"):
                        fp = inp.get("file_path", "")
                        texts.append(f"*[Tool: {name}]* `{fp}`")
                    elif name == "Edit":
                        fp = inp.get("file_path", "")
                        texts.append(f"*[Tool: Edit]* `{fp}`")
                    elif name == "Agent":
                        desc = inp.get("description", "")
                        texts.append(f"*[Tool: Agent]* {desc}")
                    elif name == "Grep":
                        pattern = inp.get("pattern", "")[:100]
                        texts.append(f"*[Tool: Grep]* `{pattern}`")
                    elif name == "Glob":
                        pattern = inp.get("pattern", "")
                        texts.append(f"*[Tool: Glob]* `{pattern}`")
                    elif name.startswith("mcp__"):
                        short = name.split("__")[-1]
                        texts.append(f"*[Tool: {short}]*")
                    else:
                        texts.append(f"*[Tool: {name}]*")
                elif block.get("type") == "tool_result":
                    # Skip tool results in the readable output (too verbose)
                    pass
        return "\n".join(texts)
    return ""


def is_noise_entry(entry):
    """Check if an entry is system noise (progress, result, etc)."""
    etype = entry.get("type", "")
    if etype in ("progress", "result"):
        return True
    if etype == "user":
        content = entry.get("message", {}).get("content", "")
        text = extract_text_from_content(content)
        if not text or len(text.strip()) < 2:
            return True
        # System reminders injected by Claude Code
        if text.strip().startswith("<system-reminder>"):
            return True
    return False


def convert_transcript(transcript_path):
    """Convert a JSONL transcript to readable markdown."""
    entries = []
    session_id = "unknown"

    try:
        fh = open(transcript_path, "r", encoding="utf-8", errors="replace")
    except (OSError, IOError) as e:
        return None, "unknown"

    with fh as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(entry)
                if entry.get("sessionId"):
                    session_id = entry["sessionId"]
            except json.JSONDecodeError:
                continue

    if not entries:
        return None, None

    # Build conversation
    conversation = []
    message_count = {"user": 0, "assistant": 0}

    for entry in entries:
        if is_noise_entry(entry):
            continue

        etype = entry.get("type", "")

        if etype == "user":
            msg = entry.get("message", {})
            content = msg.get("content", "")
            text = extract_text_from_content(content)
            if text and not text.startswith("<system-reminder>"):
                # Clean up pasted content markers
                if len(text) > 5000:
                    text = text[:5000] + "\n\n*[... truncated — full text in transcript]*"
                conversation.append(("[Your Name]", text))
                message_count["user"] += 1

        elif etype == "assistant":
            msg = entry.get("message", {})
            content = msg.get("content", [])
            text = extract_text_from_content(content)
            if text:
                # Don't truncate Claude's responses as aggressively
                if len(text) > 10000:
                    text = text[:10000] + "\n\n*[... truncated — full text in transcript]*"
                conversation.append(("Claude", text))
                message_count["assistant"] += 1

    if not conversation:
        return None, None

    # Get file timestamp
    file_mtime = os.path.getmtime(transcript_path)
    file_date = datetime.fromtimestamp(file_mtime, tz=timezone.utc)

    # Build markdown
    short_id = session_id[:8] if len(session_id) > 8 else session_id

    # Try to get first user prompt as title
    first_prompt = ""
    for speaker, text in conversation:
        if speaker == "[Your Name]":
            first_prompt = text[:200].replace("\n", " ").strip()
            break

    # Auto-detect confidential conversations
    # Confidential signals — use phrases specific enough to avoid false positives
    # A mentor's name alone triggers on every operational conversation mentioning [Your Mentor/Advisor]
    confidential_signals = [
        "power dynamic", "condescending", "mentor relationship",
        "equity split", "compensation dispute", "losing hope",
        "new llc", "separate business", "don't tell",
        "between us", "confidential", "off the record",
        "not fair", "frustrated with mentor", "upset with mentor",
        "frustrated with partner", "upset with partner",
    ]
    all_text_lower = " ".join(t.lower() for _, t in conversation)
    is_confidential = any(signal in all_text_lower for signal in confidential_signals)
    classification = "CONFIDENTIAL" if is_confidential else "OPERATIONAL"

    md = f"""---
date: {file_date.strftime("%Y-%m-%dT%H:%M:%SZ")}
session_id: {session_id}
classification: {classification}
messages: {message_count['user']} user / {message_count['assistant']} assistant
transcript: {transcript_path}
---

# Conversation — {short_id}

**Classification:** {classification}
**First prompt:** {first_prompt}

---

"""

    for speaker, text in conversation:
        if speaker == "[Your Name]":
            md += f"## [Your Name]\n\n{text}\n\n---\n\n"
        else:
            md += f"## Claude\n\n{text}\n\n---\n\n"

    return md, {
        "session_id": session_id,
        "short_id": short_id,
        "date": file_date,
        "user_messages": message_count["user"],
        "assistant_messages": message_count["assistant"],
        "total_messages": message_count["user"] + message_count["assistant"],
    }


def export_session(session_id):
    """Export a single session."""
    transcript = find_transcript(session_id)
    if not transcript:
        print(f"No transcript found for session {session_id}")
        return None

    md, meta = convert_transcript(transcript)
    if not md:
        print(f"No conversation content found in {transcript}")
        return None

    # Write to output
    month_dir = os.path.join(OUTPUT_DIR, meta["date"].strftime("%Y-%m"))
    os.makedirs(month_dir, exist_ok=True)

    output_path = os.path.join(month_dir, f"conversation-{meta['short_id']}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"Exported: {output_path} ({size_kb:.0f} KB, {meta['total_messages']} messages)")
    return output_path


def export_all_unprocessed():
    """Export all sessions that don't have conversation files yet."""
    transcripts = find_all_transcripts()
    exported = 0

    for transcript_path in transcripts:
        # Get session ID from filename
        filename = os.path.basename(transcript_path)
        session_id = filename.replace(".jsonl", "")

        # Check if already exported
        short_id = session_id[:8]
        existing = glob.glob(os.path.join(OUTPUT_DIR, "*/conversation-" + short_id + ".md"))
        if existing:
            continue

        # Skip tiny files (< 1KB = trivial sessions)
        if os.path.getsize(transcript_path) < 1024:
            continue

        result = export_session(session_id)
        if result:
            exported += 1

    print(f"\nExported {exported} new conversations")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 export-conversation.py <session_id>")
        print("  python3 export-conversation.py --all")
        print("  python3 export-conversation.py --latest")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--all":
        export_all_unprocessed()
    elif arg == "--latest":
        transcripts = find_all_transcripts()
        if transcripts:
            session_id = os.path.basename(transcripts[0]).replace(".jsonl", "")
            export_session(session_id)
        else:
            print("No transcripts found")
    else:
        export_session(arg)


if __name__ == "__main__":
    main()
