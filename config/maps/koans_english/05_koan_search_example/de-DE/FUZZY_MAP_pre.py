# config/maps/koans_english/05_koan_search_example/de-DE/FUZZY_MAP_pre.py
# using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite

import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first.
# 2. If no regex matches, a simple fuzzy match is performed.

CONFIG_DIR = Path(__file__).parent

introduction = """
For this technical demonstration, we require a complex, publicly available dataset in a standard format (SQLite). In this context, the Bible serves merely as a well-known, freely available, and multifaceted example document to illustrate database queries and research logic.

I want to emphasize that this unit is not about theological or religious content. Our focus is purely on the implementation and application of analyzing structured text data.

The key point is the availability of such data. Many historical and cultural texts are fortunately available as open-source datasets, which enables our technical work. We could just as easily analyze a legal compendium or a scientific journal here.
"""

FUZZY_MAP_pre = [
    # TODO: Activate the line below by removing the comment symbol '#'
    #('search in Ruth chapter 1 verse 1', fr'^.*$', 90, {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    # EXAMPLE: search in [book] chapter [number] verse [number]
    ('(bible) search', fr'^search in (?P<book>\w*[ ]?\w+) chapter (?P<chapter>\d+) [v]\w+ (?P<verse>\d+)$', 90,
    {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # TODO: Can you invent other search patterns ?

]
