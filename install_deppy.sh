#!/bin/bash
set -e

# --- Config ---
SCRIPT_NAME="deppy"
INSTALL_DIR="/opt/$SCRIPT_NAME"
BIN_WRAPPER="/usr/local/bin/$SCRIPT_NAME"
SOURCE_SCRIPT="./deppy.py"

# --- Ensure run as root ---
if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo ./install_deppy.sh"
  exit 1
fi

# --- Check source script exists ---
if [[ ! -f "$SOURCE_SCRIPT" ]]; then
  echo "Error: Could not find $SOURCE_SCRIPT in current directory."
  exit 1
fi

# --- Create install location ---
mkdir -p "$INSTALL_DIR"
cp "$SOURCE_SCRIPT" "$INSTALL_DIR/$SCRIPT_NAME.py"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME.py"

# --- Create wrapper in /usr/local/bin ---
echo "#!/bin/bash
exec /usr/bin/env python3 $INSTALL_DIR/$SCRIPT_NAME.py \"\$@\"" > "$BIN_WRAPPER"

chmod +x "$BIN_WRAPPER"

echo "Installed '$SCRIPT_NAME' globally."
echo "You can now run: $SCRIPT_NAME"
