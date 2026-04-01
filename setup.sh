#!/bin/bash
# PRISM Setup — One-time onboarding for new users
# Usage: ./setup.sh

set -e

PRISM_DIR="$(cd "$(dirname "$0")" && pwd)"
PERSONAL_DIR="$PRISM_DIR/.personal"
CLAUDE_DIR="$HOME/.claude"

echo ""
echo "========================================"
echo "  CLAUDE PRISM — SETUP"
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
    cp "$PRISM_DIR/CONTEXT-TEMPLATE.md" "$PERSONAL_DIR/CONTEXT.md"
    echo "[OK] Created .personal/CONTEXT.md from template"
fi

# Step 3: Personalize automation scripts
echo ""
echo "Personalizing your PRISM..."
echo ""

read -p "  Your name: " user_name
read -p "  Your email: " user_email
read -p "  Your company/agency name: " agency_name

if [ -n "$user_name" ]; then
    find "$PRISM_DIR/claude-code" "$PERSONAL_DIR" -type f -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.sh" 2>/dev/null | while read -r file; do
        if grep -q '{{USER_NAME}}' "$file" 2>/dev/null; then
            sed -i '' "s|{{USER_NAME}}|$user_name|g" "$file" 2>/dev/null || \
            sed -i "s|{{USER_NAME}}|$user_name|g" "$file"
        fi
    done
    echo "[OK] Set USER_NAME to: $user_name"
else
    echo "[SKIP] No name provided — {{USER_NAME}} placeholders left in place"
fi

if [ -n "$user_email" ]; then
    find "$PRISM_DIR/claude-code" "$PERSONAL_DIR" -type f -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.sh" 2>/dev/null | while read -r file; do
        if grep -q '\[your-email@your-agency.com\]' "$file" 2>/dev/null; then
            sed -i '' "s|\[your-email@your-agency.com\]|$user_email|g" "$file" 2>/dev/null || \
            sed -i "s|\[your-email@your-agency.com\]|$user_email|g" "$file"
        fi
    done
    echo "[OK] Set USER_EMAIL to: $user_email"
else
    echo "[SKIP] No email provided — [your-email@your-agency.com] placeholders left in place"
fi

if [ -n "$agency_name" ]; then
    find "$PRISM_DIR/claude-code" "$PERSONAL_DIR" -type f -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.sh" 2>/dev/null | while read -r file; do
        if grep -q '{{AGENCY_NAME}}' "$file" 2>/dev/null; then
            sed -i '' "s|{{AGENCY_NAME}}|$agency_name|g" "$file" 2>/dev/null || \
            sed -i "s|{{AGENCY_NAME}}|$agency_name|g" "$file"
        fi
    done
    echo "[OK] Set AGENCY_NAME to: $agency_name"
else
    echo "[SKIP] No company name provided — {{AGENCY_NAME}} placeholders left in place"
fi

# Step 4: Auto-update preference
echo ""
read -p "Enable auto-updates? PRISM will quietly pull the latest improvements when you start Claude Code. [Y/n] " auto_update_choice
auto_update_choice="${auto_update_choice:-Y}"

if [[ "$auto_update_choice" =~ ^[Yy]$ ]]; then
    touch "$PERSONAL_DIR/auto-update-enabled"
    echo "[OK] Auto-updates enabled"
    echo "     PRISM will run 'git pull' on session start (max 5s, silent if nothing new)"
    echo "     Your .personal/ data is never affected (gitignored)"
    echo "     To disable later: rm $PERSONAL_DIR/auto-update-enabled"
else
    echo "[SKIP] Auto-updates disabled"
    echo "       To enable later: touch $PERSONAL_DIR/auto-update-enabled"
fi

# Step 5: Create/update CLAUDE.md in ~/.claude/
echo ""
echo "Setting up CLAUDE.md..."

if [ -f "$CLAUDE_DIR/CLAUDE.md" ]; then
    echo ""
    echo "[!] You already have a CLAUDE.md at ~/.claude/CLAUDE.md"
    echo "    Options:"
    echo "    1) Replace it with the PRISM CLAUDE.md (backup saved)"
    echo "    2) Append PRISM instructions to existing CLAUDE.md"
    echo "    3) Skip — I'll set it up manually"
    echo ""
    read -p "    Choice [1/2/3]: " claude_choice

    case $claude_choice in
        1)
            cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.backup.$(date +%Y%m%d)"
            cp "$PRISM_DIR/CLAUDE-TEMPLATE.md" "$CLAUDE_DIR/CLAUDE.md"
            # Replace placeholder with actual path
            sed -i '' "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null || \
            sed -i "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_DIR/CLAUDE.md"
            echo "[OK] CLAUDE.md replaced (backup saved)"
            ;;
        2)
            echo "" >> "$CLAUDE_DIR/CLAUDE.md"
            echo "# --- PRISM INSTRUCTIONS (appended by setup) ---" >> "$CLAUDE_DIR/CLAUDE.md"
            echo "" >> "$CLAUDE_DIR/CLAUDE.md"
            cat "$PRISM_DIR/CLAUDE-TEMPLATE.md" >> "$CLAUDE_DIR/CLAUDE.md"
            sed -i '' "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null || \
            sed -i "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_DIR/CLAUDE.md"
            echo "[OK] PRISM instructions appended to existing CLAUDE.md"
            ;;
        3)
            echo "[SKIP] Manual setup — copy CLAUDE-TEMPLATE.md to ~/.claude/CLAUDE.md"
            ;;
    esac
else
    mkdir -p "$CLAUDE_DIR"
    cp "$PRISM_DIR/CLAUDE-TEMPLATE.md" "$CLAUDE_DIR/CLAUDE.md"
    sed -i '' "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null || \
    sed -i "s|{{PRISM_PATH}}|$PRISM_DIR|g" "$CLAUDE_DIR/CLAUDE.md"
    echo "[OK] Created ~/.claude/CLAUDE.md"
fi

# Step 6: Create logs directory
mkdir -p "$PRISM_DIR/logs/sessions" "$PRISM_DIR/logs/actions" "$PRISM_DIR/logs/reports"
echo "[OK] Logs directories ready"

# Step 7: Summary
echo ""
echo "========================================"
echo "  SETUP COMPLETE"
echo "========================================"
echo ""
echo "  PRISM: $PRISM_DIR"
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
