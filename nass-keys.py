#!/usr/bin/env python3
import os, sys, json, subprocess, time
from pathlib import Path
from PyInquirer import prompt
import keyboard

CONFIG_FILE = Path.home() / ".config" / "my_hotkeys.conf"

# Ensure config exists
if not CONFIG_FILE.exists():
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({}))

# Load config
with open(CONFIG_FILE, "r") as f:
    try:
        HOTKEYS = json.load(f)
    except:
        HOTKEYS = {}

# Save config
def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(HOTKEYS, f, indent=2)

# Interactive add
def add_hotkey():
    questions = [
        {
            'type': 'list',
            'name': 'type',
            'message': 'Select hotkey type:',
            'choices': ['Run command', 'Type text', 'Sequential keys', 'Simultaneous keys', 'Double-tap key', 'Macro']
        }
    ]
    answer = prompt(questions)
    hotkey_type = answer['type']

    if hotkey_type != "Double-tap key":
        print("Press your key combination (e.g., Ctrl+Alt+R):")
        combo = keyboard.read_hotkey()
    else:
        key = input("Enter the key to double-tap (e.g., ctrl, shift, alt): ").lower()
        combo = f"{key} (double)"

    print(f"Detected hotkey: {combo}")

    if hotkey_type == "Run command":
        value = input("Enter command to execute: ")
        HOTKEYS[combo] = {"type": "cmd", "value": value}
    elif hotkey_type == "Type text":
        value = input("Enter text to type: ")
        HOTKEYS[combo] = {"type": "text", "value": value}
    elif hotkey_type == "Sequential keys":
        value = input("Enter key sequence separated by commas (F11,F12,...): ")
        HOTKEYS[combo] = {"type": "seq", "value": value.split(",")}
    elif hotkey_type == "Simultaneous keys":
        value = input("Enter keys to press together separated by commas (F11,F12,...): ")
        HOTKEYS[combo] = {"type": "sim", "value": value.split(",")}
    elif hotkey_type == "Double-tap key":
        value = input("Enter command or text for double-tap key (prefix with cmd: or text:): ")
        HOTKEYS[combo] = {"type": "double", "value": value}
    elif hotkey_type == "Macro":
        print("Enter steps of the macro. Format: text:Hello, cmd:ls, key:enter, sleep:0.5")
        steps = input("Steps separated by commas: ").split(",")
        HOTKEYS[combo] = {"type": "macro", "value": [s.strip() for s in steps]}

    save_config()
    print(f"Hotkey {combo} added successfully!")

# List
def list_hotkeys():
    if not HOTKEYS:
        print("No hotkeys defined.")
        return
    for combo, info in HOTKEYS.items():
        print(f"{combo} : {info['type']} -> {info['value']}")

# Remove
def remove_hotkey():
    if not HOTKEYS:
        print("No hotkeys to remove.")
        return
    questions = [
        {
            'type': 'list',
            'name': 'combo',
            'message': 'Select hotkey to remove:',
            'choices': list(HOTKEYS.keys())
        }
    ]
    answer = prompt(questions)
    combo = answer['combo']
    HOTKEYS.pop(combo)
    save_config()
    print(f"Removed hotkey {combo}.")

# Apply
def apply_hotkeys():
    print("Applying hotkeys... Press ESC to exit.")
    double_tap_state = {}

    def handle_macro(steps):
        for s in steps:
            if s.startswith("text:"):
                keyboard.write(s[5:])
            elif s.startswith("cmd:"):
                subprocess.Popen(s[4:], shell=True)
            elif s.startswith("key:"):
                keyboard.press_and_release(s[4:])
            elif s.startswith("sleep:"):
                try:
                    time.sleep(float(s[6:]))
                except:
                    pass

    for combo, info in HOTKEYS.items():
        if info['type'] == "cmd":
            keyboard.add_hotkey(combo, lambda cmd=info['value']: subprocess.Popen(cmd, shell=True))
        elif info['type'] == "text":
            keyboard.add_hotkey(combo, lambda txt=info['value']: keyboard.write(txt))
        elif info['type'] == "seq":
            keyboard.add_hotkey(combo, lambda seq=info['value']: [keyboard.press_and_release(k) for k in seq])
        elif info['type'] == "sim":
            keyboard.add_hotkey(combo, lambda keys=info['value']: keyboard.press_and_release("+".join(keys)))
        elif info['type'] == "double":
            key = combo.replace(" (double)","")
            def callback(k=info['value'], key=key):
                now = time.time()
                last = double_tap_state.get(key,0)
                if now - last < 0.5: # double-tap detected
                    if k.startswith("cmd:"):
                        subprocess.Popen(k[4:], shell=True)
                    elif k.startswith("text:"):
                        keyboard.write(k[5:])
                double_tap_state[key] = now
            keyboard.on_press_key(key, lambda e: callback())
        elif info['type'] == "macro":
            keyboard.add_hotkey(combo, lambda steps=info['value']: handle_macro(steps))

    keyboard.wait("esc")

# Revert
def revert_hotkeys():
    global HOTKEYS
    HOTKEYS = {}
    save_config()
    print("All hotkeys reverted.")

# Help
def show_help():
    print("""
nass-keys CLI - Interactive Hotkey Manager

Commands:
  add     - Add a new hotkey interactively (supports cmd, text, seq, sim, double-tap, macro)
  list    - List all hotkeys
  remove  - Remove a hotkey interactively
  apply   - Apply hotkeys (ESC to exit)
  revert  - Remove all hotkeys
  help    - Show this message

Hotkey types:
  cmd       : Run a terminal command
  text      : Type text automatically
  seq       : Sequential keys (F11,F12,...)
  sim       : Simultaneous keys (F11+F12+...)
  double    : Double-tap key detection (e.g., 'ctrl (double)')
  macro     : Multi-step macro (text:..., cmd:..., key:..., sleep:...)
""")

# Main
if len(sys.argv) < 2:
    show_help()
else:
    cmd = sys.argv[1].lower()
    if cmd == "add":
        add_hotkey()
    elif cmd == "list":
        list_hotkeys()
    elif cmd == "remove":
        remove_hotkey()
    elif cmd == "apply":
        apply_hotkeys()
    elif cmd == "revert":
        revert_hotkeys()
    elif cmd == "help":
        show_help()
    else:
        print("Unknown command.")
        show_help()
