# scripts/search_rules/func/common/lang_flags.awk
# Maps language-region folder segments (e.g. /de-DE/) in short_path to
# flag emoji, for display in the FZF rule search list. Included via a
# second -f argument alongside the main AWK_SCRIPT in run_rule.sh, and
# invoked through the apply_lang_flags() function below.
# Add new languages here; no changes needed in run_rule.sh.

function apply_lang_flags(short_path,    _sp) {
    _sp = short_path;

    # English / North America
    gsub(/\/en-US\//, "🇺🇸", _sp);
    gsub(/\/en-GB\//, "🇬🇧", _sp);
    gsub(/\/en-CA\//, "🇨🇦", _sp);
    gsub(/\/en-AU\//, "🇦🇺", _sp);
    gsub(/\/es-MX\//, "🇲🇽", _sp);

    # Europe
    gsub(/\/de-DE\//, "🇩🇪", _sp);
    gsub(/\/de-AT\//, "🇦🇹", _sp);
    gsub(/\/de-CH\//, "🇨🇭", _sp);
    gsub(/\/fr-FR\//, "🇫🇷", _sp);
    gsub(/\/es-ES\//, "🇪🇸", _sp);
    gsub(/\/it-IT\//, "🇮🇹", _sp);
    gsub(/\/nl-NL\//, "🇳🇱", _sp);
    gsub(/\/pl-PL\//, "🇵🇱", _sp);
    gsub(/\/pt-PT\//, "🇵🇹", _sp);
    gsub(/\/ru-RU\//, "🇷🇺", _sp);
    gsub(/\/tr-TR\//, "🇹🇷", _sp);
    gsub(/\/uk-UA\//, "🇺🇦", _sp);
    gsub(/\/sv-SE\//, "🇸🇪", _sp);
    gsub(/\/da-DK\//, "🇩🇰", _sp);
    gsub(/\/fi-FI\//, "🇫🇮", _sp);
    gsub(/\/no-NO\//, "🇳🇴", _sp);
    gsub(/\/cs-CZ\//, "🇨🇿", _sp);
    gsub(/\/el-GR\//, "🇬🇷", _sp);

    # Latin America
    gsub(/\/pt-BR\//, "🇧🇷", _sp);
    gsub(/\/es-AR\//, "🇦🇷", _sp);
    gsub(/\/es-CL\//, "🇨🇱", _sp);
    gsub(/\/es-CO\//, "🇨🇴", _sp);

    # Asia & Middle East
    gsub(/\/ja-JP\//, "🇯🇵", _sp);
    gsub(/\/zh-CN\//, "🇨🇳", _sp);
    gsub(/\/zh-TW\//, "🇹🇼", _sp);
    gsub(/\/ko-KR\//, "🇰🇷", _sp);
    gsub(/\/hi-IN\//, "🇮🇳", _sp);
    gsub(/\/th-TH\//, "🇹🇭", _sp);
    gsub(/\/vi-VN\//, "🇻🇳", _sp);
    gsub(/\/ar-SA\//, "🇸🇦", _sp);
    gsub(/\/he-IL\//, "🇮🇱", _sp);

    return _sp;
}
