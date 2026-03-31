#!/bin/bash
# Claude PRISM — PreToolUse Naming Convention Enforcer v1.0
# Auto-corrects file naming for content files written by Claude.
# Uses updatedInput to fix naming without blocking execution.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

if ! command -v jq &>/dev/null; then
    exit 0
fi

TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
[ "$TOOL" != "Write" ] && exit 0

FILEPATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[ -z "$FILEPATH" ] && exit 0

# Only enforce on content directories
if ! echo "$FILEPATH" | grep -qE '(content-audit|articles|drafts|reports)/'; then
    exit 0
fi

BASENAME=$(basename "$FILEPATH")
DIRNAME=$(dirname "$FILEPATH")

# Check for spaces in filename (should be hyphens)
if echo "$BASENAME" | grep -q ' '; then
    FIXED=$(echo "$BASENAME" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    FIXED_PATH="$DIRNAME/$FIXED"

    jq -n --arg path "$FIXED_PATH" --arg orig "$FILEPATH" '{
        hookSpecificOutput: {
            hookEventName: "PreToolUse",
            permissionDecision: "allow",
            permissionDecisionReason: ("Filename corrected: spaces replaced with hyphens. " + $orig + " → " + $path),
            updatedInput: {
                file_path: $path
            }
        }
    }'
    exit 0
fi

# Check for uppercase in content filenames (should be lowercase)
if echo "$BASENAME" | grep -qE '[A-Z]' && echo "$BASENAME" | grep -qE '\.(md|txt|html)$'; then
    FIXED=$(echo "$BASENAME" | tr '[:upper:]' '[:lower:]')
    FIXED_PATH="$DIRNAME/$FIXED"

    jq -n --arg path "$FIXED_PATH" --arg orig "$FILEPATH" '{
        hookSpecificOutput: {
            hookEventName: "PreToolUse",
            permissionDecision: "allow",
            permissionDecisionReason: ("Filename lowercased: " + $orig + " → " + $path),
            updatedInput: {
                file_path: $path
            }
        }
    }'
    exit 0
fi

# All checks passed
exit 0
