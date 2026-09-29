# Übergabeprotokoll: z_fallback_llm, CLI-Eingabe liefert keinen Witz

Stand: 2026-09-29

## 1- Aufgabe (Verständnis, noch nicht von dir mit "ja" bestätigt)

Ist-Zustand: Die CLI-Eingabe lautet exakt "Computer genau erzähle zwei Witze". Es erscheint kein Witz.

Soll-Zustand: Die Antwort des LLM erscheint direkt in der Konsole, nicht in einer Logdatei.

Nicht Teil der Aufgabe: Logging umbauen, Log-Zeilen kürzen oder verlängern, Cache-Verhalten ändern. Die Cache-Umgehung ("witz" im Input) ist bewusst so gewählt.

Der Nachfolger muss dieses Verständnis zuerst mit dir abgleichen und auf dein "ja" warten.

## 2- Umgebung

Manjaro Linux, ZSH, Branch feature/fallback-llm-lazy-install.

Ollama läuft unter http://localhost:11434 (Binary /usr/bin/ollama). Verfügbare Modelle: llama3.2:latest, qwen3:8b.

Der Ollama-Test per curl mit Modell llama3.2, stream:false, num_predict:100 und den Stop-Wörtern liefert eine gültige Antwort ("Warum ging der Computer zum Arzt? Weil er ein Virus hatte!"). Ollama, Modellname, Stop-Wörter und Token-Limit sind damit belegt nicht die Ursache. Der Testprompt war kürzer als der reale Prompt aus ask_ollama.py (ohne system_role, Verlauf und Aura-Suffix).

Konfiguration:

```
config/settings_local.py
```

Schlüssel: PLUGINS_ENABLED = {"z_fallback_llm": 1}. Zugriff über DynamicSettings().PLUGINS_ENABLED.get("z_fallback_llm", False).

Vorhandener Paket-Installer:

```
scripts/py/func/ensure_package.py
```

## 3- Ablauf der Kette (verifiziert aus Code-Ausschnitten)

Regeln:

```
config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
```

Regel 1 hat Priorität 10 und verlangt `{aura1}` plus Modus-Wort (normal, slow, flow, langsam, genau, gründlich). Regel 2 hat Priorität 100 und verlangt einen der Trigger Aura, Aurora, laura, dora, Ära, hurra, prora oder Computer, danach ein Leerzeichen und beliebigen Text. Beide rufen ask_ollama.py auf. Beide schließen Fenster wie firefox, chrome, brave und element aus.

Ausführung:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`execute()` nimmt die letzte Regex-Gruppe als Input und macht sie klein. Bei "witz" im Input wird `bypass_cache = True` gesetzt, der Cache-Check wird übersprungen. Danach folgt der Ollama-Request mit dem Modell llama3.2. Der Timeout beträgt 90 Sekunden. Frühe Rückgaben ohne Ollama-Request gibt es bei leerem Input ("Nichts gehört."), bei "vergiss alles", bei `check_static_guardrails()` und bei den Instant-Wörtern "sofort", "schnell", "instant".

CLI-Rückgabe:

```
scripts/py/service_api.py
```

Die Funktion liest die neueste Output-Datei und gibt ein Dict mit `status`, `result_text` und `input_text` zurück. Die Log-Zeile "API-CLI-Call: Finished" kürzt Input und Result auf 20 Zeichen. Das ist reine Log-Kürzung und keine Datenkürzung.

## 4- Beobachtetes Log der CLI-Eingabe

Im Log stehen nur `reload_performed` und "API-CLI-Call: Finished. Input='…Computer genau erzäh', Result='Computer genau erzäh'". Es fehlt jede Zeile von `execute()` (kein "Input:", kein "Cache BYPASS", kein "Unzensierte KI-Antwort").

Das belegt nicht, dass `execute()` nicht lief, weil:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

den FileHandler mit `mode='w'` öffnet. Die Datei ask_ollama.log wird bei jedem Import von `utils` überschrieben. `log_debug` schreibt außerdem auf stdout, also in die Konsole des Hauptprogramms.

## 5- Offene Fragen (nicht belegt)

