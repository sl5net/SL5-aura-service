#!/bin/bash

# test:
# bash -x ./scripts/type_watcher/detect_layout.sh

# 2. Keyboard-Layout from Modellname
XKB_LAYOUT=''
MODEL_PATH="config/model_name.txt"
if [[ -f "$MODEL_PATH" ]]; then
    MODEL_NAME=$(cat "$MODEL_PATH")
    XKB_LAYOUT=$(echo "$MODEL_NAME" | sed -n 's/.*model-\([a-z]\{2\}\).*/\1/p')
fi

[[ -z "$XKB_LAYOUT" ]] && XKB_LAYOUT="de"

LANG_CODE="${LANG_CODE:-de}"

uname_s=$(uname -s)

if [[ "$uname_s" == "Darwin" ]]; then
    # macOS: use compiled helper get_macos_layout (see get_macos_layout.c)
    if command -v ./get_macos_layout &>/dev/null || command -v get_macos_layout &>/dev/null; then
        if command -v get_macos_layout &>/dev/null; then
            MAC_SRC=$(get_macos_layout 2>/dev/null)
        else
            MAC_SRC=$(./get_macos_layout 2>/dev/null)
        fi

        if [[ -n "$MAC_SRC" ]]; then
            # map common macOS input source IDs to layout codes
            case "$MAC_SRC" in
                *German*|*keylayout.German*|*com.apple.keylayout.German*) XKB_LAYOUT="de" ;;
                *US*|*keylayout.US*|*com.apple.keylayout.US*|*com.apple.keylayout.ABC*) XKB_LAYOUT="us" ;;
                *com.apple.keylayout.Japanese*|*keylayout.Japanese*) XKB_LAYOUT="jp" ;;
                *com.apple.keylayout.Australian*|*Australian*) XKB_LAYOUT="au" ;;
                *)
                    # Try to extract last segment: com.apple.keylayout.German -> German -> de
                    SHORT=$(echo "$MAC_SRC" | sed -n 's/.*\.keylayout\.\([A-Za-z]*\).*/\1/p')
                    if [[ "$SHORT" == "German" ]]; then XKB_LAYOUT="de"; fi
                    ;;
            esac
        fi
    else
        echo "WARN: get_macos_layout helper not found; bitte get_macos_layout.c kompilieren."
    fi

else
    # Linux: systemd localectl
    if command -v localectl &>/dev/null; then
        DETECTED=$(localectl status | grep "X11 Layout" | sed -n 's/.*Layout:[[:space:]]*\([a-z]\{2\}\).*/\1/p')
        [[ -n "$DETECTED" ]] && XKB_LAYOUT="$DETECTED"
    fi

    # Fallback: setxkbmap (X11)
    if [[ "$XKB_LAYOUT" == "de" ]] && command -v setxkbmap &>/dev/null; then
        DETECTED=$(setxkbmap -query 2>/dev/null | grep "layout" | sed -n 's/.*layout:[[:space:]]*\([a-z]\{2\}\).*/\1/p')
        [[ -n "$DETECTED" ]] && XKB_LAYOUT="$DETECTED"
    fi
fi

export XKB_DEFAULT_LAYOUT="$XKB_LAYOUT"
export DOTOOL_XKB_LAYOUT="$XKB_LAYOUT"
echo "Language detected: $LANG_CODE (Mapped to layout: $XKB_LAYOUT)" >&2
echo "$XKB_LAYOUT"



