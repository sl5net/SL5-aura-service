# Berühmte Mathematiker – STT-Korrekturleitfaden

## Das Problem

Spracherkennungssysteme (STT) wie Vosk verstehen oft Namen berühmter Mathematiker falsch oder schreiben sie falsch.
Dies kommt besonders häufig bei deutschen Namen vor, die Sonderzeichen (ß, ü, ä, ö) enthalten.
oder aus anderen Sprachen entlehnte Namen.

## Häufige STT-Fehler

| Gesprochene / STT-Ausgabe | Richtige Schreibweise | Notizen |
|---|---|---|
| Gaus, Gauss | Gauß | Deutscher Mathematiker, ß fehlt oft |
| Öler, Oyler | Euler | Schweizer, Name klingt auf Deutsch wie „Oiler“ |
| Leibnitz, Lipnitz | Leibniz | z am Ende, häufige Rechtschreibfehler |
| riman, riemann | Riemann | Doppel-n wird oft übersehen |
| hilbert | Hilbert | normalerweise richtig, nur Groß- und Kleinschreibung |
| Kantor | Kantor | normalerweise richtig, nur Groß- und Kleinschreibung |
| poincaré, poincaré | Poincaré | Akzent fehlt oft |
| noether, nöter | Noether | Umlaut wird oft übersehen |

## Beispielregeln

```python
FUZZY_MAP_pre = [
    ('Gauß', r'\bgau[sß]{1,2}\b', 0, {'flags': re.IGNORECASE}),
    ('Euler', r'\b(oiler|oyler|euler)\b', 0, {'flags': re.IGNORECASE}),
    ('Leibniz', r'\bleib(nitz|niz|nits)\b', 0, {'flags': re.IGNORECASE}),
    ('Riemann', r'\bri{1,2}e?mann?\b', 0, {'flags': re.IGNORECASE}),
    ('Noether', r'\bn[oö]e?th?er\b', 0, {'flags': re.IGNORECASE}),
]
```

## Warum Pre-LanguageTool?

Diese Korrekturen sollten in „FUZZY_MAP_pre.py“ (vor LanguageTool) erfolgen.
weil LanguageTool einen falsch geschriebenen Namen möglicherweise in ein anderes falsches Wort „korrigieren“ könnte.
Es ist besser, das Problem zuerst zu beheben und dann LanguageTool die Grammatik überprüfen zu lassen.

## Testen

Testen Sie nach dem Hinzufügen einer Regel mit der Aura-Konsole:
```
s euler hat die formel e hoch i pi plus eins gleich null bewiesen
```
Erwartet: „Euler hat die Formel e hoch i pi plus eins gleich null bewiesen“.