# tests/test_collect_unmatched.py
import unittest
import sys
from pathlib import Path

# Insert plugin helpers directory to sys.path dynamically
root_dir = Path(__file__).resolve().parents[1]
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
        entries = get_fuzzy_map_entries(self.mock_variable)
        self.assertIsNotNone(entries)
        self.assertEqual(len(entries), 2)

        idx = find_catch_all_index(self.mock_variable, entries)
        self.assertEqual(idx, 1)

        rule_source = self.mock_variable[entries[0][0]:entries[0][1]]
        span = find_trailing_group_span(rule_source)
        self.assertIsNotNone(span)
        s, e, hp = span
        self.assertTrue(hp)
        self.assertEqual(rule_source[s:e], "Python|System Instructions")

    def test_parser_with_string_literal(self):
        entries = get_fuzzy_map_entries(self.mock_string)
        self.assertIsNotNone(entries)
        self.assertEqual(len(entries), 2)

if __name__ == "__main__":
    unittest.main()
