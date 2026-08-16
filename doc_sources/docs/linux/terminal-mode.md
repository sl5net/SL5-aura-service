# Terminal Mode (Language Exclusion)

Terminal Mode is a configuration state where no specific language packs are installed or configured for the speech/text processing units.

## How to Enable
During the initial setup or language selection script, when prompted for the **Primary Language**, enter:
- `n`
- `none`
- `0`

## Effects
- **EXCLUDE_LANGUAGES** is set to `all`.
- No language-specific models (like Whisper or Vosk models) will be downloaded or initialized.
- The system operates in a "Terminal Only" mode, useful for low-disk environments or when only the core CLI tools are required without localized speech support.

## Environment Variables
When active, the following exports are generated:
```bash
export SELECTED_LANG='none'
export SECOND_LANG='none'
export EXCLUDE_LANGUAGES='all'

