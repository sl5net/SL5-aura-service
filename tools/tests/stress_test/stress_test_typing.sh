#!/bin/bash

INPUT_METHOD="dotool"

do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Passe hier die Verzögerung an (z.B. 0.05, 0.1 oder 0.15), falls der Bug auftritt
        { printf 'typedelay 2\ntype %s\n' "$text"; sleep 0.05; } | dotool
    else
        LC_ALL=C.UTF-8 timeout 1 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}

echo "=== Aura dotool Stresstest ==="
echo "Bitte öffne JETZT einen Texteditor (z. B. VS Code, gedit, nano) und fokussiere das Schreibfeld."
echo "Der Test startet in 5 Sekunden..."
sleep 5

sentences=(
    "Hello world. This is a stress test for dotool typing. Let us see if it hangs on any character."
    "Another long paragraph of text that should be typed quickly. Typing under Wayland can sometimes be tricky."
    "It seems it gets with every step of development some minor improvements. Let us hope the repeating key bug is gone."
    "The brown fox jumps over the lazy dog. Programming in bash and python is fun. This is sentence number four."
    "Testing special characters and punctuation: hello! how are you? i am fine, thank you. let's check double quotes and commas."
)

for i in {1..20}; do
    idx=$(( RANDOM % ${#sentences[@]} ))
    text="${sentences[$idx]} (Iteration $i)"
    echo "Tippe Iteration $i/20..."
    do_type "$text"
    # Eine kurze Pause zwischen den Tipp-Vorgängen
    sleep 0.5
done

echo "Stresstest abgeschlossen!"
