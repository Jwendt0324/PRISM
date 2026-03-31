#!/bin/bash
# PostCompact Hook — Verify critical context preserved after compaction
# Added: 2026-03-30 (Iteration 6)
# Trigger: PostCompact event (fires after context window compaction)

LOG_DIR="$HOME/Documents/Claude/PRISM/logs/actions"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).jsonl"
mkdir -p "$LOG_DIR"

# Read session ID from stdin if available
INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
SID="unknown"
if command -v jq &>/dev/null && [ -n "$INPUT" ]; then
    SID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
fi

# Log the compaction event
echo "{\"event\":\"PostCompact\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"session\":\"$SID\"}" >> "$LOG_FILE"

# Inject reminder to Claude about what must be preserved
cat << 'EOF'
COMPACTION OCCURRED — Verify these items are still in your context:
- List of files modified this session
- Client names and client-specific decisions
- Current task and its status
- Human gates or approvals given
- File paths referenced for current work
If any are missing, re-read the relevant files before continuing.
EOF
