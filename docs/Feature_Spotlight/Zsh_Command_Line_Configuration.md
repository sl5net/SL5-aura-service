This document summarizes the final and verified Zsh configuration for interacting with your Python service via the command line.

The configuration provides three distinct methods for accessing the service, ranging from safe output to immediate execution.

## Zsh Command Line Configuration Summary

### 1. Configuration File

All the code below should be pasted into your **`~/.zshrc`** file. Remember to **`source ~/.zshrc`** or open a new terminal session after making changes.

### 2. The Final Code Block

This block defines the three required functions. It includes the necessary `unalias` commands to prevent the conflict error we previously encountered.

```bash
# ===================================================================
# == 1. sl: Output Only (Safe Mode - Just prints the result)
# ===================================================================

# Unalias 'sl' in case it was previously defined as a simple alias
unalias sl 2>/dev/null
sl() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    /home/seeh/projects/py/STT/.venv/bin/python3 /home/seeh/projects/py/STT/scripts/py/cli_client.py "$*" --lang "de-DE"
}
# source ~/.zshrc


# ===================================================================
# == 2. slz: Zsh Line Insertion (Safe Prep Mode - Paste output to prompt)
# ===================================================================

# Unalias 'slz' in case it was previously defined as an alias
unalias slz 2>/dev/null
slz() {
    if [ $# -eq 0 ]; then
        echo "Usage: slz <your question whose result should be pasted to the line>"
        return 1
    fi

    # 1. Execute the client and capture the output (the command string)
    # "$*" ensures all arguments are passed as a single string to the CLI client.
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" --lang "de-DE")

    # 2. Use 'print -z' to paste the captured command into the current prompt line.
    print -z "$COMMAND"
}
# source ~/.zshrc

# ===================================================================
# == 3. slxXsoidfuasdzof: Immediate Execution (DANGEROUS MODE)
# ===================================================================

# Unalias the long name in case it was previously defined
unalias slxXsoidfuasdzof 2>/dev/null
slxXsoidfuasdzof() {
    if [ $# -eq 0 ]; then
        echo "Usage: slx <your question whose result will be executed immediately>"
        return 1
    fi

    # Führt den CLI-Client aus und speichert die Ausgabe in der Variable 'COMMAND'
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" \
        --lang "de-DE")

    # Check if any output was received
    if [ -n "$COMMAND" ]; then
        echo "--> Ausführen des Befehls: $COMMAND"
        echo "--> Executing command: $COMMAND"
        # DANGER: 'eval' executes the command string immediately
        eval "$COMMAND"
    else
        echo "No command output received from the service."
    fi
}
# source ~/.zshrc

```

---

### 3. Usage of the Three Commands

| Command | Functionality | Safety Level | Example |
| :--- | :--- | :--- | :--- |
| **`sl`** | **Standard Output:** Executes the service and prints the entire output directly to the console. | **SAFE** | `sl What is a house` (Prints: "A house is...") |
| **`slz`** | **Safe Execution Prep:** Executes the service and pastes the output (e.g., a shell command) into the Zsh input line, ready for review or execution. | **SAFE/PREP** | `slz git` (Pastes: `git add . && git commit...` **but does not run it**.) |
| **`slxXsoidfuasdzof`** | **Immediate Execution:** Executes the service and immediately runs the output as a shell command. Use the cryptic name as a security measure. | **DANGEROUS** | `slxXsoidfuasdzof git` (Runs the `git add...` command immediately.) |
