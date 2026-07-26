# tools/tests/test_collect_unmatched.py
import os
import unittest
import sys
from pathlib import Path

# Insert plugin helpers directory to sys.path dynamically


tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())
root_dir = PROJECT_ROOT
helpers_dir = root_dir / "config" / "maps" / "plugins" / "1_collect_unmatched_training" / "helpers"
if str(helpers_dir) not in sys.path:
    sys.path.insert(0, str(helpers_dir))

from get_fuzzy_map_entries import get_fuzzy_map_entries
from find_catch_all_index import find_catch_all_index
from find_trailing_group_span import find_trailing_group_span

class TestCollectUnmatched(unittest.TestCase):
    def setUp(self):
        # Mock file content containing an active variable
        self.mock_variable = """
System_Instructions_20260721_1417 = "dummy instruction string"
FUZZY_MAP_pre = [
    (System_Instructions_20260721_1417, r'^(Python|System Instructions)$'),
    (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [
        PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
]
"""
        # Mock file content containing a string literal
        self.mock_string = """
FUZZY_MAP_pre = [
    ('System_Instructions_20260721_1417', r'^(Python|System Instructions)$'),
    (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [
        PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
]
"""

    def test_parser_with_variable(self):
        print("\n--- start: test_parser_with_variable ---")
        entries = get_fuzzy_map_entries(self.mock_variable)
        self.assertIsNotNone(entries)
        self.assertEqual(len(entries), 2)
        print(f"[OK] {len(entries)} entries from Mock.")

        idx = find_catch_all_index(self.mock_variable, entries)
        self.assertEqual(idx, 1)
        print(f"[OK] Catch-All-rule-Index was found at: {idx}")

        rule_source = self.mock_variable[entries[0][0]:entries[0][1]]
        print(f"[INFO] found rule-source:\n{rule_source.strip()}")

        span = find_trailing_group_span(rule_source)
        self.assertIsNotNone(span)
        s, e, hp = span
        self.assertTrue(hp)
        match_pattern = rule_source[s:e]
        self.assertEqual(match_pattern, "Python|System Instructions")
        print(f"[OK] search pattern: '{match_pattern}'")

    def test_parser_with_string_literal(self):
        print("\n--- start: test_parser_with_string_literal ---")
        entries = get_fuzzy_map_entries(self.mock_string)
        self.assertIsNotNone(entries)
        self.assertEqual(len(entries), 2)
        print(f"[OK] {len(entries)} entries successfully from Mock-String-Literal ")
if __name__ == "__main__":
    unittest.main()
