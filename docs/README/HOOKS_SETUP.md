# Setting Up Pre-Push Git Hooks and Python Tools on Linux

This project uses a pre-push Git hook to automatically update `requirements.txt` from your Python scripts.  
To use this workflow, you need to have the `pipreqs` tool installed and available to Git.

## Recommended: Install pipreqs with pipx

1. **Install pipx (if not already installed):**
   ```bash
   sudo pacman -S python-pipx
   ```

2. **Install pipreqs using pipx:**
   ```bash
   pipx install pipreqs
   ```

3. **Verify pipreqs works:**
   ```bash
   pipreqs --version
   ```

## Alternative: Use a Python Virtual Environment

If you prefer or are using a virtualenv for your project:

1. **Create and activate a virtualenv:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install pipreqs inside the virtualenv:**
   ```bash
   pip install pipreqs
   ```

3. **Edit the git hook** to call pipreqs using the full path:
   ```bash
   .venv/bin/pipreqs "$TMPDIR" --force
   ```

## Why not use plain pip install?

Modern Linux distros restrict system-wide pip installs to prevent breaking OS packages.  
**Do NOT** use `sudo pip install pipreqs` or `pip install pipreqs` globally.

## Troubleshooting

- If you see `pipreqs: command not found`, make sure you installed it with pipx and that `~/.local/bin` is in your `$PATH`.
- You can check your path with:
  ```bash
  echo $PATH
  ```

## Need help?

Open an issue or ask in the project discussion!
