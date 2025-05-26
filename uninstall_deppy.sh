#!/bin/bash
set -e

SCRIPT_NAME="deppy"
INSTALL_DIR="/opt/$SCRIPT_NAME"
BIN_WRAPPER="/usr/local/bin/$SCRIPT_NAME"

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo ./uninstall_deppy.sh"
  exit 1
fi

rm -f "$BIN_WRAPPER"
rm -rf "$INSTALL_DIR"

echo "Uninstalled '$SCRIPT_NAME'."
