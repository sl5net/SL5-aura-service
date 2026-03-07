# Zsh Funktion: s() - KI-Client mit adaptivem Timeout

Englisch (Englisch)
Zweck

Diese Zsh-Funktion(en) fungieren als Wrapper für den Python-Client (cli_client.py) und implementieren eine robuste Fehlerbehandlung und eine adaptive Timeout-Strategie. Es ist darauf ausgelegt, Dienstverbindungsfehler schnell zu erkennen und sicherzustellen, dass vollständige KI-Antworten (bis zu 70 Sekunden) erfasst werden.
Schlüssellogik

Aus Gründen der Robustheit stützt sich die Funktion auf zwei Shell-Funktionen:

Timeout: Verhindert, dass das Skript auf unbestimmte Zeit hängen bleibt, und ermöglicht eine schnelle Fehlererkennung.

mktemp / Temporäre Dateien: Umgeht Probleme mit der Pufferung der Shell-Ausgabe, indem die Ausgabe des Skripts nach der Beendigung aus einer Datei gelesen wird.

Verwendung
Code Bash

  
s <Ihr Fragetext>
# Beispiel: s Computer Guten Morgen

  
  
### Quelle
__CODE_BLOCK_0__