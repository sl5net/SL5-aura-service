# Aura Admin UI

The Admin UI lets you view and change Aura settings in your browser with zero idle resource cost. The dashboard server does not run on boot; it is started on-demand only when requested.

## How to Open (On-Demand)

You can launch and open the Admin Dashboard dynamically using any of the following three methods:

### 1. Voice Command
Simply speak into your microphone:
* *"aura administration"

### 2. Terminal / Console Command
If you are working in the terminal, run this command to trigger the launcher directly:
```bash
s aura administration
```

*⚠️ **Platform Note for Windows/macOS Users:** The short `s` command wrapper is primarily configured for Linux environments. Please read the doc for that. If you are running Windows or macOS, the `s` command may not work out-of-the-box. Please refer to our official CLI setup documentation to learn how to configure and implement the `s` command alias for your operating system.*


### 3. Desktop Shortcut
To create a platform-specific desktop icon, run this setup script once:
```bash
python scripts/py/chat/install_shortcut.py
```
Then, simply double-click the **Aura Admin Dashboard** icon on your Desktop.

---

## Direct Browser Access
Once the server has been launched via any of the on-demand methods above, you can access the interface directly in your browser at any time:

http://localhost:8084

*(Feel free to bookmark this link in your browser!)*

---

## What You Can Do

- See translation status for each interface (speech, terminal, web).
- Enable or disable translation per interface.
- Choose target language (English, French, Spanish, etc.).

## Interfaces

| Interface | Description                        |
|-----------|------------------------------------|
| speech    | Voice input (microphone)           |
| terminal  | Command line (`s` command)         |
| web       | Streamlit web chat (port 8831)     |

## Example

To translate only web users to English — leave speech and terminal off, enable web with language `en`.
