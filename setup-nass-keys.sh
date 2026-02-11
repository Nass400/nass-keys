#!/bin/bash

# Install dependencies
sudo apt update
sudo apt install -y xbindkeys xdotool xvkbd

# Create default xbindkeys config if missing
if [ ! -f "$HOME/.xbindkeysrc" ]; then
    xbindkeys --defaults > "$HOME/.xbindkeysrc"
fi

# Make nass-keys system-wide
mkdir -p ~/bin
cp nass-keys.sh ~/bin/nass-keys
chmod +x ~/bin/nass-keys

# Ensure ~/bin is in PATH
if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/bin:$PATH"
fi

echo "✅ Setup complete! You can now use the 'nass-keys' command."
echo "Try 'nass-keys --help' to see available commands."
