# Motivation: Warum „Disk Wins“?

## Das Problem im Aura-Oma-Modus

In [Aura Oma Mode](../../../GettingStarted.i18n/GettingStarted-delang.md) (siehe Zeile 67) arbeitet Aura weitgehend autonom:
Der Benutzer spricht Befehle und Aura schreibt selbstständig in Dateien –
Konfigurationen, Skripte, Protokolleinträge, generierter Text.

Das folgende Szenario passiert ständig:

1. Der Benutzer hat eine Datei im Editor geöffnet (z. B. eine Regeldatei oder ein Skript).
2. Sie vergessen, dass der Editor noch aktiv ist und sprechen einen Aura-Befehl.
3. Aura ändert die Datei auf der Festplatte.
4. Der Redakteur erkennt die externe Änderung – und **fragt nach**.

Diese Aufforderung ist ein **Showstopper** im Oma-Modus:
- Der Benutzer sitzt möglicherweise auf der Couch und verwendet die Spracheingabe.
und kann den Dialog weder sehen noch erreichen.
- Oder sie haben versehentlich eine Taste im Editor gedrückt, der Puffer ist nun da
„modifiziert“, und jede externe Änderung blockiert mit einem
„Neu laden? / Lokal bleiben?“ Dialog.
- Das Ergebnis: Aura funktioniert weiter, aber der Editor zeigt eine veraltete Version an.
Der Benutzer denkt, dass er sich die aktuelle Datei ansieht, basiert jedoch auf Änderungen
auf einem alten Stand – Chaos ist garantiert.

## Was wir brauchen

Editor-Verhalten, das **immer die Festplatte priorisiert**.
Wenn Aura (oder ein anderes Tool) die Datei ändert, muss der Editor dies tun
sofort und **ohne Aufforderung** den neuen Inhalt anzeigen.
Nicht gespeicherte Eingaben im Editor können stillschweigend verworfen werden – weil in
Im Oma-Modus ist Aura die Quelle der Wahrheit, nicht die menschliche Tastatureingabe.

## Warum Standardeditoren scheitern

Fast alle gängigen Editoren (Kate, VS Code, Sublime Text, Notepad++,
Emacs, Vim, CudaText verfügen standardmäßig über einen Schutzmechanismus:
Sobald der Puffer nicht gespeicherte Änderungen enthält, fragen sie **immer** nach
wenn eine äußere Veränderung eintritt. Dies ist eine normale Funktion
Entwicklerarbeit – aber ein Fehler für den Aura Oma-Modus.

Dieses Plugin schließt genau diese Lücke für CudaText.

## Zielgruppe

- Benutzer des Aura Oma-Modus, die parallel Dateien in einem Editor anzeigen.
- Automatisierungsszenarien, in denen ein Prozess Dateien und einen Editor schreibt
dient nur als Live-Viewer.
- Jeder, für den „Festplatte gewinnt immer“ das gewünschte Verhalten ist.