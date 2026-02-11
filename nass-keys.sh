#!/bin/bash

CONFIG="$HOME/.config/my_hotkeys.conf"
XBINDSRC="$HOME/.xbindkeysrc"
HELP_FILE="$(dirname "$(readlink -f "$0")")/help.txt"

# Ensure config exists
mkdir -p "$(dirname "$CONFIG")"
touch "$CONFIG"

reload_hotkeys() {
    # Remove old nass-keys section
    sed -i '/# NASSKEYS/,/^$/d' "$XBINDSRC"
    echo -e "\n# NASSKEYS" >> "$XBINDSRC"

    while IFS= read -r line; do
        [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
        HOTKEY="${line%%:*}"
        CMD="${line#*:}"
        HOTKEY="$(echo $HOTKEY | xargs)"
        CMD="$(echo $CMD | xargs)"

        # Parse our new syntax
        if [[ "$CMD" == seq:* ]]; then
            keys="${CMD#seq:}"
            IFS=',' read -ra K <<< "$keys"
            XDOCMD=""
            for k in "${K[@]}"; do
                XDOCMD+="xdotool key $k; "
            done
        elif [[ "$CMD" == sim:* ]]; then
            keys="${CMD#sim:}"
            IFS=',' read -ra K <<< "$keys"
            XDOCMD=""
            for k in "${K[@]}"; do
                XDOCMD+="xdotool keydown $k "
            done
            for (( idx=${#K[@]}-1 ; idx>=0 ; idx-- )); do
                XDOCMD+="xdotool keyup ${K[idx]} "
            done
        elif [[ "$CMD" == text:* ]]; then
            text="${CMD#text:}"
            XDOCMD="xvkbd -xsendevent -text \"$text\""
        elif [[ "$CMD" == cmd:* ]]; then
            XDOCMD="${CMD#cmd:}"
        else
            XDOCMD="$CMD"
        fi

        echo "\"$XDOCMD\"" >> "$XBINDSRC"
        echo "    $HOTKEY" >> "$XBINDSRC"
    done < "$CONFIG"

    pkill xbindkeys 2>/dev/null || true
    xbindkeys
}

show_help() {
    if [ -f "$HELP_FILE" ]; then
        cat "$HELP_FILE"
    else
        echo "Help file not found."
    fi
}

revert_hotkeys() {
    pkill xbindkeys 2>/dev/null || true
    sed -i '/# NASSKEYS/,/^$/d' "$XBINDSRC"
    > "$CONFIG"
    echo "✅ All custom hotkeys reverted and removed from config."
}

case "$1" in
    add)
        KEY="$2"
        CMD="$3"
        if grep -q "^$KEY" "$CONFIG"; then
            echo "Hotkey $KEY already exists."
        else
            echo "$KEY : $CMD" >> "$CONFIG"
            echo "Hotkey added: $KEY → $CMD"
        fi
        reload_hotkeys
        ;;
    remove)
        KEY="$2"
        sed -i "/^$KEY/d" "$CONFIG"
        echo "Hotkey removed: $KEY"
        reload_hotkeys
        ;;
    list)
        cat "$CONFIG"
        ;;
    apply)
        reload_hotkeys
        echo "✅ Hotkeys applied."
        ;;
    revert)
        revert_hotkeys
        ;;
    --help)
        show_help
        ;;
    *)
        echo "Unknown command. Use 'nass-keys --help' for usage."
        ;;
esac
