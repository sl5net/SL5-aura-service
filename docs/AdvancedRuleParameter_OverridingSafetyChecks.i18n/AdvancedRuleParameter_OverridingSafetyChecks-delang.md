# SL5 Aura Rule Engine-Dokumentation

## Erweiterter Regelparameter: Überschreiben von Sicherheitsprüfungen

In einigen Szenarien (z. B. hochzuverlässige interne Befehle oder einfache, hochzuverlässige Eingaben) möchten Benutzer möglicherweise die Ausführung von Nachverarbeitungsschritten (wie „fuzzyRules“) erzwingen, selbst wenn die Systemzuverlässigkeit in der anfänglichen Spracherkennung gering ist.

Standardmäßig verwendet SL5 Aura eine Sicherheitsleitplanke: Wenn die Eingabeänderungen hoch sind („LT_SKIP_RATIO_THRESHOLD“), werden Nachbearbeitungswerkzeuge übersprungen, um unzuverlässige Korrekturen/Halluzinationen zu verhindern und aus Leistungsgründen.


Um diese Sicherheitsprüfung für eine bestimmte Regel zu deaktivieren, fügen Sie die Kennung zum Parameter „skip_list“ hinzu:

__CODE_BLOCK_0__