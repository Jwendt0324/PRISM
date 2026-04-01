#!/bin/bash
# ============================================================
# CLAUDE PRISM — INSTALLER
# Wires PRISM into Claude Code so it runs automatically.
#
# What this does:
# 1. Installs CLAUDE.md as global instructions (loaded every session)
# 2. Installs hook configuration into Claude Code settings
# 3. Replaces {{PRISM_PATH}} placeholders with actual install path
# 4. Verifies everything is connected
#
# Run this once: bash claude-code/install.sh
# ============================================================

set -e

# Auto-detect PRISM root from script location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRISM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
SETTINGS="$CLAUDE_DIR/settings.json"

echo "=========================================="
echo "  CLAUDE PRISM — INSTALLER"
echo "=========================================="
echo ""
echo "  PRISM directory: $PRISM_DIR"
echo ""

# ---- Step 1: Ensure directories exist ----
mkdir -p "$CLAUDE_DIR"
mkdir -p "$PRISM_DIR/logs/sessions" "$PRISM_DIR/logs/actions" "$PRISM_DIR/logs/reports"
echo "[1/5] Directories ready"

# ---- Step 2: Install CLAUDE.md ----
PRISM_CLAUDE="$PRISM_DIR/claude-code/CLAUDE.md"
if [ ! -f "$PRISM_CLAUDE" ]; then
    echo "[2/5] ERROR: $PRISM_CLAUDE not found"
    exit 1
fi

if [ -f "$CLAUDE_MD" ]; then
    BACKUP="$CLAUDE_DIR/CLAUDE.md.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$CLAUDE_MD" "$BACKUP"
    echo "[2/5] Backed up existing CLAUDE.md to $(basename "$BACKUP")"

    if grep -q "CLAUDE PRISM" "$CLAUDE_MD" 2>/dev/null; then
        echo "      PRISM already present — replacing with latest version..."
        cp "$PRISM_CLAUDE" "$CLAUDE_MD"
    else
        # Prepend PRISM instructions, preserve existing content
        cat "$PRISM_CLAUDE" > "$CLAUDE_MD.tmp"
        echo "" >> "$CLAUDE_MD.tmp"
        echo "---" >> "$CLAUDE_MD.tmp"
        echo "" >> "$CLAUDE_MD.tmp"
        echo "# PREVIOUS INSTRUCTIONS (preserved from before PRISM install)" >> "$CLAUDE_MD.tmp"
        echo "" >> "$CLAUDE_MD.tmp"
        cat "$BACKUP" >> "$CLAUDE_MD.tmp"
        mv "$CLAUDE_MD.tmp" "$CLAUDE_MD"
        echo "      PRISM instructions prepended (old instructions preserved)"
    fi
else
    cp "$PRISM_CLAUDE" "$CLAUDE_MD"
    echo "[2/5] Installed CLAUDE.md (fresh install)"
fi

# Replace {{PRISM_PATH}} in CLAUDE.md
sed -i '' "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_MD" 2>/dev/null || \
sed -i "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_MD"
echo "      Replaced {{PRISM_PATH}} with: $PRISM_DIR"

# ---- Step 3: Install hooks into settings.json ----
PRISM_SETTINGS="$PRISM_DIR/claude-code/settings.json"
if [ ! -f "$PRISM_SETTINGS" ]; then
    echo "[3/5] ERROR: $PRISM_SETTINGS not found"
    exit 1
fi

# Create a resolved copy of settings.json with actual paths
RESOLVED_SETTINGS="/tmp/prism-settings-resolved.json"
sed "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$PRISM_SETTINGS" > "$RESOLVED_SETTINGS"

if [ -f "$SETTINGS" ]; then
    SETTINGS_BACKUP="$CLAUDE_DIR/settings.json.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$SETTINGS" "$SETTINGS_BACKUP"
    echo "[3/5] Backed up existing settings.json to $(basename "$SETTINGS_BACKUP")"

    if command -v jq &> /dev/null; then
        # Deep merge: existing settings + PRISM hooks
        # PRISM hooks override existing hook config for the same events
        jq -s '.[0] * .[1]' "$SETTINGS_BACKUP" "$RESOLVED_SETTINGS" > "$SETTINGS"
        echo "      Hooks merged into existing settings"
    else
        echo "      WARNING: jq not installed — installing jq is recommended."
        echo "      Copying PRISM settings directly (your existing settings are backed up)."
        cp "$RESOLVED_SETTINGS" "$SETTINGS"
    fi
