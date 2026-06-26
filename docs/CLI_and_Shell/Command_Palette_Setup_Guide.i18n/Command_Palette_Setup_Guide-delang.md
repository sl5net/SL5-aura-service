# Befehlspalette und Kartensuchanleitung

In dieser Anleitung wird erläutert, wie Sie die systemweite, standortunabhängige **Befehlspalette** für SL5 Aura einrichten und verwenden. Es ermöglicht Ihnen, Ihre Kartenregeln interaktiv zu durchsuchen, Live-Ausführungsvorschauen aus dem lokalen SQLite-Cache anzuzeigen und die ausgewählte Ausgabe sofort an Ihrem aktiven Cursor einzugeben.

## Voraussetzungen

Stellen Sie sicher, dass die folgenden Hintergrunddienste und Tools installiert und aktiv sind:
1. **`fzf`** (Fuzzy Finder)
2. **CopyQ** (Zwischenablage-Manager, wird für die globale Hotkey-Orchestrierung verwendet)
3. **`type_watcher.sh`** (Aura-Hintergrund-Typing-Daemon)

---

## CopyQ Global Shortcut-Setup

Um die Befehlspalette sofort aus jedem aktiven Fenster (z. B. Ihrem Browser oder Texteditor) zu starten, konfigurieren Sie einen globalen Hotkey in CopyQ:

1. Öffnen Sie **CopyQ** und drücken Sie „F6“ (oder gehen Sie zu **Befehle** / **Befehle**).
2. Klicken Sie auf **Hinzufügen** (Hinzufügen) und nennen Sie es „Aura Command Palette“.
3. Legen Sie die gewünschte **Globale Verknüpfung** fest (z. B. „Meta+S“ oder „Strg+Alt+S“).
4. Stellen Sie den **Typ** auf „Befehl“ (Befehl) ein.
5. Fügen Sie den folgenden JavaScript-Code in das Befehlsfeld ein:

__CODE_BLOCK_0__