# Aura Admin-Benutzeroberfläche

Mit der Admin-Benutzeroberfläche können Sie die Aura-Einstellungen in Ihrem Browser anzeigen und ändern, ohne dass Kosten für Leerlaufressourcen anfallen. Der Dashboard-Server wird beim Booten nicht ausgeführt. Es wird nur bei Bedarf gestartet, wenn es angefordert wird.

## So öffnen Sie (On-Demand)

Sie können das Admin-Dashboard mit einer der folgenden drei Methoden dynamisch starten und öffnen:

### 1. Sprachbefehl
Sprechen Sie einfach in Ihr Mikrofon:
* *„Aura-Verwaltung“

### 2. Terminal-/Konsolenbefehl
Wenn Sie im Terminal arbeiten, führen Sie diesen Befehl aus, um den Launcher direkt auszulösen:
```bash
s aura administration
```

*⚠️ **Plattformhinweis für Windows-/macOS-Benutzer:** Der kurze „s“-Befehlswrapper ist hauptsächlich für Linux-Umgebungen konfiguriert. Bitte lesen Sie dazu das Dokument. Wenn Sie Windows oder macOS verwenden, funktioniert der Befehl „s“ möglicherweise nicht sofort. Weitere Informationen zum Konfigurieren und Implementieren des Befehlsalias „s“ für Ihr Betriebssystem finden Sie in unserer offiziellen CLI-Setup-Dokumentation.*


### 3. Desktop-Verknüpfung
Um ein plattformspezifisches Desktopsymbol zu erstellen, führen Sie dieses Setup-Skript einmal aus:
```bash
python scripts/py/chat/install_shortcut.py
```
Doppelklicken Sie dann einfach auf das Symbol **Aura Admin Dashboard** auf Ihrem Desktop.

---

## Direkter Browserzugriff
Sobald der Server über eine der oben genannten On-Demand-Methoden gestartet wurde, können Sie jederzeit direkt in Ihrem Browser auf die Schnittstelle zugreifen:

http://localhost:8084

*(Sie können diesen Link gerne in Ihrem Browser als Lesezeichen speichern!)*

---

## Was Sie tun können

- Sehen Sie sich den Übersetzungsstatus für jede Schnittstelle an (Sprache, Terminal, Web).
- Aktivieren oder deaktivieren Sie die Übersetzung pro Schnittstelle.
- Wählen Sie die Zielsprache (Englisch, Französisch, Spanisch usw.).

## Schnittstellen

| Schnittstelle | Beschreibung |
|-----------|----------------------|
| Rede | Spracheingabe (Mikrofon) |
| Terminal | Befehlszeile (`s`-Befehl) |
| Web | Streamlit-Webchat (Port 8831) |

## Beispiel

Um nur Webbenutzer ins Englische zu übersetzen, lassen Sie Sprache und Terminal ausgeschaltet und aktivieren Sie Web mit der Sprache „en“.