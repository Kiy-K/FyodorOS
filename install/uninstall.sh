#!/bin/bash
set -e

# ----------------------------------------------------------------------
# FYODOROS KIOSK UNINSTALLER
# Reverts changes made by setup_kiosk.sh
# ----------------------------------------------------------------------

if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Please run as root."
  exit 1
fi

echo "🗑️  Uninstalling FyodorOS Kiosk..."

# 1. REMOVE ARTIFACTS
echo "   Removing /opt/fyodoros..."
rm -rf /opt/fyodoros

echo "   Removing /usr/local/bin/fyodor..."
rm -f /usr/local/bin/fyodor

# 2. RESTORE OPENBOX CONFIG
OPENBOX_AUTOSTART="/etc/xdg/openbox/autostart"
if [ -f "$OPENBOX_AUTOSTART.bak" ]; then
    echo "   Restoring Openbox autostart backup..."
    mv "$OPENBOX_AUTOSTART.bak" "$OPENBOX_AUTOSTART"
else
    echo "   Removing Openbox autostart (no backup found)..."
    rm -f "$OPENBOX_AUTOSTART"
fi

# 3. RESTORE LIGHTDM CONFIG
echo "   Removing LightDM configuration..."
rm -f /etc/lightdm/lightdm.conf.d/50-fyodor.conf

# 4. REVERT DISPLAY MANAGER
# Check if GDM3 is available (common Ubuntu default)
if [ -f "/usr/sbin/gdm3" ]; then
    echo "   Reverting to GDM3..."
    echo "/usr/sbin/gdm3" > /etc/X11/default-display-manager
    systemctl disable lightdm
    systemctl enable gdm3
else
    echo "⚠️  GDM3 not found. Leaving LightDM enabled but unconfigured."
    echo "   You may be presented with a login screen on reboot."
fi

# NOTE: We intentionally DO NOT remove the 'fyodor' user or their home directory
# to preserve user data and avoid accidental deletion of important files.

echo "✅ Uninstall Complete."
echo "   Please reboot to restore your session."
