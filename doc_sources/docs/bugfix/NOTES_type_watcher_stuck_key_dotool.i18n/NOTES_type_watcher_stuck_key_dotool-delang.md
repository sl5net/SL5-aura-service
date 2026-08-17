# Hinweise: type_watcher.sh-Problem mit hängengebliebenen Tasten (dotool)

## Symptom
Kurz nach einem Manjaro-Neustart, beim ersten Diktat nach „sl5net Aura“.
automatisch gestartet, ein einzelnes Zeichen blieb hängen und wiederholte sich unendlich
(z. B. „n“ hunderte Male wiederholt), bis die Auslösetaste gedrückt wurde
noch einmal als manuelle Problemumgehung.

Einmal gesehen am 21.07.2026 ~09:44 (Di), Text: „Die Ideen niemand wird
mehr gefragt, aber es soll trotzdem genauso sein wie...nnnnn...".

## Zeitleiste (über Protokolle nachgewiesen)
- 09:29:17 - `type_watcher.sh` gestartet (log/type_watcher.log)
- 09:41:56 - Diktat „Ideen niemand wird mehr gefragt...“ erhalten
(log/aura_engine.log, Thread-13/14)
- 09:42:03 – Textverarbeitung abgeschlossen („bester Fuzzy-Score: 0 %“),
vermutlich in eine `tts_output_*.txt`-Datei geschrieben
- ~09:42:04-09:42:09 - „type_watcher.sh“ ist abgestürzt (abgeleitet: Watchdog
Das Abfrageintervall beträgt 5 Sekunden, siehe unten.)
- 09:42:09 – Watchdog-Protokoll (log/type_watcher_keep_alive.log):
„WATCHDOG: ‚type_watcher.sh‘ läuft nicht. Starte es jetzt.“
- 09:42:13 - `type_watcher.sh` neu gestartet (log/type_watcher.log)
- Für die Datei „ideen niemand…“ war kein Eintrag „typisierter Inhalt von ...“ vorhanden
jemals in log/type_watcher.log gefunden – die Typisierung dieses spezifischen
Text wurde nie vervollständigt/protokolliert.

## Status der Grundursache
- BESTÄTIGT: „type_watcher.sh“ stürzte zwischen dem Fertigstellen des Textes ab
Verarbeitung (09:42:03) und der Watchdog erkennt, dass es nicht läuft
(09:42:09). Der Watchdog („type_watcher_keep_alive.sh“) tötet nur
und startet bei einer Änderung des Zeitstempels der Konfigurationsdatei (`ts1`/`ts2`,
(bei diesem Vorfall unverändert bestätigt) oder startet automatisch neu, wenn
`pgrep -f "type_watcher.sh"` findet keinen Prozess – d.h. das war sehr
wahrscheinlich ein Selbstunfall, kein äußerer Tod.
- HYPOTHESE (nicht bewiesen): `set -euo pipefail` (type_watcher.sh Zeile 5)
hat dazu geführt, dass das Skript bei einem Exit-Code ungleich Null innerhalb von beendet wurde
Pipeline, möglicherweise während die „dotool“-Pipe von „do_type()“ (Zeile 125) war
mitten im Stream. Wenn der Bash-Prozess beim Streamen in „dotool“ abstürzt,
der separate „dotoold“-Daemon (der unabhängig weiterläuft)
kann mit einem Schlüssel im „unten“-Zustand belassen werden, ohne dass jemals ein passender „oben“-Zustand vorhanden ist
empfangen, was zu einer Tastenwiederholung auf Betriebssystemebene führt.
- NOCH NICHT BEWIESEN: Der genaue Befehl/die genaue Zeile, die den Wert ungleich Null verursacht hat
Beenden Sie unter „set -euo pipefail“. Kein Fehler vom Absturz
Der Prozess „type_watcher.sh“ wurde erfasst (der Watchdog ruft ihn auf).
ohne Ausgabeumleitung, `type_watcher_keep_alive.sh` Zeile 79).
- Der betroffene Schlüssel war NICHT immer das gleiche Zeichen über verschiedene hinweg
Vorkommen dieses Fehlers (Benutzerbericht: zuvor auch „t“).

