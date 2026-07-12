"""Insert a template rule right before the catch-all rule."""

import re
from pathlib import Path


def insert_template_rule(fuzzy_map_file: Path, content: str, catch_all_start: int, text: str = "nix"):
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
