#!/bin/bash

XBINDSRC="$HOME/.xbindkeysrc"
CONFIG="$HOME/.config/my_hotkeys.conf"

pkill xbindkeys 2>/dev/null || true
sed -i '/# NASSKEYS/,/^$/d' "$XBINDSRC"
> "$CONFIG"

echo "✅ Custom hotkeys removed and config cleared."