## Bereits untersucht und ausgeschlossen
– Kein durch eine Konfigurationsänderung ausgelöster Neustart (bestätigt durch Benutzer: config
unverändert, und die Prüfung „ts1_old != ts1_new“ würde „Konfiguration geändert“ protokollieren).
- Kein doppelter Autostart von „type_watcher.sh“, der sich mit überschneidet
selbst (nur ein „Hello from Watcher“-Eintrag ging dem Absturz voraus).
- Der „dotool type“-Aufruf von „do_type()“ ist pro Aufruf atomar und funktioniert auch
sendet nicht selbst die Taste pro Zeichen nach unten/oben – schließt „type_watcher.sh“ aus
Anwendungslogik als direkte Ursache für einen feststeckenden Schlüssel im Normalfall
(absturzfreier) Betrieb.

## Fix wurde bereits angewendet (Fallback/Abhilfe, keine Fehlerbehebung der Grundursache)
Sowohl „cleanup()“ in „type_watcher.sh“ als auch „do_cleanup()“ in
„keep-keys-up.sh“ gab bisher nur Zusatztasten (Umschalt, Strg,
alt usw.) über `dotool`/`xdotool`. Für einen festsitzenden Stammgast hat das nichts gebracht
Schlüssel (Buchstabe, Zahl, Satzzeichen).

- „type_watcher.sh“: „cleanup()“ sendet jetzt „dotool key <name>:up“ für
Alle Buchstaben, Zahlen und üblichen Satzzeichen/Leerzeichen, nicht
nur Modifikatoren.
- „type_watcher.sh“: „INPUT_METHOD“ wird jetzt nach der Erkennung exportiert, also
Andere Skripte können sehen, welches Backend („dotool“ / „xdotool“) aktiv ist.
- „keep-keys-up.sh“: „do_cleanup()“ hat einen „dotool“-Zweig erhalten (mithilfe von
„keyup“-Verb, keine Verzögerung pro Taste, für die Leistung) nur aktiv, wenn
„INPUT_METHOD=dotool“ spiegelt den vorhandenen „xdotool keyup“-Aufruf wider
für Modifikatoren.

Dadurch wird der zugrunde liegende Absturz von „type_watcher.sh“ nicht behoben; es nur
stellt sicher, dass ein festsitzender Schlüssel freigegeben wird, wenn der Absturz erneut auftritt
der nächste Bereinigungsdurchlauf („--cleanup“, aufgerufen nach jedem „do_type()“ und
über den „Trap Cleanup EXIT INT TERM“-Handler) statt zu wiederholen
auf unbestimmte Zeit, bis ein manueller Auslöser-Tastendruck erfolgt.

## Nächste Schritte, falls dies erneut passiert
- Erfassen Sie stderr von „type_watcher.sh“ bei einem Absturz. Momentan
`type_watcher_keep_alive.sh` Zeile 79 ruft es ohne Umleitung auf, also
Jede Bash-Fehlermeldung geht verloren (geht an den Watchdog).
stdout/stderr, wo immer dies vom Autostart-Mechanismus vorgegeben wird).
- Erwägen Sie einen Debug-Modus, z. `bash -x scripts/type_watcher/type_watcher.sh
2>> log/type_watcher_debug.log`, umgeschaltet über eine Umgebungsvariable wie z
`TYPE_WATCHER_DEBUG=1`, um die genaue fehlerhafte Zeile in der nächsten zu erfassen
Absturz.
- Überprüfen Sie, was „type_watcher_keep_alive.sh“ beim Manjaro-Boot startet
(Autostart-Datei „.desktop“, systemd-Einheit „--user“ usw.) und ob
seine stdout/stderr werden überall erfasst.
- Wenn reproduzierbar, testen Sie, ob der Absturz damit zusammenhängt
„dotoold“ initialisiert sich immer noch direkt nach dem Booten (siehe „sleep 0.1“)
in type_watcher.sh Zeile 8 und die `dotoold`-Startschleife in Zeilen
102-110).