else
    cp "$RESOLVED_SETTINGS" "$SETTINGS"
    echo "[3/5] Installed settings.json (fresh install)"
fi

rm -f "$RESOLVED_SETTINGS"

# ---- Step 4: Ensure auto-update hook is registered ----
if [ -f "$PRISM_DIR/.personal/auto-update-enabled" ]; then
    AUTO_UPDATE_CMD="/bin/bash $PRISM_DIR/claude-code/hooks/auto-update.sh"
    if command -v jq &> /dev/null; then
        # Check if auto-update is already in any SessionStart hook
        if ! grep -q "auto-update.sh" "$SETTINGS" 2>/dev/null; then
            # Add auto-update hook to the first SessionStart entry's hooks array
            jq --arg cmd "$AUTO_UPDATE_CMD" \
                '.hooks.SessionStart[0].hooks += [{"type": "command", "command": $cmd, "timeout": 10}]' \
                "$SETTINGS" > "$SETTINGS.tmp" && mv "$SETTINGS.tmp" "$SETTINGS"
            echo "[4/5] Auto-update hook registered"
        else
            echo "[4/5] Auto-update hook already registered"
        fi
    else
        echo "[4/5] Skipped auto-update registration (jq required)"
    fi
else
    echo "[4/5] Auto-updates not enabled (run setup.sh first to opt in)"
fi

# ---- Step 5: Make hook scripts executable ----
chmod +x "$PRISM_DIR/claude-code/hooks/"*.sh 2>/dev/null
echo "[5/5] Hook scripts marked executable"

# ---- Verify ----
echo ""
echo "Verifying installation..."
echo ""

PASS=true

if [ -f "$CLAUDE_MD" ] && grep -q "CLAUDE PRISM" "$CLAUDE_MD"; then
    echo "  ✓ CLAUDE.md installed with PRISM instructions"
else
    echo "  ✗ CLAUDE.md missing PRISM instructions"
    PASS=false
fi

# Check that {{PRISM_PATH}} was replaced (no remaining placeholders)
if grep -q '{{PRISM_PATH}}' "$CLAUDE_MD" 2>/dev/null; then
    echo "  ✗ CLAUDE.md still has unresolved {{PRISM_PATH}} placeholders"
    PASS=false
else
    echo "  ✓ CLAUDE.md paths resolved"
fi

if grep -q '{{PRISM_PATH}}' "$SETTINGS" 2>/dev/null; then
    echo "  ✗ settings.json still has unresolved {{PRISM_PATH}} placeholders"
    PASS=false
else
    echo "  ✓ settings.json paths resolved"
fi

for EVENT in SessionStart PreToolUse PostToolUse UserPromptSubmit Stop SessionEnd StopFailure PostCompact; do
    if [ -f "$SETTINGS" ] && grep -q "$EVENT" "$SETTINGS"; then
        echo "  ✓ $EVENT hook configured"
    else
        echo "  ✗ $EVENT hook missing"
        PASS=false
    fi
done

for HOOK in session-start.sh session-end.sh post-tool.sh pre-tool-guard.sh prompt-submit.sh stop-summary.sh auto-update.sh; do
    if [ -x "$PRISM_DIR/claude-code/hooks/$HOOK" ]; then
        echo "  ✓ $HOOK is executable"
    else
        echo "  ✗ $HOOK missing or not executable"
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
    echo "  • SOPs are auto-matched to your tasks"
    echo "  • Sessions are auto-logged when they end"
    echo "  • Tool usage is tracked for pattern detection"
    echo ""
    echo "  Next time you open Claude Code, PRISM is already running."
else
    echo "=========================================="
    echo "  INSTALL INCOMPLETE — check errors above"
    echo "=========================================="
fi
