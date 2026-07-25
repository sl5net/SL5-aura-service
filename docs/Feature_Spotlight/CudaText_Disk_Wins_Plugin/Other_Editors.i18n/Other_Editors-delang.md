# Automatisches Neuladen in anderen Editoren

In diesem Dokument wird beschrieben, wie Sie das automatische Nachladen auf externen Geräten einrichten
Dateiänderungen in gängigen Editoren – und warum dies oft **nicht ausreicht**
im Aura-Oma-Modus.

---

## Kate (KDE)

### Aufstellen

1. **Einstellungen → Kate konfigurieren → Öffnen/Speichern → Erweitert**
2. Aktivieren Sie:
- **"Dateien automatisch neu laden"**

### Was funktioniert

- Wenn der Puffer **unverändert** ist, lädt Kate die Datei sofort neu.
- Für den reinen Betrachtungsmodus reicht dies aus.

### Was funktioniert **nicht** (und warum schlägt es im Oma-Modus fehl)

- Sobald Sie **eine einzelne Taste** im Puffer drücken (auch nur eine
Leerzeichen oder versehentlicher Tastendruck), gilt der Puffer als „geändert“.
- Von diesem Moment an fragt Kate **immer** bei jeder äußerlichen Veränderung:
> „Die Datei wurde extern verändert. Möchten Sie sie neu laden?“
- Im Oma-Modus befindet sich der Benutzer möglicherweise nicht am Computer oder sieht ihn nicht
Dialog – Aura schreibt weiter, aber der Editor bleibt bei der alten Version.
- **Kate hat keine Einstellung**, die nicht gespeicherte Pufferänderungen stillschweigend verwirft
zugunsten der Diskettenversion.

> **Fazit:** Kate ist für den Oma-Modus ungeeignet, sobald der Benutzer
> tippt versehentlich den Editor ein.

---

## VS-Code

### Aufstellen

In „settings.json“:

```json
{
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
```

### Einschränkungen

- „autoSave“ speichert den Puffer – es überschreibt Auras Änderungen mit
lokale Version, nicht umgekehrt.
– Für nicht gespeicherte Änderungen wird weiterhin eine Eingabeaufforderung angezeigt.
- Keine Option für „Festplatte gewinnt immer“.

---

## Emacs

```elisp
(global-auto-revert-mode t)
```

### Einschränkungen

- Lädt nur dann automatisch neu, wenn der Puffer unverändert ist.
– Fragt, wenn der Puffer geändert wird.

---

## Vim / Neovim

```vim
set autoread
au FocusGained,BufEnter,CursorHold * :checktime
```

### Einschränkungen

- „autoread“ lädt nur dann neu, wenn der Puffer unverändert ist.
- Überschreibt einen „geänderten“ Puffer nicht automatisch.

---

## CudaText (ohne Plugin)

In „user.json“:

```json
{
    "ui_notif": true,
    "ui_notif_confirm": 0
}
```

### Einschränkungen

- Alle Werte von „ui_notif_confirm“ (0–4) zeigen eine Art Eingabeaufforderung –
modal oder modallos.
- Es gibt **keinen** Wert, der bedeutet: „Sofort neu laden, nie fragen.“
- Daher ist das Plugin „cuda_disk_wins“ erforderlich.

---

## Übersicht

| Herausgeber | Automatisches Neuladen (unverändert) | Automatisches Neuladen (geändert) | Lizenz |
|--------|-----------|-----------------------|---------|
| Kate | Ja | Immer Aufforderungen | Open Source |
| VS-Code | Ja | Immer Aufforderungen | Open Source |
| Erhabener Text | Ja | Immer Aufforderungen | Proprietär |
| Emacs | Ja | Immer Aufforderungen | Open Source |
| Vim | Ja | Immer Aufforderungen | Open Source |
| CudaText (kein Plugin) | Ja | Immer Aufforderungen | Open Source |
| **CudaText + Disk gewinnt** | Ja | **Keine Aufforderung** | Open Source |

---

## Warum kein Redakteur dies sofort erledigen kann

Das stille Verwerfen nicht gespeicherter Änderungen gilt als **massiver Datenverlust
Fehler** in der Softwareentwicklung. Kein seriöser Editor bietet eine Einstellung an
„Überschreibe meinen Puffer, ohne zu fragen“. Das ist richtig und wichtig –
für normale Entwicklerarbeit.

Im Aura-Oma-Modus ist die Priorität jedoch umgekehrt: Aura ist die Quelle
der Wahrheit, und der Puffer des menschlichen Editors ist zweitrangig. Deshalb ein
Um dieses Verhalten zu erzwingen, ist ein expliziter Plugin-Eingriff erforderlich
diesen speziellen Anwendungsfall.