### FAQ (Deutsch) 3.8.'2025 Sun

**1. F: Was ist SL5 Aura?**
A: Es ist ein systemweites Offline-Spracherkennungsprogramm. Sie können damit in jede beliebige Anwendung auf Ihrem Computer (Windows, macOS, Linux) diktieren, ohne eine Internetverbindung zu benötigen.

F: Is offline Spracherkennung Alexa/Siri und konsorten?
A: Gute Frage. Nein, es ist das genaue Gegenteil. Alexa/Siri sind cloudbasiert. Die Sprachdaten werden zur Verarbeitung an deren Server gesendet. offline: alles passiert sicher auf dem Gerät des Nutzers. Das ist der entscheidende Vorteil für den Datenschutz.

**2. F: Warum sollte ich das nutzen? Was ist das Besondere?**
A: **Datenschutz.** Ihre Sprachdaten werden zu 100 % auf Ihrem lokalen Rechner verarbeitet und niemals in die Cloud gesendet. Das macht es absolut privat und DSGVO-konform.

**3. F: Ist es kostenlos?**
A: Ja, die Community Edition ist vollständig kostenlos und Open-Source. Den Code und den Installer finden Sie auf unserem GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. F: Was brauche ich, um es zu verwenden?**
A: Einen Computer und ein Mikrofon. Für die beste Genauigkeit empfehlen wir dringend ein gutes Headset-Mikrofon anstelle des eingebauten Laptop-Mikrofons.

**5. F: Die Genauigkeit ist nicht perfekt. Wie kann ich sie verbessern?**
A: Versuchen Sie, deutlich, in gleichmäßiger Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und ein besseres Mikrofon machen den größten Unterschied.

--------------------------> Hier könnten wir erwähnen, dass wir verschiedene FuzzyMaps mit denen man die Genauigkeit erheblich verbessern kann oder sogar eigene Sprachen entwerfen kann






#### **Teil 1: Allgemeine Fragen**

**F: Was ist SL5 Auro?**
A: SL5 Auro ist ein systemweites Offline-Spracherkennungsprogramm. Es ermöglicht Ihnen, Text in jede beliebige Anwendung auf Ihrem Computer (z. B. E-Mail-Programm, Textverarbeitung, Code-Editor) zu diktieren, ohne eine Internetverbindung zu benötigen.

**F: Was bedeutet "offline" und warum ist das wichtig?**
A: "Offline" bedeutet, dass die gesamte Sprachverarbeitung direkt auf Ihrem Computer stattfindet. Ihre Sprachdaten werden **niemals** an einen Cloud-Server (wie Google, Amazon oder OpenAI) gesendet. Dies bietet maximale Privatsphäre und Sicherheit, ideal für vertrauliche Informationen (z. B. für Anwälte, Ärzte, Journalisten) und ist vollständig konform mit Datenschutzverordnungen wie der DSGVO.

