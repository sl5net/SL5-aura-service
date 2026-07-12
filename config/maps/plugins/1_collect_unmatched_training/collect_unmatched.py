# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py
"""
Entry point invoked (via on_match_exec) when the catch-all rule matches.
Delegates the actual file-update logic to helpers/process_unmatched_text.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'helpers'))

from process_unmatched_text import process_unmatched_text  # noqa: E402
import process_unmatched_text as _put_module  # noqa: E402
import insert_template_rule as _itr_module  # noqa: E402


def execute(match_data: dict):
    # --- TEMPORARY DEBUG, remove once the issue is found ---
    print(f'DEBUG collect_unmatched.py __file__: {Path(__file__).resolve()}')
    print(f'DEBUG process_unmatched_text loaded from: {Path(_put_module.__file__).resolve()}')
    print(f'DEBUG insert_template_rule loaded from: {Path(_itr_module.__file__).resolve()}')
    print(f'DEBUG match_data: {match_data!r}')
    # --- end debug ---

    text = match_data['original_text']
    file_rule_path = match_data['text_after_replacement']
    print(f'file_rule_path: {file_rule_path}')
    if not text:
        print(f'ERROR: text empty {text}')
        return None
    process_unmatched_text(file_rule_path, text)
    sys.exit(1)
