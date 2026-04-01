#!/bin/bash
# Claude PRISM — Notification Hook v1.0
# Sends Claude Code notifications to Telegram when long tasks complete.
# Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment or config.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

# Load Telegram config
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRISM_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG_FILE="$PRISM_DIR/config/telegram.json"
if [ ! -f "$CONFIG_FILE" ]; then
    exit 0  # Telegram not configured — silently skip
fi

if ! command -v jq &>/dev/null; then
    exit 0
fi

BOT_TOKEN=$(jq -r '.bot_token // empty' "$CONFIG_FILE" 2>/dev/null)
CHAT_ID=$(jq -r '.chat_id // empty' "$CONFIG_FILE" 2>/dev/null)

# If not configured, skip silently
[ -z "$BOT_TOKEN" ] && exit 0
[ -z "$CHAT_ID" ] && exit 0

# Extract notification message
MESSAGE=$(echo "$INPUT" | jq -r '.message // empty' 2>/dev/null)
[ -z "$MESSAGE" ] && exit 0

# Filter out noise — only forward substantive notifications
# Drop: "waiting for input", idle/ready status messages
LOWER_MSG=$(echo "$MESSAGE" | tr '[:upper:]' '[:lower:]')
case "$LOWER_MSG" in
    *"waiting for"*input*|*"waiting for"*response*|*"ready for"*|*"standing by"*|*"awaiting"*input*)
        exit 0
        ;;
esac

# Format for Telegram
TIMESTAMP=$(date +"%H:%M")
TEXT="🤖 *PRISM* ($TIMESTAMP)
$MESSAGE"

# Send via Telegram Bot API (async, don't block Claude)
# Use --data-urlencode to handle special characters in message text
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${CHAT_ID}" \
    --data-urlencode "text=${TEXT}" \
    > /dev/null 2>&1 &

exit 0
