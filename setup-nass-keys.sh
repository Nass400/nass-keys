#!/bin/bash
# -------------------------------
# nass-keys setup script
# Installs dependencies and sets up nass-keys globally
# -------------------------------

# Update package lists
sudo apt update

# Install required system packages
sudo apt install -y python3 python3-pip xbindkeys xdotool xvkbd

# Install required Python packages
pip3 install --user keyboard PyInquirer

# Create a bin folder in home if it doesn't exist
mkdir -p ~/bin

# Copy nass_keys.py to ~/bin as 'nass-keys'
cp nass_keys.py ~/bin/nass-keys
chmod +x ~/bin/nass-keys

# Add ~/bin to PATH if not already
if ! echo $PATH | grep -q "$HOME/bin"; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
fi

echo "Setup complete! You can now run 'nass-keys' from anywhere."
