#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting dotfiles installation...${NC}"

# 1. Install GNU Stow if not present
if ! command -v stow &> /dev/null; then
    echo "Stow is not installed. Installing..."
    # Assumes a Debian/Ubuntu/Arch based system; adjust if using Fedora/macOS
    sudo apt update && sudo apt install -y stow || sudo pacman -S --noconfirm stow
fi

# 2. Pull submodules (if any)
echo -e "${GREEN}Updating git submodules...${NC}"
git submodule update --init --recursive

# 3. Manually clone plugins if they don't exist
# (This acts as a safety net for the errors you just saw)
mkdir -p .config/zsh/plugins
if [ ! -d ".config/zsh/plugins/zsh-autosuggestions" ]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions .config/zsh/plugins/zsh-autosuggestions
fi
if [ ! -d ".config/zsh/plugins/zsh-syntax-highlighting" ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting .config/zsh/plugins/zsh-syntax-highlighting
fi

# 4. Run Stow
echo -e "${GREEN}Stowing configurations...${NC}"
# --adopt handles existing files by pulling them into the repo
# Use with caution! Remove --adopt if you prefer it to just fail on conflicts.
stow --adopt .

echo -e "${BLUE}Done! Restart your shell or run 'source ~/.zshrc'${NC}"
