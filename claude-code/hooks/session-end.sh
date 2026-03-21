#!/bin/bash
# Claude Mainframe — Session End Hook v3
# Calls parse-session.py v3 which produces:
#   1. logs/sessions/YYYY-MM/session-{id}.jsonl  (machine-readable)
#   2. logs/sessions/YYYY-MM/session-{id}.md     (human-readable)
# No debug dumps. Errors go to hook-errors.log.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi

MAINFRAME_DIR="$HOME/Documents/Claude/Mainframe"
SCRIPT="$MAINFRAME_DIR/scripts/parse-session.py"

# Run the Python parser if it exists
if [ -f "$SCRIPT" ]; then
    echo "$INPUT" | python3 "$SCRIPT" 2>> "$MAINFRAME_DIR/logs/hook-errors.log"
else
    # Fallback: log the event only
    TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    SID="unknown"
    if command -v jq &>/dev/null && [ -n "$INPUT" ]; then
        SID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
    fi
    printf '{"ts":"%s","event":"end","sid":"%s","error":"parse-session.py not found"}\n' \
        "$TS" "$SID" \
        >> "$MAINFRAME_DIR/logs/session-events.jsonl"
fi

exit 0
