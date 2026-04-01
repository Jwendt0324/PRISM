#!/bin/bash
# Claude PRISM — StopFailure Hook v1.0
# Handles API errors gracefully — logs the failure and provides context for recovery.
# Triggered on: rate_limit, authentication_failed, billing_error, server_error, etc.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

if ! command -v jq &>/dev/null; then
    exit 0
fi

ERROR_TYPE=$(echo "$INPUT" | jq -r '.error // "unknown"' 2>/dev/null)
ERROR_DETAILS=$(echo "$INPUT" | jq -r '.error_details // "no details"' 2>/dev/null)
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRISM_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PRISM_DIR/logs/actions"
LOG_FILE="$LOG_DIR/$DATE.jsonl"

# Log the failure (use jq for safe JSON encoding)
mkdir -p "$LOG_DIR"
if command -v jq &>/dev/null; then
    jq -n --arg e "$ERROR_TYPE" --arg d "$ERROR_DETAILS" --arg t "$TIMESTAMP" \
        '{"event":"stop_failure","error":$e,"details":$d,"timestamp":$t}' >> "$LOG_FILE"
else
    # Fallback: basic sanitization
    SAFE_ERROR=$(printf '%s' "$ERROR_TYPE" | tr '"' "'")
    SAFE_DETAILS=$(printf '%s' "$ERROR_DETAILS" | tr '"' "'" | tr '\n' ' ')
    echo "{\"event\":\"stop_failure\",\"error\":\"$SAFE_ERROR\",\"details\":\"$SAFE_DETAILS\",\"timestamp\":\"$TIMESTAMP\"}" >> "$LOG_FILE"
fi

# Provide context back to Claude for recovery
SAFE_TYPE=$(printf '%s' "$ERROR_TYPE" | tr '"' "'")
SAFE_DET=$(printf '%s' "$ERROR_DETAILS" | tr '"' "'" | tr '\n' ' ')
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "StopFailure",
    "additionalContext": "API error occurred: $SAFE_TYPE. Details: $SAFE_DET. The error has been logged. If rate_limited, wait briefly and retry. If authentication_failed, check API key. If billing_error, notify [Your Name]."
  }
}
EOF

exit 0
