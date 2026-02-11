# nass-keys

Interactive CLI tool to manage hotkeys on Linux.

## Features

- Run terminal commands
- Type text automatically
- Sequential key presses
- Simultaneous key presses
- Double-tap key detection
- Multi-step macros

## Commands

- `nass-keys add`       : Add a new hotkey interactively
- `nass-keys list`      : List all hotkeys
- `nass-keys remove`    : Remove a hotkey interactively
- `nass-keys apply`     : Apply hotkeys (press ESC to exit)
- `nass-keys revert`    : Remove all hotkeys
- `nass-keys help`      : Show help

## Hotkey Types

- `cmd`      : Run a terminal command
- `text`     : Type text automatically
- `seq`      : Sequential keys (F11,F12,...)
- `sim`      : Simultaneous keys (F11+F12+...)
- `double`   : Double-tap key detection (e.g., 'ctrl (double)')
- `macro`    : Multi-step macro (text:..., cmd:..., key:..., sleep:...)

## Installation

```bash
git clone <repo_url>
cd nass-keys
./setup-nass-keys.sh
