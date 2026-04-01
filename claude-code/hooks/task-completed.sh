#!/bin/bash
# Claude PRISM — TaskCompleted Hook v1.0
# Appends completed tasks to a running daily task log.
# The weekly retrospective reads this for a complete picture of what got done.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

if ! command -v jq &>/dev/null; then
    exit 0
fi

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date +"%Y-%m-%d")
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRISM_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PRISM_DIR/logs"
TASK_LOG="$LOG_DIR/tasks/$TODAY.jsonl"
mkdir -p "$LOG_DIR/tasks"

SID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
TASK_ID=$(echo "$INPUT" | jq -r '.task_id // "unknown"' 2>/dev/null)
STATUS=$(echo "$INPUT" | jq -r '.status // "completed"' 2>/dev/null)

printf '{"ts":"%s","sid":"%s","task_id":"%s","status":"%s"}\n' \
    "$TS" "$SID" "$TASK_ID" "$STATUS" \
    >> "$TASK_LOG"

exit 0
