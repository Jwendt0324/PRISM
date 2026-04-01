#!/bin/bash
# Claude PRISM — Session End Hook v4
# Produces three outputs:
#   1. logs/sessions/YYYY-MM/session-{id}.jsonl  (machine-readable)
#   2. logs/sessions/YYYY-MM/session-{id}.md     (human-readable summary)
#   3. logs/conversations/YYYY-MM/conversation-{id}.md  (full readable conversation)
# Errors go to hook-errors.log.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi

# Clean up tab title enforcer background process
[ -f "$HOME/.claude_tab_title_pid" ] && kill "$(cat "$HOME/.claude_tab_title_pid")" 2>/dev/null
rm -f "$HOME/.claude_tab_title_pid" "$HOME/.claude_tab_title"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRISM_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PARSER="$PRISM_DIR/scripts/parse-session.py"
EXPORTER="$PRISM_DIR/scripts/export-conversation.py"

# Extract session ID for the conversation export
SID="unknown"
if command -v jq &>/dev/null && [ -n "$INPUT" ]; then
    SID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
fi

# Run the session parser (structured summary)
if [ -f "$PARSER" ] && [ -n "$INPUT" ]; then
    echo "$INPUT" | python3 "$PARSER" 2>> "$PRISM_DIR/logs/hook-errors.log"
else
    TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    printf '{"ts":"%s","event":"end","sid":"%s","error":"parse-session.py not found"}\n' \
        "$TS" "$SID" \
        >> "$PRISM_DIR/logs/session-events.jsonl"
fi

# Run the conversation exporter (full readable conversation)
if [ -f "$EXPORTER" ] && [ "$SID" != "unknown" ]; then
    python3 "$EXPORTER" "$SID" 2>> "$PRISM_DIR/logs/hook-errors.log" &
fi

exit 0
