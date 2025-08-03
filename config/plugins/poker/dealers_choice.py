# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# config/plugins/poker/dealers-choice.py
import re

# (key, regex, confidence_threshold, flags)
COMMAND_MAP = [
    # Action keys
    ('c', r'^\s*(call|check)\s*$', 50, re.IGNORECASE),
    ('r', r'^\s*(raise)\s*$', 50, re.IGNORECASE),
    ('f', r'^\s*(fold)\s*$', 50, re.IGNORECASE),
    ('d', r'^\s*(discard)\s*$', 50, re.IGNORECASE),
    ('b', r'^\s*(bet)\s*$', 50, re.IGNORECASE),
    ('x', r'^\s*(exchange)\s*$', 50, re.IGNORECASE),
    # Amount keys
    ('1', r'^\s*(100|one hundred)\s*$', 50, re.IGNORECASE),
    ('2', r'^\s*(250|two fifty)\s*$', 50, re.IGNORECASE),
    ('3', r'^\s*(50|fifty)\s*$', 50, re.IGNORECASE),
]
