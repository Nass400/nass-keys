# Nass-Keys ⌨️

Nass-Keys is a lightweight Linux hotkey manager that allows you to map key combinations to commands, text, or key sequences—including sequential or simultaneous key presses—without manual setup. Perfect for automating repetitive tasks.

---

## 🚀 Features

* **Versatile Mapping:** Map hotkeys to terminal commands, files, folders, or automated text.
* **Macro Support:** Press function keys sequentially (`seq`) or simultaneously (`sim`).
* **Simple Configuration:** Manage everything via a single file (`my_hotkeys.conf`).
* **CLI Managed:** Apply, list, remove, or revert hotkeys with simple commands.
* **Portable:** Fully scriptable and works across Linux systems using X11.

---

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Nass400/nass-keys.git
    cd nass-keys
    ```

2.  **Run the setup script:**
    ```bash
    chmod +x setup-nass-keys.sh
    ./setup-nass-keys.sh
    ```

> [!IMPORTANT]
> The setup script installs dependencies (`xbindkeys`, `xdotool`, `xvkbd`), sets up the `nass-keys` CLI in `~/bin`, and initializes default configurations.

---

## 🛠 Usage

### Common Commands

```bash
# Add a new hotkey
nass-keys add "Ctrl+Alt+R" "seq:F11,F12"

# Apply changes (required after adding/removing)
nass-keys apply

# List current hotkeys
nass-keys list

# Remove a specific hotkey
nass-keys remove "Ctrl+Alt+N"

# Revert all custom hotkeys to default
nass-keys revert
 ```
### Hotkey Command Formats

| Type | Syntax | Example | Description |
| :--- | :--- | :--- | :--- |
| **Sequential** | `seq:key1,key2` | `seq:F11,F12` | Presses keys one after another |
| **Simultaneous** | `sim:key1,key2` | `sim:F11,F12` | Presses keys together |
| **Text** | `text:string` | `text:Hello world!` | Automatically types text |
| **Command** | `cmd:utility` | `cmd:gnome-terminal` | Executes terminal commands |
| **Direct** | `bash command` | `xdg-open ~/Docs` | Runs any shell command |

---

## ⚙️ Configuration

All hotkey definitions are stored in `~/.config/my_hotkeys.conf`.

**Example Config Structure:**
```bash
# Sequential keys
Ctrl+Alt+R : seq:F11,F12

# Type text
Ctrl+Alt+U : text:Hello world!

# Run a command
Ctrl+Alt+N : cmd:gnome-terminal
```

### 💡 Pro Tips

* **Delays:** To add a pause in sequential keys, use the `sleep` command:  
  `seq:F11,sleep 0.1,F12`
* **Comments:** Lines starting with `#` in your `my_hotkeys.conf` file are ignored, making it easy to organize your shortcuts.
* **X11 Requirement:** Ensure you are running an **X11 session** (standard on most desktop Linux distros like Ubuntu, Mint, or Fedora).

---

### 🖇 Dependencies

Nass-Keys relies on the following core packages to function:

* **xbindkeys**: For detecting your keyboard shortcuts.
* **xdotool**: For simulating mouse and keyboard input.
* **xvkbd**: For handling virtual keyboard text entry.

---

### 📄 License

This project is open-source and free to use, modify, and distribute.
