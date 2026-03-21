#!/bin/bash
# Claude Mainframe — Session Start Hook v3
# Logs session start event to session-events.jsonl (structured, no debug dumps)

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
MAINFRAME_DIR="$HOME/Documents/Claude/Mainframe"
LOG_DIR="$MAINFRAME_DIR/logs"
mkdir -p "$LOG_DIR/actions" "$LOG_DIR/sessions/$(date +%Y-%m)"

if command -v jq &>/dev/null; then
    SID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
    CWD=$(echo "$INPUT" | jq -r '.cwd // "unknown"' 2>/dev/null)
else
    SID="unknown"
    CWD="unknown"
fi

# Write structured JSONL event
printf '{"ts":"%s","event":"start","sid":"%s","cwd":"%s"}\n' \
    "$TS" "$SID" "$CWD" \
    >> "$LOG_DIR/session-events.jsonl"

exit 0
