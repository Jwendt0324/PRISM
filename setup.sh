#!/bin/bash
# Mainframe Setup — One-time onboarding for new users
# Usage: ./setup.sh

set -e

MAINFRAME_DIR="$(cd "$(dirname "$0")" && pwd)"
PERSONAL_DIR="$MAINFRAME_DIR/.personal"
CLAUDE_DIR="$HOME/.claude"

echo ""
echo "========================================"
echo "  CLAUDE MAINFRAME — SETUP"
echo "========================================"
echo ""

# Step 1: Create personal directory
if [ -d "$PERSONAL_DIR" ]; then
    echo "[OK] Personal directory already exists at .personal/"
else
    echo "[+] Creating personal directory..."
    mkdir -p "$PERSONAL_DIR/memory-bank"
    echo "[OK] Created .personal/ and .personal/memory-bank/"
fi

# Step 2: Copy context template if no CONTEXT.md exists
if [ -f "$PERSONAL_DIR/CONTEXT.md" ]; then
    echo "[OK] CONTEXT.md already exists — skipping template copy"
else
    cp "$MAINFRAME_DIR/CONTEXT-TEMPLATE.md" "$PERSONAL_DIR/CONTEXT.md"
    echo "[OK] Created .personal/CONTEXT.md from template"
fi

# Step 3: Create/update CLAUDE.md in ~/.claude/
echo ""
echo "Setting up CLAUDE.md..."

if [ -f "$CLAUDE_DIR/CLAUDE.md" ]; then
    echo ""
    echo "[!] You already have a CLAUDE.md at ~/.claude/CLAUDE.md"
    echo "    Options:"
    echo "    1) Replace it with the Mainframe CLAUDE.md (backup saved)"
    echo "    2) Append Mainframe instructions to existing CLAUDE.md"
    echo "    3) Skip — I'll set it up manually"
    echo ""
    read -p "    Choice [1/2/3]: " claude_choice

    case $claude_choice in
        1)
            cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.backup.$(date +%Y%m%d)"
            cp "$MAINFRAME_DIR/CLAUDE-TEMPLATE.md" "$CLAUDE_DIR/CLAUDE.md"
            # Replace placeholder with actual path
            sed -i '' "s|{{MAINFRAME_PATH}}|$MAINFRAME_DIR|g" "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null || \
            sed -i "s|{{MAINFRAME_PATH}}|$MAINFRAME_DIR|g" "$CLAUDE_DIR/CLAUDE.md"
            echo "[OK] CLAUDE.md replaced (backup saved)"
            ;;
        2)
            echo "" >> "$CLAUDE_DIR/CLAUDE.md"
            echo "# --- MAINFRAME INSTRUCTIONS (appended by setup) ---" >> "$CLAUDE_DIR/CLAUDE.md"
            echo "" >> "$CLAUDE_DIR/CLAUDE.md"
            cat "$MAINFRAME_DIR/CLAUDE-TEMPLATE.md" >> "$CLAUDE_DIR/CLAUDE.md"
            sed -i '' "s|{{MAINFRAME_PATH}}|$MAINFRAME_DIR|g" "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null || \
            sed -i "s|{{MAINFRAME_PATH}}|$MAINFRAME_DIR|g" "$CLAUDE_DIR/CLAUDE.md"
            echo "[OK] Mainframe instructions appended to existing CLAUDE.md"
            ;;
        3)
            echo "[SKIP] Manual setup — copy CLAUDE-TEMPLATE.md to ~/.claude/CLAUDE.md"
            ;;
    esac
else
    mkdir -p "$CLAUDE_DIR"
    cp "$MAINFRAME_DIR/CLAUDE-TEMPLATE.md" "$CLAUDE_DIR/CLAUDE.md"
    sed -i '' "s|{{MAINFRAME_PATH}}|$MAINFRAME_DIR|g" "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null || \
    sed -i "s|{{MAINFRAME_PATH}}|$MAINFRAME_DIR|g" "$CLAUDE_DIR/CLAUDE.md"
    echo "[OK] Created ~/.claude/CLAUDE.md"
fi

# Step 4: Create logs directory
mkdir -p "$MAINFRAME_DIR/logs/sessions" "$MAINFRAME_DIR/logs/actions" "$MAINFRAME_DIR/logs/reports"
echo "[OK] Logs directories ready"

# Step 5: Summary
echo ""
echo "========================================"
echo "  SETUP COMPLETE"
echo "========================================"
echo ""
echo "  Mainframe: $MAINFRAME_DIR"
echo "  Personal:  $PERSONAL_DIR"
echo "  CLAUDE.md: $CLAUDE_DIR/CLAUDE.md"
echo ""
echo "  NEXT STEP: Run the Identity Scan"
echo ""
echo "  Open Claude Code in any directory and say:"
echo ""
echo "    \"Run the identity scan\""
echo ""
echo "  This will scan your computer, email, drive, and"
echo "  other sources to build your personal context."
echo "  You choose which sources to include."
echo ""
echo "  Or to skip the scan and fill in context manually:"
echo "    Edit $PERSONAL_DIR/CONTEXT.md"
echo ""
echo "========================================"
