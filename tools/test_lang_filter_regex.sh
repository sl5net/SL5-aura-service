#!/usr/bin/env bash
# tools/test_lang_filter_regex.sh
# Standalone test for the AWK language-folder filter regex used in
# scripts/search_rules/run_rule.sh. Extend TEST_CASES below as needed.
set -uo pipefail

# Each line: <current_lang>|<full_path>|<expected: match|nomatch>
TEST_CASES="
de-DE|/home/user/project/config/maps/plugins/game/0ad/signal/en-US/FUZZY_MAP.py|nomatch
de-DE|/home/user/project/config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP.py|match
en-US|/home/user/project/config/maps/plugins/game/0ad/signal/en-US/FUZZY_MAP.py|match
en-US|/home/user/project/config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP.py|nomatch
de-DE|/home/user/project/config/maps/plugins/game/0ad/common/FUZZY_MAP.py|neutral
"

AWK_TEST_SCRIPT='BEGIN {
    full_path = full_path_in;
    current_lang = current_lang_in;
    langpos = match(full_path, /[/][a-z][a-z]-[A-Z][A-Z][/]/);
    if (langpos > 0) {
        folder_lang = substr(full_path, langpos + 1, 5);
        if (folder_lang == current_lang) {
            print "match";
        } else {
            print "nomatch";
        }
    } else {
        print "neutral";
    }
}'

echo "=== Language filter regex test ==="
pass=0
fail=0

while IFS='|' read -r lang path expected; do
    [ -z "$lang" ] && continue
    result=$(awk -v full_path_in="$path" -v current_lang_in="$lang" "$AWK_TEST_SCRIPT" < /dev/null)
    if [ "$result" = "$expected" ]; then
        status="OK"
        pass=$((pass + 1))
    else
        status="FAIL"
        fail=$((fail + 1))
    fi
    printf "%-4s current_lang=%-6s expected=%-8s got=%-8s path=%s\n" "$status" "$lang" "$expected" "$result" "$path"
done <<< "$TEST_CASES"

echo "=== done ==="