**F: Ist es wirklich kostenlos? Wo ist der Haken?**
A: Die "Community Edition" ist zu 100 % kostenlos und Open-Source. Es gibt keinen Haken. Wir glauben an die Stärke von Open-Source-Tools. Wenn Sie die Software nützlich finden und ihre Weiterentwicklung unterstützen möchten, können Sie dies über unsere [Ko-fi Seite](https://ko-fi.com/sl5) tun.

**F: Für wen ist diese Software gedacht?**
A: Für jeden, der viel schreibt und seine Effizienz steigern möchte: Autoren, Studenten, Programmierer, Juristen und Mediziner, Menschen mit körperlichen Einschränkungen oder jeder, der einfach lieber spricht als tippt.

#### **Teil 2: Installation & Einrichtung**

**F: Welche Betriebssysteme werden unterstützt?**
A: Die Software wurde erfolgreich auf Windows 11, Manjaro Linux und Ubuntu und macOS getestet.

**F: Wie installiere ich es unter Windows?**
A: Wir bieten ein einfaches Ein-Klick-Installationsprogramm. Es ist ein Batch-Skript, das Administratorrechte benötigt, um die Umgebung einzurichten und die notwendigen Modelle herunterzuladen. Einmal ausgeführt, erledigt es alles für Sie.

**F: Der Download für die Modelle ist sehr groß. Warum?**
A: Die Spracherkennungsmodelle ermöglichen es der Software, offline zu arbeiten. Sie enthalten alle Daten, die die KI benötigt, um Ihre Sprache zu verstehen. Größere, präzisere Modelle können mehrere Gigabyte groß sein. Unser neuer Downloader teilt diese in kleinere, überprüfbare Teile auf, um einen zuverlässigen Download zu gewährleisten.

**F: Ich bin auf Linux. Wie gehe ich vor?**
A: Unter Linux klonen Sie typischerweise das Repository von GitHub und führen ein Setup-Skript wie aus. Dieses Skript erstellt eine virtuelle Python-Umgebung, installiert Abhängigkeiten und startet den Diktier-Dienst.

**F: Wenn ich unter Windows auf eine `.py`-Datei doppelklicke, öffnet sie sich im Texteditor. Wie führe ich sie aus?**
A: Das ist ein häufiges Windows-Problem, bei dem `.py`-Dateien nicht dem Python-Interpreter zugeordnet sind. Sie sollten die einzelnen Python-Skripte nicht direkt ausführen. Verwenden Sie immer das bereitgestellte Haupt-Startskript (z.B. eine `.bat`-Datei), da dieses sicherstellt, dass zuerst die richtige Umgebung aktiviert wird.

#### **Teil 3: Nutzung & Funktionen**

**F: Wie benutze ich es, um zu diktieren?**
A: Zuerst starten Sie den "Diktier-Dienst" durch Ausführen des entsprechenden Skripts. Er läuft dann im Hintergrund. Danach verwenden Sie einen Auslöser (wie einen Hotkey oder ein spezielles Skript), um die Aufnahme zu starten und zu stoppen. Der erkannte Text wird dann automatisch in das gerade aktive Fenster geschrieben.

**F: Wie kann ich die Genauigkeit verbessern?**
A: 1. **Verwenden Sie ein gutes Mikrofon:** Ein Headset-Mikrofon ist weitaus besser als das eingebaute Mikrofon eines Laptops. 2. **Minimieren Sie Hintergrundgeräusche:** Eine ruhige Umgebung ist entscheidend. 3. **Sprechen Sie deutlich:** Sprechen Sie in einem gleichmäßigen Tempo und mit konstanter Lautstärke. Nuscheln oder Hetzen vermeiden.
Software-Anpassung (Die Stärke der Software): Für eine noch höhere Genauigkeit bietet SL5 Auro eine sehr mächtige Funktion: FuzzyMaps. Stellen Sie sich diese wie Ihr persönliches, intelligentes Wörterbuch vor. Sie können einfache Textdateien mit Regeln erstellen, um typische, wiederkehrende Erkennungsfehler zu beheben.

Beispiel: Wenn die Software hartnäckig "get hap" statt "GitHub" versteht, können Sie eine Regel in einer FuzzyMap anlegen, die das automatisch korrigiert.

Vorteil: Auf diese Weise können Sie der Software Ihren speziellen Fachjargon, Produktnamen, Abkürzungen oder sogar eigene "Sprachen" beibringen. Durch die Anpassung dieser Maps können Sie die Genauigkeit für Ihren persönlichen Anwendungsfall erheblich steigern.

**F: Kann ich die Sprache wechseln?**
A: Ja. Das System unterstützt das "Hot-Reloading" von Konfigurationsdateien im laufenden Betrieb. Sie können das Sprachmodell in der Konfiguration ändern, und der Dienst wechselt sofort und ohne Neustart zur neuen Sprache.

**F: Was ist "LanguageTool"?**
A: LanguageTool ist eine Open-Source-Prüfung für Grammatik und Stil, die wir integriert haben. Nachdem Ihre Sprache in Text umgewandelt wurde, korrigiert LanguageTool automatisch häufige Transkriptionsfehler (z. B. "seid" vs. "seit") und die Zeichensetzung, was die finale Ausgabe erheblich verbessert.

#### **Teil 4: Fehlerbehebung & Support**

**F: Ich habe den Dienst gestartet, aber nichts passiert, wenn ich diktieren will.**
A: Überprüfen Sie bitte Folgendes:
1. Läuft der Dienst noch in Ihrem Terminal/Ihrer Konsole? Suchen Sie nach Fehlermeldungen.
2. Ist Ihr Mikrofon korrekt als Standard-Eingabegerät in Ihrem Betriebssystem ausgewählt?
3. Ist das Mikrofon stummgeschaltet oder die Lautstärke zu niedrig eingestellt?

**F: Ich habe einen Fehler gefunden oder eine Idee für eine neue Funktion. Was soll ich tun?**
A: Das ist großartig! Der beste Ort, um Fehler zu melden oder Funktionen vorzuschlagen, ist das Erstellen eines "Issues" in unserem [GitHub Repository](https://github.com/sl5net/Vosk-System-Listener).





Absolut richtig, das ist ein entscheidender Punkt und eine unserer Stärken. Ich habe die Antwort überarbeitet, um die FuzzyMaps hervorzuheben.

***

### Überarbeitete FAQ-Antwort

#### **English:**

**5. F: Die Genauigkeit ist nicht perfekt. Wie kann ich sie verbessern?**
A: Die Genauigkeit hängt sowohl von Ihrer Ausrüstung als auch von der Software-Anpassung ab.

*   **Ihre Ausrüstung (Die Grundlagen):** Versuchen Sie, deutlich, in gleichmäßiger Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und die Verwendung eines guten Headset-Mikrofons anstelle des eingebauten Laptop-Mikrofons machen den größten Unterschied.

*   **Software-Anpassung (Die Stärke der Software):** Für eine noch höhere Genauigkeit bietet SL5 Auro eine sehr mächtige Funktion: **FuzzyMaps**. Stellen Sie sich diese wie Ihr persönliches, intelligentes Wörterbuch vor. Sie können einfache Textdateien mit Regeln erstellen, um typische, wiederkehrende Erkennungsfehler zu beheben.

    *   **Beispiel:** Wenn die Software hartnäckig "get hap" statt "GitHub" versteht, können Sie eine Regel in einer FuzzyMap anlegen, die das automatisch korrigiert.
    *   **Vorteil:** Auf diese Weise können Sie der Software Ihren speziellen Fachjargon, Produktnamen, Abkürzungen oder sogar eigene "Sprachen" beibringen. Durch die Anpassung dieser Maps können Sie die Genauigkeit für Ihren persönlichen Anwendungsfall erheblich steigern.

    
# Live Hot-Reload für Konfigurationen

SL5 Aura bietet eine leistungsstarke Live Hot-Reload-Funktion für Konfigurationsänderungen, wie z.B. die Aktivierung oder Deaktivierung von Git-Kommandos. Dies bedeutet, dass Sie Anpassungen vornehmen können, ohne den SL5 Aura-Service neu starten zu müssen – ein großer Vorteil für die Produktivität!

Wie es funktioniert:
Um eine optimale Performance zu gewährleisten, werden Konfigurationsänderungen erst beim Start eines neuen Verarbeitungsdurchlaufs überprüft und angewendet. Das bedeutet:

1 Änderung speichern: Sie ändern eine Einstellung (z.B. aktivieren Git-Kommandos).
2 Aktivierung: Die Änderung wird aktiv, sobald SL5 Aura das nächste Mal eine Aktion verarbeitet (z.B. Sie sprechen einen Befehl ein). Der Cache wird dann aktualisiert.

Wichtiger Hinweis: Ihre Änderungen sind sofort nach dem Speichern "vorgemerkt", werden aber erst mit der nächsten Interaktion aktiv. Es ist kein Neustart des Dienstes erforderlich.
