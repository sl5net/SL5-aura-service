# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py
"""
Entry point invoked (via on_match_exec) when the catch-all rule matches.
Delegates the actual file-update logic to helpers/process_unmatched_text.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'helpers'))

from .helpers.process_unmatched_text import process_unmatched_text

def execute(match_data: dict):

    text = match_data['original_text']
    file_rule_path = match_data['text_after_replacement']
    print(f'file_rule_path: {file_rule_path}')
    if not text:
        print(f'ERROR: text empty {text}')
        return None
    process_unmatched_text(file_rule_path, text)
    sys.exit(1)
