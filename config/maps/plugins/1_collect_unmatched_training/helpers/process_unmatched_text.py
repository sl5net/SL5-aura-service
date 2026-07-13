"""Orchestrate the update of a FUZZY_MAP_pre.py file for an unmatched text."""

from pathlib import Path

# helpers4collect_unmatched
from get_fuzzy_map_entries import get_fuzzy_map_entries
from find_catch_all_index import find_catch_all_index
from add_variant_to_rule import add_variant_to_rule
from insert_template_rule import insert_template_rule

def process_unmatched_text(file_rule_path: str, text: str):
    """
    Update the FUZZY_MAP_pre.py file at `file_rule_path` so it can match
    `text` next time:

    - No catch-all rule found -> do nothing.
    - Catch-all rule found, with a rule before it -> add `text` as a new
      alternative to that previous rule's trailing regex group.
    - Catch-all rule found, with no rule before it -> insert the template
      rule ('nix', r'^(nix)$') right before the catch-all rule.
    """
    fuzzy_map_file = Path(file_rule_path)
    if not fuzzy_map_file.exists():
        return

    content = fuzzy_map_file.read_text(encoding="utf-8")

    entries = get_fuzzy_map_entries(content)
    if not entries:
        return

    catch_all_index = find_catch_all_index(content, entries)
    if catch_all_index is None:
        # No catch-all rule present -> do nothing
        return

    if catch_all_index > 0:
        # There is a rule before the catch-all -> modify it
        prev_start, prev_end = entries[catch_all_index - 1]
        add_variant_to_rule(fuzzy_map_file, content, prev_start, prev_end, text)
    else:
        # No rule before the catch-all -> insert a template rule
        catch_all_start, _ = entries[catch_all_index]
        insert_template_rule(fuzzy_map_file, content, catch_all_start, text)
