# Regelattribut: `execute_only` (Experimentell, 7.7.'26 Di)

Das Attribut „execute_only“ ist eine experimentelle Konfigurationsoption, die für Regeln entwickelt wurde, die nur externe Skripte auslösen, ohne den Eingabetext zu ändern oder zu ersetzen.

## Übersicht
- **Typ:** „bool“ (z. B. „True“ oder „False“)
- **Primärer Anwendungsfall:** Wird normalerweise in Kombination mit „on_match_exec“ verwendet, um externe Skripte auszuführen.

## Funktionsweise und aktuelles Verhalten
- **Geschwindigkeitsoptimierung:** (nur einige Millisekunden) Umgeht Textnachbearbeitungs- und Textersetzungsroutinen und beschleunigt so die sofortige Ausführung der ausgelösten Aktion.
- **Kein Ausschluss-/Fall-Through-Nebeneffekt:** Das Setzen von „execute_only“ auf „True“ verhindert **nicht**, dass andere übereinstimmende Regeln denselben Eingabetext auswerten.
- **Fluss anhalten:** Wenn Sie verhindern müssen, dass nachfolgende Regeln denselben Eingabetext verarbeiten, müssen Sie den Ausführungsfluss derzeit manuell beenden (z. B. durch Auslösen einer Ausnahme am Ende Ihres ausgelösten Skripts oder Regelsatz-Handlers).

## Beispielkonfiguration

```python
# EXAMPLE: gather metal
('gather metal',
 r'^(gather\s*)?(met\w+|mat\w+|metall|mit|zitat|metal|matcha|günther)$',
 85,
 {
     'command_flags': re.IGNORECASE,
     'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
     'on_match_exec': [CONFIG_DIR / '..' / '0ad_actions.py'],
     'execute_only': True, # Experimental: Fast execution, does not halt the rule-chain.
 }),
```