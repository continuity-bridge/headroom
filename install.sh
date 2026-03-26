#!/bin/bash
#
# headroom installer
#
# Quick setup script for headroom Claude usage monitor
#

set -e

echo "headroom installer"
echo "=================="
echo

# Check OS
if [ -f /etc/debian_version ]; then
    PKG_MGR="apt"
    INSTALL_CMD="sudo apt install -y"
elif [ -f /etc/arch-release ]; then
    PKG_MGR="pacman"
    INSTALL_CMD="sudo pacman -S --noconfirm"
elif [ -f /etc/fedora-release ]; then
    PKG_MGR="dnf"
    INSTALL_CMD="sudo dnf install -y"
else
    echo "Unsupported OS. Please install dependencies manually."
    PKG_MGR="unknown"
fi

# Install system dependencies
if [ "$PKG_MGR" != "unknown" ]; then
    echo "Installing system dependencies..."
    
    case "$PKG_MGR" in
        apt)
            $INSTALL_CMD python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-appindicator3-0.1
            ;;
        pacman)
            $INSTALL_CMD python-gobject gtk4 libadwaita libappindicator-gtk3
            ;;
        dnf)
            $INSTALL_CMD python3-gobject gtk4 libadwaita libappindicator-gtk3
            ;;
    esac
fi

# Install Python dependencies
echo
echo "Installing Python dependencies..."
pip install requests --break-system-packages || pip install --user requests

# Make scripts executable
echo
echo "Making scripts executable..."
chmod +x headroom.py claude-setup-session claude-auto-sync claude-sync-usage

# Setup
echo
echo "Installation complete!"
echo
echo "Next steps:"
echo "  1. Run: ./claude-setup-session"
echo "  2. Follow the wizard to configure API access"
echo "  3. Run: ./headroom.py"
echo
echo "Optional:"
echo "  - Autostart: cp headroom.desktop ~/.config/autostart/"
echo "  - Auto-sync: crontab -e (add: */5 * * * * $(pwd)/claude-auto-sync)"
echo
