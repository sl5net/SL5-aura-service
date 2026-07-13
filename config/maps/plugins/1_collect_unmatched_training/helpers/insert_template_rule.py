"""
insert_template_rule.py
Insert a template rule right before the catch-all rule."""

import re
import os
from pathlib import Path
import logging

try:
    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())
except Exception as e:
    print(e)
    raise

log_file = PROJECT_ROOT / "log" / f"{Path(__file__).stem}.log"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(log_file)


def insert_template_rule(fuzzy_map_file: Path, content: str, catch_all_start: int, text: str = "nix"):

    from scripts.py.func.audio.handle_tts_fallback import handle_tts_fallback
    """
    Insert a template rule for `text`, e.g. ('nix', r'^(nix)$'), on its own
    line, directly before the catch-all rule (matching its indentation),
    and write the updated content back to `fuzzy_map_file`.

    `text` is embedded safely:
    - re.escape(text) escapes regex-special characters, so characters like
      '(', '.', '*' in `text` can't break or change the pattern's meaning.
    - repr(...) is used for BOTH the label and the pattern (instead of a
      fixed r'...' template) to build valid Python string literals. This
      matters because re.escape() does not escape quote characters, so a
      raw '\'' in `text` (e.g. "das ist's") would otherwise still be able
      to break out of a hardcoded r'...' literal. repr() picks whichever
      quote style avoids that and escapes backslashes/quotes correctly.

    The label carries a trailing '2' (e.g. text='wasser' -> label 'wasser2')
    so the user can visually tell the label apart from the matched text
    itself and recognize that it has been auto-generated/changed. The
    regex pattern itself is unaffected and still matches `text` exactly.
    """
    line_start = content.rfind('\n', 0, catch_all_start) + 1
    indent_match = re.match(r'[ \t]*', content[line_start:catch_all_start])
    indent = indent_match.group() if indent_match else ''

    label = repr(f"{text}2")
    pattern_literal = repr(f'^({re.escape(text)})$')

    template_line = f"{indent}({label}, {pattern_literal}),\n"
    new_content = content[:line_start] + template_line + content[line_start:]
    fuzzy_map_file.write_text(new_content, encoding="utf-8")

    lang_for_tts = "de-DE"
    handle_tts_fallback(str(fuzzy_map_file), lang_for_tts, logger)
