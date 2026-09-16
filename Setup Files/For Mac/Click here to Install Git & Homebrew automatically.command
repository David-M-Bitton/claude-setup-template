#!/bin/bash
# Installs Git + Homebrew on this Mac automatically. Double-click this file to run it.
# Safe to run more than once — it skips anything already installed.

echo ""
echo "=============================================="
echo "  Setting up this Mac for Claude Code"
echo "=============================================="
echo ""

# ---------- Git (via Apple's free Command Line Tools) ----------
if command -v git >/dev/null 2>&1; then
  echo "Git is already installed: $(git --version)"
else
  echo "Installing Git (via Apple's Command Line Tools)..."
  echo "A small Apple window should pop up — click Install, then agree to the license."
  echo ""

  if xcode-select --install 2>&1 | grep -q "already installed"; then
    echo "macOS says developer tools are already installed, but 'git' isn't on PATH."
    echo "Try opening a NEW Terminal window, or restart your Mac, then run: git --version"
  else
    i=0
    until command -v git >/dev/null 2>&1; do
      sleep 5
      i=$((i + 5))
      if [ $((i % 30)) -eq 0 ]; then
        echo "   ...still waiting — look for the Apple install popup and click Install."
      fi
      if [ $i -ge 600 ]; then
        echo "This is taking a while (10+ minutes). If you never saw a popup, close this"
        echo "window and tell Claude — something may have blocked it."
        break
      fi
    done
    if command -v git >/dev/null 2>&1; then
      echo "Git installed: $(git --version)"
    fi
  fi
fi

echo ""

# ---------- Homebrew ----------
if command -v brew >/dev/null 2>&1; then
  echo "Homebrew is already installed: $(brew --version | head -1)"
else
  echo "Installing Homebrew..."
  echo "It will ask for THIS MAC'S LOGIN PASSWORD — that's normal, it's not sent anywhere."
  echo "(Typing will be invisible — that's normal too, just type it and press Enter.)"
  echo ""
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  # Apple Silicon Macs need Homebrew added to PATH; Intel Macs work out of the box.
  if [ "$(uname -m)" = "arm64" ]; then
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
  fi

  if command -v brew >/dev/null 2>&1; then
    echo "Homebrew installed: $(brew --version | head -1)"
  else
    echo "Homebrew's installer finished but 'brew' isn't on PATH yet in this window."
    echo "Close this window, open a NEW Terminal, and run: brew --version"
  fi
fi

echo ""
echo "=============================================="
echo "  All done! You can close this window now"
echo "  and go back to setting up Claude."
echo "=============================================="
echo ""
read -p "Press Enter to close this window..."
