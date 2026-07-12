# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py
import ast
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

import libcst as cst



# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger.setLevel(logging.INFO)

log_dir = PROJECT_ROOT / "log"
log_dir.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(
    f"{log_dir}/{__name__}.log", mode="a", encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)


# ---------------------------------------------------------------------------
# TTS helper
# ---------------------------------------------------------------------------
def speak(text: str) -> None:
    """Speak text via a TTS engine and echo it to stdout."""
    print(text)
    logger.info("TTS speak: %s", text)
    try:
        subprocess.run(["espeak", "-v", "en-US", text], check=True)
    except Exception as exc:
        logger.warning("TTS fallback: %s — %s", text, exc)
        print(f"STDOUT (TTS fallback): {text}  —  {exc}")


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------
FUZZY_MAP_FILE = Path(__file__).parent / "de-DE" / "FUZZY_MAP_pre.py"


# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------
def _split_top_level_pipes(pattern: str) -> list[str]:
    parts = []
    buffer = []
    depth = 0
    for char in pattern:
        if char == "(":
            depth += 1
            buffer.append(char)
        elif char == ")":
            depth = max(0, depth - 1)
            buffer.append(char)
        elif char == "|" and depth == 0:
            parts.append("".join(buffer).strip())
            buffer = []
        else:
            buffer.append(char)
    parts.append("".join(buffer).strip())
    return parts


def _find_last_capturing_group(pattern: str) -> tuple[str, str, str] | None:
    depth = 0
    end = -1
    for i in range(len(pattern) - 1, -1, -1):
        char = pattern[i]
        if char == ")":
            if depth == 0:
                end = i
            depth += 1
        elif char == "(":
            depth -= 1
            if depth == 0 and end != -1:
                prefix = pattern[:i]
                core = pattern[i + 1 : end]
                suffix = pattern[end + 1 :]
                return prefix, core, suffix
    return None


def _build_new_pattern(old_pattern: str, new_variant: str) -> str | None:
    group = _find_last_capturing_group(old_pattern)
    if group:
        prefix, inner, suffix = group
        if "|" in inner:
            parts = _split_top_level_pipes(inner)
            if new_variant in parts:
                return None
            parts.append(new_variant)
            return f"{prefix}({'|'.join(parts)}){suffix}"
        if new_variant == inner.strip():
            return None
        return f"{prefix}({inner}|{new_variant}){suffix}"

    if "|" in old_pattern:
        parts = _split_top_level_pipes(old_pattern)
        if new_variant in parts:
            return None
        parts.append(new_variant)
        return "|".join(parts)

    has_start = old_pattern.startswith("^")
    has_end = old_pattern.endswith("$")
    body = old_pattern[1:-1] if (has_start and has_end) else old_pattern
    new_body = f"({body}|{new_variant})"
    return ("^" if has_start else "") + new_body + ("$" if has_end else "")


def _build_new_pattern_for_formatted_string_fragment(pattern_text: str, new_variant: str) -> str | None:
    """
    Special version for FormattedString fragments.
    The pattern_text may end with ')$' or similar suffixes that belong to the outer group.
    """
    last_paren = pattern_text.rfind(")")
    if last_paren == -1:
        if new_variant in pattern_text:
            return None
        return pattern_text + "|" + new_variant

    before_paren = pattern_text[:last_paren]
    after_paren = pattern_text[last_paren:]

    if "|" in before_paren:
        parts = _split_top_level_pipes(before_paren)
        if new_variant in parts:
            return None
        parts.append(new_variant)
        return "|".join(parts) + after_paren

    if new_variant == before_paren.strip():
        return None

    return f"{before_paren}|{new_variant}{after_paren}"


