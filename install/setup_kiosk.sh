#!/bin/bash
set -e

# ----------------------------------------------------------------------
# FYODOROS KIOSK INSTALLER
# Transforms a standard Linux install into a FyodorOS Kiosk.
# ----------------------------------------------------------------------

# 1. CHECKS
if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Please run as root."
  exit 1
fi

if [ ! -f "pyproject.toml" ]; then
  echo "❌ Error: Please run from the repository root."
  exit 1
fi

if [ -z "$SUDO_USER" ]; then
  echo "❌ Error: Could not detect invoking user. Please run with sudo."
  exit 1
fi

echo "✅ Environment checks passed."
echo "Target User: $SUDO_USER"
TARGET_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
echo "Target Home: $TARGET_HOME"

# 2. DEPENDENCIES
echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y \
    python3-pip \
    python3-tk \
    libwebkit2gtk-4.0-37 \
    openbox \
    lightdm \
    rxvt-unicode \
    git \
    cmake \
    python3-pybind11 \
    build-essential \
    patchelf \
    ccache

# 3. CORE INSTALL
echo "🚀 Installing FyodorOS..."

# Clean previous install if exists
rm -rf /opt/fyodoros
mkdir -p /opt/fyodoros

# Copy source to /opt/fyodoros
echo "   Copying source to /opt/fyodoros..."
cp -r . /opt/fyodoros/

# Set permissions
chown -R root:root /opt/fyodoros
chmod -R 755 /opt/fyodoros

# Build & Install
cd /opt/fyodoros

echo "   Building C++ extensions..."
python3 setup_extensions.py install

echo "   Installing Python package..."
pip install .

# 4. USER CONFIGURATION
echo "👤 Initializing user configuration..."
if [ -d "$TARGET_HOME/.fyodor" ]; then
    echo "   ~/.fyodor exists, skipping initialization."
else
    su - "$SUDO_USER" -c "fyodor init"
fi

# 5. KIOSK CONFIGURATION (OPENBOX)
echo "🖥️  Configuring Openbox Kiosk..."
OPENBOX_AUTOSTART="/etc/xdg/openbox/autostart"

# Backup existing autostart
if [ -f "$OPENBOX_AUTOSTART" ] && [ ! -f "$OPENBOX_AUTOSTART.bak" ]; then
    cp "$OPENBOX_AUTOSTART" "$OPENBOX_AUTOSTART.bak"
fi

cat > "$OPENBOX_AUTOSTART" <<EOF
# FyodorOS Kiosk Autostart
xset -dpms
xset s off
# Launch Fyodor inside URXVT for visibility/debugging, then drop to bash if it crashes
urxvt -geometry 120x40 -e sh -c "/usr/local/bin/fyodor start; bash" &
EOF

# 6. SESSION MANAGER (LIGHTDM)
echo "💡 Configuring LightDM..."

# Ensure LightDM config directory exists
mkdir -p /etc/lightdm/lightdm.conf.d

# Configure Autologin
cat > /etc/lightdm/lightdm.conf.d/50-fyodor.conf <<EOF
[Seat:*]
autologin-user=$SUDO_USER
autologin-session=openbox
EOF

# Force LightDM as default
echo "   Setting LightDM as default display manager..."
echo "/usr/sbin/lightdm" > /etc/X11/default-display-manager

# Enable LightDM service, disable others
systemctl stop gdm3 2>/dev/null || true
systemctl disable gdm3 2>/dev/null || true
systemctl enable lightdm

echo "✅ Installation Complete!"
echo "   Please reboot your machine to enter the Kiosk."
