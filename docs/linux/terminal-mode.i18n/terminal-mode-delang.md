# Terminalmodus (Sprachausschluss)

Der Terminalmodus ist ein Konfigurationszustand, in dem keine spezifischen Sprachpakete für die Sprach-/Textverarbeitungseinheiten installiert oder konfiguriert sind.

## So aktivieren Sie
Wenn Sie während der Ersteinrichtung oder des Sprachauswahlskripts zur Angabe der **Primärsprache** aufgefordert werden, geben Sie Folgendes ein:
- `n`
- „keine“.
- `0`

## Effekte
- **EXCLUDE_LANGUAGES** ist auf „alle“ gesetzt.
- Es werden keine sprachspezifischen Modelle (wie Whisper- oder Vosk-Modelle) heruntergeladen oder initialisiert.
- Das System arbeitet im „Nur-Terminal“-Modus, was für Umgebungen mit wenig Speicherplatz nützlich ist oder wenn nur die wichtigsten CLI-Tools ohne lokalisierte Sprachunterstützung erforderlich sind.

## Umgebungsvariablen
Wenn aktiv, werden die folgenden Exporte generiert:
__CODE_BLOCK_0__