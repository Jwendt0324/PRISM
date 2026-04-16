#!/bin/bash
# PRISM Quick Install — one-command bootstrap for new apprentices
#
# Usage (paste into Terminal):
#   curl -fsSL https://raw.githubusercontent.com/Jwendt0324/PRISM/main/quick-install.sh | bash
#
# What it does:
#   1. Checks prerequisites (Claude Code CLI, git, Homebrew, jq)
#   2. Offers to install anything missing
#   3. Clones PRISM to ~/Documents/Claude/PRISM
#   4. Runs setup.sh (personalization + hook wiring)
#
# Safe to re-run: skips anything already in place.

set -e

REPO_URL="https://github.com/Jwendt0324/PRISM.git"
INSTALL_DIR="$HOME/Documents/Claude/PRISM"

echo ""
echo "=========================================="
echo "  CLAUDE PRISM — QUICK INSTALL"
echo "=========================================="
echo ""
echo "  This will install PRISM to:"
echo "    $INSTALL_DIR"
echo ""

# Step 0: OS check
OS="$(uname -s)"
if [ "$OS" != "Darwin" ] && [ "$OS" != "Linux" ]; then
    echo "[!] Unsupported OS: $OS"
    echo "    PRISM supports macOS, Linux, and WSL. For Windows, use WSL."
    exit 1
fi

# Step 1: Claude Code CLI check
if ! command -v claude &> /dev/null; then
    echo "[!] Claude Code CLI not found in PATH"
    echo ""
    echo "    Install it first from: https://claude.ai/download"
    echo "    Then re-run this installer."
    echo ""
    read -p "    Continue anyway? PRISM will install but won't work until Claude Code is installed. [y/N] " cont
    cont="${cont:-N}"
    if [[ ! "$cont" =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "[OK] Claude Code CLI found: $(command -v claude)"
fi

# Step 2: git check
if ! command -v git &> /dev/null; then
    echo "[!] git not found"
    if [ "$OS" = "Darwin" ]; then
        echo "    macOS will prompt you to install Xcode Command Line Tools..."
        xcode-select --install 2>/dev/null || true
        echo "    Complete the install dialog, then re-run this installer."
        exit 1
    else
        echo "    Install git via your package manager (e.g. sudo apt install git), then re-run."
        exit 1
    fi
else
    echo "[OK] git found: $(git --version)"
fi

# Step 3: Homebrew check (macOS only — needed for jq install)
if [ "$OS" = "Darwin" ] && ! command -v brew &> /dev/null; then
    echo "[!] Homebrew not found"
    read -p "    Install Homebrew now? Required to auto-install jq. [Y/n] " install_brew
    install_brew="${install_brew:-Y}"
    if [[ "$install_brew" =~ ^[Yy]$ ]]; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        # Add brew to PATH for this session (Apple Silicon vs Intel paths)
        if [ -f /opt/homebrew/bin/brew ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        elif [ -f /usr/local/bin/brew ]; then
            eval "$(/usr/local/bin/brew shellenv)"
        fi
    else
        echo "    Skipping. You'll need to install jq manually before hooks can merge."
    fi
elif [ "$OS" = "Darwin" ]; then
    echo "[OK] Homebrew found: $(brew --version | head -1)"
fi

# Step 4: jq check
if ! command -v jq &> /dev/null; then
    echo "[!] jq not found"
    if command -v brew &> /dev/null; then
        read -p "    Install jq via Homebrew? [Y/n] " install_jq
        install_jq="${install_jq:-Y}"
        if [[ "$install_jq" =~ ^[Yy]$ ]]; then
            brew install jq
        fi
    elif [ "$OS" = "Linux" ]; then
        echo "    Install via: sudo apt install jq  (or your distro's package manager)"
    fi
else
    echo "[OK] jq found: $(jq --version)"
fi

# Step 5: Clone (or update) PRISM
echo ""
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "[OK] PRISM already cloned at $INSTALL_DIR"
    echo "     Pulling latest..."
    cd "$INSTALL_DIR" && git pull --ff-only
else
    if [ -d "$INSTALL_DIR" ]; then
        echo "[!] $INSTALL_DIR exists but isn't a git repo"
        read -p "    Back it up and clone fresh? [y/N] " overwrite
        overwrite="${overwrite:-N}"
        if [[ "$overwrite" =~ ^[Yy]$ ]]; then
            mv "$INSTALL_DIR" "${INSTALL_DIR}.backup.$(date +%Y%m%d-%H%M%S)"
        else
            echo "    Aborting to avoid overwriting your data."
            exit 1
        fi
    fi
    mkdir -p "$(dirname "$INSTALL_DIR")"
    echo "[+] Cloning PRISM..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Step 6: Run setup
echo ""
echo "=========================================="
echo "  Running setup.sh (personalization)..."
echo "=========================================="
cd "$INSTALL_DIR" && ./setup.sh

echo ""
echo "=========================================="
echo "  ALL DONE"
echo "=========================================="
echo ""
echo "  Next: open Claude Code anywhere and say:"
echo ""
echo "    \"Run the identity scan\""
echo ""
echo "  Or paste: Read $INSTALL_DIR/identity-scan.md and follow the instructions."
echo ""
