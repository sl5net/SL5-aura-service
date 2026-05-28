# Aura Admin UI

The Admin UI lets you view and change Aura settings in your browser.

## Open

http://localhost:8084

## What you can do

- See translation status for each interface (speech, terminal, web)
- Enable or disable translation per interface
- Choose target language (English, French, Spanish, etc.)

## Interfaces

| Interface | Description                        |
|-----------|------------------------------------|
| speech    | Voice input (microphone)           |
| terminal  | Command line (`s` command)         |
| web       | Streamlit web chat (port 8831)     |

## Example

To translate only web users to English — leave speech and terminal off,
enable web with language `en`.
