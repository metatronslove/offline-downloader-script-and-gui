#!/bin/bash
set -e  # Exit immediately if any command fails

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Header
echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════╗"
echo "║      Offline Page Downloader Installation      ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

# 1. Install dependencies
echo -e "${YELLOW}➤ Installing dependencies...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-requests python3-bs4 python3-pyqt5 wget

# 2. Download and extract source files
echo -e "${YELLOW}➤ Downloading application...${NC}"
wget -q https://github.com/metatronslove/offline-downloader-script-and-gui/archive/refs/tags/offline-page-downloader.tar.gz
tar -xzf offline-page-downloader.tar.gz
cd offline-downloader-script-and-gui-offline-page-downloader

# 3. Install files to correct locations
echo -e "${YELLOW}➤ Installing files...${NC}"
sudo install -Dm644 utils.py "/usr/lib/python3/dist-packages/utils.py"
sudo install -Dm755 offline_downloader.py "/usr/bin/offline_downloader"
sudo install -Dm755 offline_downloader_gui.py "/usr/bin/offline_downloader_gui"
sudo install -Dm644 LICENSE.md "/usr/share/doc/offline-page-downloader/LICENSE"

# 4. Create desktop shortcut
echo -e "${YELLOW}➤ Creating desktop entry...${NC}"
sudo mkdir -p "/usr/share/applications"
sudo bash -c 'cat > /usr/share/applications/offline-downloader.desktop <<EOD
[Desktop Entry]
Name=Offline Page Downloader
Exec=/usr/bin/offline_downloader_gui
Icon=/usr/share/icons/offline-downloader.png
Type=Application
Categories=Network;
EOD'

# 5. Download icon
echo -e "${YELLOW}➤ Setting up icon...${NC}"
sudo mkdir -p "/usr/share/icons"
sudo wget -q https://raw.githubusercontent.com/metatronslove/offline-downloader-script-and-gui/main/icon.png -O "/usr/share/icons/offline-downloader.png"

# 6. Cleanup
echo -e "${YELLOW}➤ Cleaning up...${NC}"
cd ..
rm -rf offline-page-downloader.tar.gz offline-downloader-script-and-gui-offline-page-downloader

# Completion message
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════╗"
echo "║          Installation Successful!             ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

# Usage instructions
echo -e "${CYAN}HOW TO USE:${NC}"
echo -e "1. Terminal version: ${YELLOW}offline_downloader <URL>${NC}"
echo -e "   Example: offline_downloader https://example.com"
echo -e ""
echo -e "2. GUI version: ${YELLOW}offline_downloader_gui${NC}"
echo -e "   (Look for 'Offline Page Downloader' in your application menu)"
echo -e ""
echo -e "3. To uninstall: ${YELLOW}sudo rm /usr/bin/offline_downloader* && sudo rm -r /usr/share/icons/offline-downloader.png /usr/share/applications/offline-downloader.desktop /usr/lib/python3/dist-packages/utils.py${NC}"
echo -e ""
echo -e "${GREEN}Enjoy your offline browsing!${NC}"