1- Läuft `execute()` bei der CLI-Eingabe überhaupt?
2- Welche Regel matcht, Regel 1, Regel 2 oder keine?
3- Gibt der CLI-Client den Wert `result_text` in der Konsole aus?
4- Enthält die Output-Datei nur den Input oder auch eine Antwort? Die ersten 20 Zeichen von Input und Result sind identisch, mehr ist nicht sichtbar.
5- Wie lautet der exakte CLI-Aufruf, mit dem du den Text absetzt? Er wurde bisher nicht genannt.

## 6- Verworfene Hypothesen

1- Der Input kommt nicht gekürzt an, das war nur die 20-Zeichen-Kürzung im Log.
2- Ollama, Stop-Wörter und num_predict sind nicht die Ursache.
3- Der Cache ist bei "witz" bypassed und damit nicht die Ursache.

## 7- Gefundene Fehler außerhalb der Aufgabe (nichts ändern ohne Auftrag)

1- Datei:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

Nach `if not raw_text:` wird `response = answer_for_all_fallback` gesetzt. Die nächste Zeile überschreibt sie mit `clean_text_for_typing(raw_text)`. Bei leerer Ollama-Antwort bleibt die Antwort leer. Ebenso haben `response.replace('sl5_config.py', ...)` und `response.replace(' sl5_record_trigger.py ', ...)` keine Wirkung, weil das Ergebnis nicht zugewiesen wird.

2- Datei:

```
config/maps/plugins/internals/de-DE/aura_constants.py
```

Nach `Overlay` fehlt ein `|`, es entsteht die Variante `OverlayOrange`. Außerdem enthält `_variants` das Wort "Computer" nicht. Regel 1 kann "Computer genau ..." daher nicht matchen, Regel 2 kann es.

3- Datei:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'` überschreibt das Log bei jedem Import.

## 8- Nächste Schritte (erst nach deinem "ja")

Schritt A: Den CLI-Aufruf von dir erfragen, ohne Prompt-Zeichen.

Schritt B: Die Verarbeitung von `result_text` finden:

```
tools/search.sh "result_text" .
```

Schritt C: Die Konsolenausgabe nach der Eingabe prüfen. Dafür den vollständigen Text aus der Konsole des Hauptprogramms von dir anfordern.

Schritt D: Erst danach Änderungen vorschlagen, nur im Vorher/Nachher-Format.

## 9- Arbeitsregeln, die der Nachfolger einhalten muss

1- Kommunikation auf Deutsch. Code, Kommentare, Logs und Bezeichner ausschließlich auf Englisch, auch in Codeblöcken.
2- Keine Aussage über Systemzustand ohne Beleg aus deiner Ausgabe. Nichts raten, nichts rekonstruieren.
3- Neue Aufgabe: zuerst Verständnis schildern, auf dein "ja" warten.
4- Kein "Ich habe keinen Zugriff auf dein Repository"-Satz.
5- Repository-Suche nur über tools/search.sh mit den Optionen -i, -E und -w.
6- Bei Fehlern zuerst den vollständigen Traceback holen.
7- Befehle und Dateipfade stehen jeweils auf eigener Zeile, ohne Satzzeichen am Ende.
8- Nummerierung im Format 1-, 2-, 3-.
9- Codeänderungen nur als geänderte Zeilen im Vorher/Nachher-Format, ohne umgebenden Funktionscode.
10- Kein Python-Code mit führender Einrückung in Codeblöcken, stattdessen kleine Funktionen ohne Einrückung.
11- Keine absoluten, nutzerspezifischen Pfade und keine Zeilennummern ohne Dateipfad.
12- Keine Füllsätze, kein emotionaler Ton, ungefähr 1400 Zeichen pro Antwort als Ziel.
13- Von dir bereits ausgeführte Aktionen als erledigt behandeln.
14- Beim Kopieren von Ausgaben das Prompt-Zeichen nicht mitkopieren, sonst entsteht Exit-Code 127.
15- Commit zu Datum und Uhrzeit finden: ./tools/find-nearest-commit.sh "2026-07-28 17:00"
