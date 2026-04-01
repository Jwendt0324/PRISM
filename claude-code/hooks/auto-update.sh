#!/bin/bash
# Claude PRISM — Auto-Update Hook
# Runs on SessionStart. Quietly pulls latest PRISM improvements.
# Controlled by .personal/auto-update-enabled flag.
# Total timeout: 5 seconds. Silent when nothing to update.

# Determine PRISM directory (this script lives in claude-code/hooks/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRISM_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
FLAG_FILE="$PRISM_DIR/.personal/auto-update-enabled"
UPDATE_LOG="$PRISM_DIR/.personal/update-log.txt"

# Exit silently if auto-update not enabled
[ -f "$FLAG_FILE" ] || exit 0

# Exit silently if not a git repo
[ -d "$PRISM_DIR/.git" ] || exit 0

# Exit silently if no remote configured
cd "$PRISM_DIR" || exit 0
git remote get-url origin &>/dev/null || exit 0

# Check internet connectivity (1 second timeout)
if ! curl -s --connect-timeout 1 --max-time 2 https://github.com -o /dev/null 2>/dev/null; then
    exit 0
fi

# Fetch latest from origin (quiet, 3 second timeout)
if ! timeout 3 git fetch origin main --quiet 2>/dev/null; then
    exit 0
fi

# Check if local is behind remote
LOCAL=$(git rev-parse HEAD 2>/dev/null)
REMOTE=$(git rev-parse origin/main 2>/dev/null)

# If up to date, exit silently
[ "$LOCAL" = "$REMOTE" ] && exit 0

# Check if local is actually behind (not diverged)
MERGE_BASE=$(git merge-base HEAD origin/main 2>/dev/null)
[ "$LOCAL" != "$MERGE_BASE" ] && exit 0  # Diverged — don't auto-update

# Count how many commits behind
BEHIND_COUNT=$(git rev-list HEAD..origin/main --count 2>/dev/null)

# Stash any local changes (safety)
STASHED=false
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    git stash push -m "prism-auto-update-$(date +%Y%m%d-%H%M%S)" --quiet 2>/dev/null
    STASHED=true
fi

# Pull the updates
if timeout 3 git pull origin main --quiet 2>/dev/null; then
    # Get summary of what changed
    FILES_CHANGED=$(git diff --stat "$LOCAL"..HEAD --name-only 2>/dev/null | wc -l | tr -d ' ')

    # Log the update
    mkdir -p "$(dirname "$UPDATE_LOG")"
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Updated: $BEHIND_COUNT commits, $FILES_CHANGED files changed ($LOCAL -> $(git rev-parse --short HEAD))" >> "$UPDATE_LOG"

    # Pop stash if we stashed
    if $STASHED; then
        git stash pop --quiet 2>/dev/null || true
    fi

    # Output brief message (visible to Claude/user)
    echo "PRISM updated: $FILES_CHANGED files changed"
else
    # Pull failed — restore stash and exit silently
    if $STASHED; then
        git stash pop --quiet 2>/dev/null || true
    fi
    exit 0
fi
