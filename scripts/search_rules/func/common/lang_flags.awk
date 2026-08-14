# scripts/search_rules/func/common/lang_flags.awk
# Maps a language-region folder segment (e.g. /de-DE/) in short_path to
# a flag emoji, for display in the FZF rule search list. Included via a
# second -f argument alongside the main AWK_SCRIPT in run_rule.sh, and
# invoked through the apply_lang_flags() function below.
#
# Since a path contains at most one language segment, this does a
# single regex match + array lookup instead of testing ~35 gsub
# patterns sequentially against the whole string.
# Add new languages to LANG_FLAG[] below; no changes needed in run_rule.sh.

BEGIN {
    # English / North America
    LANG_FLAG["en-US"] = "🇺🇸";
    LANG_FLAG["en-GB"] = "🇬🇧";
    LANG_FLAG["en-CA"] = "🇨🇦";
    LANG_FLAG["en-AU"] = "🇦🇺";
    LANG_FLAG["es-MX"] = "🇲🇽";

    # Europe
    LANG_FLAG["de-DE"] = "🇩🇪";
    LANG_FLAG["de-AT"] = "🇦🇹";
    LANG_FLAG["de-CH"] = "🇨🇭";
    LANG_FLAG["fr-FR"] = "🇫🇷";
    LANG_FLAG["es-ES"] = "🇪🇸";
    LANG_FLAG["it-IT"] = "🇮🇹";
    LANG_FLAG["nl-NL"] = "🇳🇱";
    LANG_FLAG["pl-PL"] = "🇵🇱";
    LANG_FLAG["pt-PT"] = "🇵🇹";
    LANG_FLAG["ru-RU"] = "🇷🇺";
    LANG_FLAG["tr-TR"] = "🇹🇷";
    LANG_FLAG["uk-UA"] = "🇺🇦";
    LANG_FLAG["sv-SE"] = "🇸🇪";
    LANG_FLAG["da-DK"] = "🇩🇰";
    LANG_FLAG["fi-FI"] = "🇫🇮";
    LANG_FLAG["no-NO"] = "🇳🇴";
    LANG_FLAG["cs-CZ"] = "🇨🇿";
    LANG_FLAG["el-GR"] = "🇬🇷";

    # Latin America
    LANG_FLAG["pt-BR"] = "🇧🇷";
    LANG_FLAG["es-AR"] = "🇦🇷";
    LANG_FLAG["es-CL"] = "🇨🇱";
    LANG_FLAG["es-CO"] = "🇨🇴";

    # Asia & Middle East
    LANG_FLAG["ja-JP"] = "🇯🇵";
    LANG_FLAG["zh-CN"] = "🇨🇳";
    LANG_FLAG["zh-TW"] = "🇹🇼";
    LANG_FLAG["ko-KR"] = "🇰🇷";
    LANG_FLAG["hi-IN"] = "🇮🇳";
    LANG_FLAG["th-TH"] = "🇹🇭";
    LANG_FLAG["vi-VN"] = "🇻🇳";
    LANG_FLAG["ar-SA"] = "🇸🇦";
    LANG_FLAG["he-IL"] = "🇮🇱";
}

# Replaces a single /xx-XX/ language segment in short_path with its flag
# emoji. Returns short_path unchanged if no segment is found or the
# code has no mapping. One match() + one array lookup, not ~35 gsub scans.
function apply_lang_flags(short_path,    pos, code, flag) {
    pos = match(short_path, /\/[a-z][a-z]-[A-Z][A-Z]\//);
    if (pos == 0) return short_path;

    code = substr(short_path, pos + 1, 5);
    flag = LANG_FLAG[code];
    if (flag == "") return short_path;

    return substr(short_path, 1, pos - 1) flag substr(short_path, pos + RLENGTH);
}
