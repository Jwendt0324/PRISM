#!/bin/bash
# Claude PRISM — PreToolUse Security Guard v1.0
# Blocks truly destructive operations even in [google-doc-id] mode.
# Returns exit code 2 to BLOCK, exit code 0 to ALLOW.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

if ! command -v jq &>/dev/null; then
    exit 0
fi

TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
[ -z "$TOOL" ] && exit 0

# ─── BASH COMMAND GUARD ───
if [ "$TOOL" = "Bash" ]; then
    CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

    # Block rm -rf (recursive + force) on home directory or root
    # Must have BOTH -r and target a dangerous path. Single file rm is allowed.
    if echo "$CMD" | grep -qE 'rm\s+-[a-zA-Z]*r[a-zA-Z]*\s' && echo "$CMD" | grep -qE '(\/\s*$|~\/?\s*$|\/Users\/[a-zA-Z]+\/?\s*$|\$HOME\/?\s*$|\/Users\/\s)'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked recursive rm on home/root directory. This is a destructive operation."}'
        exit 2
    fi

    # Block rm -rf / (root filesystem)
    if echo "$CMD" | grep -qE 'rm\s+-[a-zA-Z]*r[a-zA-Z]*\s+/\s' ; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked rm -rf /. This would delete everything."}'
        exit 2
    fi

    # Block git push --force to main/master (catches --force, --force-with-lease, -f in any position)
    if echo "$CMD" | grep -qE 'git\s+push' && echo "$CMD" | grep -qE '(--force|-f\b)' && echo "$CMD" | grep -qE '\b(main|master)\b'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked force push to main/master. Use a feature branch instead."}'
        exit 2
    fi

    # Block git reset --hard on main/master
    if echo "$CMD" | grep -qE 'git\s+reset\s+--hard' && echo "$CMD" | grep -qE '(main|master|origin)'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked git reset --hard on main/master. This discards all uncommitted work."}'
        exit 2
    fi

    # Block DROP TABLE / DROP DATABASE
    if echo "$CMD" | grep -qiE '(DROP\s+TABLE|DROP\s+DATABASE|TRUNCATE\s+TABLE)'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked destructive database operation."}'
        exit 2
    fi

    # Block modifications to SSH keys
    if echo "$CMD" | grep -qE '(rm|mv|cp|cat\s*>)\s+.*\.ssh/'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked modification to SSH keys."}'
        exit 2
    fi
fi

# ─── WRITE/EDIT FILE GUARD ───
if [ "$TOOL" = "Write" ] || [ "$TOOL" = "Edit" ]; then
    FILEPATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

    # Block writes to credentials and secrets
    if echo "$FILEPATH" | grep -qE '(\.env$|\.env\.|credentials|secrets|\.ssh/|\.aws/|\.gnupg/)'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked write to credentials/secrets file. Store secrets in environment variables, not files."}'
        exit 2
    fi

    # Block writes to Claude settings (prevent self-modification of permissions)
    if echo "$FILEPATH" | grep -qE '\.claude/settings\.json$|\.claude/settings\.local\.json$'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked write to Claude settings. Modify settings manually to prevent permission escalation."}'
        exit 2
    fi

    # Block writes to system files
    if echo "$FILEPATH" | grep -qE '^/(etc|usr|bin|sbin|System|Library)/'; then
        echo '{"decision":"block","reason":"PRISM GUARD: Blocked write to system directory."}'
        exit 2
    fi
fi

# All checks passed — allow the operation
exit 0
