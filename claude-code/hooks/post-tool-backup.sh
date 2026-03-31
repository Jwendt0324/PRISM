#!/bin/bash
# Claude PRISM — PostToolUse Auto-Backup v1.0
# After any Write or Edit to a file >1KB, creates a .bak copy.
# Keeps last 3 backups per file to prevent disk bloat.
# Runs AFTER the tool completes (PostToolUse), so the backup is of the NEW version.

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

if ! command -v jq &>/dev/null; then
    exit 0
fi

TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# Only backup on Write or Edit
if [ "$TOOL" != "Write" ] && [ "$TOOL" != "Edit" ]; then
    exit 0
fi

FILEPATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[ -z "$FILEPATH" ] && exit 0
[ ! -f "$FILEPATH" ] && exit 0

# Skip small files (<1KB) — not worth backing up
FILESIZE=$(wc -c < "$FILEPATH" 2>/dev/null | tr -d ' ')
[ "$FILESIZE" -lt 1024 ] 2>/dev/null && exit 0

# Skip files in logs/, .git/, node_modules/, __pycache__/
if echo "$FILEPATH" | grep -qE '(\/logs\/|\/\.git\/|\/node_modules\/|\/__pycache__\/)'; then
    exit 0
fi

# Skip backup files themselves
if echo "$FILEPATH" | grep -qE '\.(bak|bak\.[0-9]+)$'; then
    exit 0
fi

# Create backup directory alongside the file
BACKUP_DIR="$(dirname "$FILEPATH")/.backups"
mkdir -p "$BACKUP_DIR" 2>/dev/null

BASENAME=$(basename "$FILEPATH")
TS=$(date +"%Y%m%d-%H%M%S")

# Copy current file as backup (this runs AFTER the edit, so we're backing up the new version)
# Note: for true "previous version" backup, we'd need PreToolUse. But having the current
# version backed up still protects against the NEXT edit going wrong.
# Only clean up old backups if new backup succeeds
if cp "$FILEPATH" "$BACKUP_DIR/${BASENAME}.${TS}.bak" 2>/dev/null; then
    # Keep only last 3 backups per file to prevent disk bloat
    ls -t "$BACKUP_DIR/${BASENAME}".*.bak 2>/dev/null | tail -n +4 | xargs rm -f 2>/dev/null
fi

exit 0
