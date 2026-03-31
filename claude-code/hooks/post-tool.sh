#!/bin/bash
# Claude PRISM — Post Tool Use Hook v3
# Writes one JSONL line per tool call to logs/actions/YYYY-MM-DD.jsonl
# Captures action metadata WITHOUT content (no tool_response, no file contents)
# Target: <100ms execution time, ~150 bytes per event

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date -u +"%Y-%m-%d")
LOG_DIR="$HOME/Documents/Claude/PRISM/logs/actions"
mkdir -p "$LOG_DIR"

# Use jq for fast JSON parsing
if ! command -v jq &>/dev/null; then
    exit 0
fi

TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
SID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)

[ -z "$TOOL" ] && exit 0

# Extract target based on tool type — metadata only, never content
case "$TOOL" in
    Read|Write)
        TARGET=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
        ;;
    Edit)
        TARGET=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
        ;;
    Bash)
        TARGET=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null | head -c 200)
        ;;
    Grep)
        PATTERN=$(echo "$INPUT" | jq -r '.tool_input.pattern // empty' 2>/dev/null | head -c 100)
        GPATH=$(echo "$INPUT" | jq -r '.tool_input.path // empty' 2>/dev/null)
        TARGET="pattern=${PATTERN} path=${GPATH}"
        ;;
    Glob)
        PATTERN=$(echo "$INPUT" | jq -r '.tool_input.pattern // empty' 2>/dev/null)
        GPATH=$(echo "$INPUT" | jq -r '.tool_input.path // empty' 2>/dev/null)
        TARGET="pattern=${PATTERN} path=${GPATH}"
        ;;
    WebFetch)
        TARGET=$(echo "$INPUT" | jq -r '.tool_input.url // empty' 2>/dev/null | head -c 200)
        ;;
    WebSearch)
        TARGET=$(echo "$INPUT" | jq -r '.tool_input.query // empty' 2>/dev/null | head -c 200)
        ;;
    Agent)
        TARGET=$(echo "$INPUT" | jq -r '.tool_input.description // empty' 2>/dev/null | head -c 200)
        ;;
    mcp__*)
        # MCP tools — capture tool name only, inputs may contain sensitive data
        TARGET=""
        ;;
    *)
        TARGET=""
        ;;
esac

# Sanitize target for JSON — escape quotes, backslashes, remove newlines
SAFE_TARGET=$(printf '%s' "$TARGET" | sed 's/\\/\\\\/g' | tr '"' "'" | tr '\n' ' ' | tr '\r' ' ')

# Write single JSONL line — compact, no content
printf '{"ts":"%s","sid":"%s","tool":"%s","target":"%s","cwd":"%s"}\n' \
    "$TS" "$SID" "$TOOL" "$SAFE_TARGET" "$CWD" \
    >> "$LOG_DIR/$TODAY.jsonl"

exit 0
