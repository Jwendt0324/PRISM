#!/bin/bash
# ============================================================
# CLAUDE PRISM — INSTALLER
# Wires PRISM into Claude Code so it runs automatically.
#
# What this does:
# 1. Installs CLAUDE.md as global instructions (loaded every session)
# 2. Merges hook configuration into Claude Code settings
# 3. Verifies everything is connected
#
# Run this once: bash ~/Documents/Claude/PRISM/claude-code/install.sh
# ============================================================

set -e

PRISM_DIR="$HOME/Documents/Claude/PRISM"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
SETTINGS="$CLAUDE_DIR/settings.json"

echo "=========================================="
echo "  CLAUDE PRISM — INSTALLER"
echo "=========================================="
echo ""

# ---- Step 1: Ensure ~/.claude/ exists ----
mkdir -p "$CLAUDE_DIR"
echo "[1/4] ~/.claude/ directory ready"

# ---- Step 2: Install CLAUDE.md ----
if [ -f "$CLAUDE_MD" ]; then
    # Back up existing CLAUDE.md
    BACKUP="$CLAUDE_DIR/CLAUDE.md.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$CLAUDE_MD" "$BACKUP"
    echo "[2/4] Backed up existing CLAUDE.md to $(basename $BACKUP)"

    # Check if PRISM instructions already present
    if grep -q "CLAUDE PRISM" "$CLAUDE_MD" 2>/dev/null; then
        echo "      PRISM instructions already in CLAUDE.md — replacing..."
        # Remove old PRISM block and replace
        # Simple approach: prepend PRISM, then append non-PRISM content
        EXISTING_NON_PRISM=$(sed '/# CLAUDE PRISM/,/^# [^C]/{ /^# [^C]/!d; }' "$CLAUDE_MD" 2>/dev/null || cat "$CLAUDE_MD")
    fi

    # Prepend PRISM instructions to existing content
    cat "$PRISM_DIR/claude-code/CLAUDE.md" > "$CLAUDE_MD.tmp"
    echo "" >> "$CLAUDE_MD.tmp"
    echo "---" >> "$CLAUDE_MD.tmp"
    echo "" >> "$CLAUDE_MD.tmp"
    echo "# PREVIOUS INSTRUCTIONS (preserved from before PRISM install)" >> "$CLAUDE_MD.tmp"
    echo "" >> "$CLAUDE_MD.tmp"
    cat "$BACKUP" >> "$CLAUDE_MD.tmp"
    mv "$CLAUDE_MD.tmp" "$CLAUDE_MD"
    echo "      PRISM instructions prepended (old instructions preserved)"
else
    cp "$PRISM_DIR/claude-code/CLAUDE.md" "$CLAUDE_MD"
    echo "[2/4] Installed CLAUDE.md (fresh install)"
fi

# ---- Step 3: Install hooks into settings.json ----
if [ -f "$SETTINGS" ]; then
    # Back up existing settings
    SETTINGS_BACKUP="$CLAUDE_DIR/settings.json.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$SETTINGS" "$SETTINGS_BACKUP"
    echo "[3/4] Backed up existing settings.json to $(basename $SETTINGS_BACKUP)"

    # Merge hooks — use jq to combine existing settings with PRISM hooks
    if command -v jq &> /dev/null; then
        # Deep merge: existing settings + PRISM hooks
        jq -s '.[0] * .[1]' "$SETTINGS_BACKUP" "$PRISM_DIR/claude-code/settings.json" > "$SETTINGS"
        echo "      Hooks merged into existing settings"
    else
        echo "      WARNING: jq not installed. Manually merge hooks from:"
        echo "      $PRISM_DIR/claude-code/settings.json"
        echo "      into: $SETTINGS"
    fi
else
    cp "$PRISM_DIR/claude-code/settings.json" "$SETTINGS"
    echo "[3/4] Installed settings.json (fresh install)"
fi

# ---- Step 4: Verify ----
echo "[4/4] Verifying installation..."
echo ""

PASS=true

if [ -f "$CLAUDE_MD" ] && grep -q "CLAUDE PRISM" "$CLAUDE_MD"; then
    echo "  ✓ CLAUDE.md installed with PRISM instructions"
else
    echo "  ✗ CLAUDE.md missing PRISM instructions"
    PASS=false
fi

if [ -f "$SETTINGS" ] && grep -q "SessionStart" "$SETTINGS"; then
    echo "  ✓ SessionStart hook configured"
else
    echo "  ✗ SessionStart hook missing"
    PASS=false
fi

if [ -f "$SETTINGS" ] && grep -q "PostToolUse" "$SETTINGS"; then
    echo "  ✓ PostToolUse hook configured"
else
    echo "  ✗ PostToolUse hook missing"
    PASS=false
fi

if [ -f "$SETTINGS" ] && grep -q "SessionEnd" "$SETTINGS"; then
    echo "  ✓ SessionEnd hook configured"
else
    echo "  ✗ SessionEnd hook missing"
    PASS=false
fi

for HOOK in session-start.sh session-end.sh post-tool.sh; do
    if [ -x "$PRISM_DIR/claude-code/hooks/$HOOK" ]; then
        echo "  ✓ Hook script $HOOK is executable"
    else
        echo "  ✗ Hook script $HOOK missing or not executable"
        PASS=false
    fi
done

if [ -d "$PRISM_DIR/logs" ]; then
    echo "  ✓ Logs directory exists"
else
    echo "  ✗ Logs directory missing"
    PASS=false
fi

if [ -f "$PRISM_DIR/INDEX.md" ]; then
    echo "  ✓ INDEX.md exists"
else
    echo "  ✗ INDEX.md missing"
    PASS=false
fi

echo ""
if $PASS; then
    echo "=========================================="
    echo "  PRISM INSTALLED SUCCESSFULLY"
    echo "=========================================="
    echo ""
    echo "  What happens now:"
    echo "  • Every Claude Code session auto-loads PRISM instructions"
    echo "  • Every session auto-checks SOPs before starting work"
    echo "  • Every session auto-logs what was done when it ends"
    echo "  • Tool usage is tracked for pattern detection"
    echo "  • Weekly Retrospective (Cowork) processes logs into SOPs"
    echo ""
    echo "  Next time you open Claude Code, it's already running."
else
    echo "=========================================="
    echo "  INSTALL INCOMPLETE — check errors above"
    echo "=========================================="
fi