# ---------------------------------------------------------------------------
# libcst transformer
# ---------------------------------------------------------------------------
class FuzzyMapTransformer(cst.CSTTransformer):
    """
    Walks an assignment to FUZZY_MAP_pre and appends *new_variant* to the
    **first** regex pattern found inside a tuple at index 1.
    """

    def __init__(self, new_variant: str) -> None:
        super().__init__()
        self._new_variant = new_variant
        self._modified = False

    @property
    def modified(self) -> bool:
        return self._modified

    def leave_Assign(
        self, original_node: cst.Assign, updated_node: cst.Assign
    ) -> cst.Assign:
        if not self._is_fuzzy_map_target(original_node.targets):
            return updated_node

        rhs = original_node.value
        if not isinstance(rhs, cst.List) or not rhs.elements:
            return updated_node

        first = rhs.elements[0]
        updated_first = self._process_list_element(first)

        if not self._modified:
            return updated_node

        new_elements = [updated_first] + list(rhs.elements[1:])
        new_rhs = rhs.with_changes(elements=new_elements)
        return updated_node.with_changes(value=new_rhs)

    def _is_fuzzy_map_target(self, targets: list[cst.BaseExpression]) -> bool:
        for target in targets:
            if isinstance(target, cst.AssignTarget) and isinstance(
                target.target, cst.Name
            ):
                if target.target.value == "FUZZY_MAP_pre":
                    return True
        return False

    def _process_list_element(self, element: cst.BaseExpression) -> cst.BaseExpression:
        if not isinstance(element.value, cst.Tuple):
            return element

        tup = element.value
        if len(tup.elements) < 2:
            return element

        pattern_node = tup.elements[1].value

        # Handle SimpleString ('...' or r'...')
        if isinstance(pattern_node, cst.SimpleString):
            raw = pattern_node.value  # e.g. "r'^(nix|...)$'"
            try:
                pattern_text = ast.literal_eval(raw)
            except Exception:
                pattern_text = raw.strip("\"'")
                if pattern_text.startswith(("r'", "R'", 'r"', 'R"')):
                    pattern_text = pattern_text[2:]
                elif pattern_text.startswith(("u'", "U'", 'u"', 'U"')):
                    pattern_text = pattern_text[2:]
                elif pattern_text.startswith(("ur'", "UR'", 'ur"', 'UR"')):
                    pattern_text = pattern_text[3:]
            new_pattern = _build_new_pattern(pattern_text, self._new_variant)
            if new_pattern is None:
                return element

            new_literal = cst.SimpleString(f"r'{new_pattern}'")
            new_tuple_elements = list(tup.elements)
            new_tuple_elements[1] = tup.elements[1].with_changes(value=new_literal)
            new_tuple = tup.with_changes(elements=new_tuple_elements)
            self._modified = True
            return element.with_changes(value=new_tuple)

        # Handle FormattedString (f'...' or fr'...')
        elif isinstance(pattern_node, cst.FormattedString):
            return self._process_formatted_string_pattern(element, tup, pattern_node)

        return element

    def _process_formatted_string_pattern(
        self, element: cst.BaseExpression, tup: cst.Tuple, pattern_node: cst.FormattedString
    ) -> cst.BaseExpression:
        """
        Modify a FormattedString pattern by appending the new variant
        to the last FormattedStringText part, keeping expressions intact.
        """
        if not pattern_node.parts:
            return element

        last_text_idx = -1
        for i, part in enumerate(pattern_node.parts):
            if isinstance(part, cst.FormattedStringText):
                last_text_idx = i

        if last_text_idx == -1:
            return element

        last_text_part = pattern_node.parts[last_text_idx]
        pattern_text = last_text_part.value

        new_pattern_text = _build_new_pattern_for_formatted_string_fragment(
            pattern_text, self._new_variant
        )
        if new_pattern_text is None:
            return element

        new_parts = list(pattern_node.parts)
        new_parts[last_text_idx] = last_text_part.with_changes(value=new_pattern_text)

        new_formatted = pattern_node.with_changes(parts=new_parts)
        new_tuple_elements = list(tup.elements)
        new_tuple_elements[1] = tup.elements[1].with_changes(value=new_formatted)
        new_tuple = tup.with_changes(elements=new_tuple_elements)

        self._modified = True
        return element.with_changes(value=new_tuple)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def add_variant_to_fuzzy_map(file_path: Path, new_variant: str) -> bool:
    file_path = Path(file_path)
    logger.info("add_variant_to_fuzzy_map called: file=%s variant=%r", file_path, new_variant)

    if not file_path.exists():
        logger.error("File does not exist: %s", file_path)
        return False

    backup = file_path.with_suffix(file_path.suffix + ".bak")
    shutil.copy2(file_path, backup)
    logger.info("Backup created: %s", backup)

    source = file_path.read_text(encoding="utf-8")
    logger.info("Source file read: %d bytes", len(source))

    module = cst.parse_module(source)
    logger.info("CST module parsed successfully")

    transformer = FuzzyMapTransformer(new_variant)
    new_module = module.visit(transformer)

    if not transformer.modified:
        logger.warning("No modification made — variant %r may already exist", new_variant)
        return False

    new_src = new_module.code
    file_path.write_text(new_src, encoding="utf-8")
    logger.info("File written: %s (%d bytes)", file_path, len(new_src))
    return True


# ---------------------------------------------------------------------------
# Plugin entry point
# ---------------------------------------------------------------------------
def execute(match_data: dict) -> None:
    logger.info("execute() called with match_data keys: %s", list(match_data.keys()))

    text = match_data.get("original_text", "")
    logger.info("original_text: %r", text)

    if not text or "Lernmodus" in text:
        logger.info("Skipping — text empty or contains 'Lernmodus'")
        return None

    file_rule_path = match_data.get("text_after_replacement")
    logger.info("text_after_replacement (file_rule_path): %s", file_rule_path)

    if not text:
        logger.error("text is empty")
        print(f"ERROR: text is empty — {text!r}")
        return None

    if not file_rule_path:
        msg = (
            "ERROR: no file_rule_path in match_data. "
            "A catch-all rule may have intercepted this text. "
            "Run: python3 tools/find_catch_all_in_fuzzy_maps.py"
        )
        logger.error(msg)
        speak(msg)
        return None

    speak("collect unmatched")

    success = add_variant_to_fuzzy_map(file_rule_path, text)
    if success:
        logger.info("SUCCESS — exiting with code 1 to trigger reload")
        sys.exit(1)

    msg = (
        f"WARNING: Could not add {text!r} to {file_rule_path}. "
        "Run: python3 tools/find_catch_all_in_fuzzy_maps.py"
    )
    logger.warning(msg)
    speak(msg)
    return None