### FAQ (Deutsch) 3.8.'2025 Niedz

**1. F: Czy to była aura SL5?**
O: Jest to systemweites Offline-Spracherkennungsprogramm. Sie können damit in jede beliebige Anwendung auf Ihrem Computer (Windows, macOS, Linux) diktieren, ohne eine Internetverbindung zu benötigen.

F: Czy Spracherkennung Alexa/Siri und konsorten jest offline?
O: Gute Frage. Nein, es ist das genaue Gegenteil. Alexa/Siri w chmurze. Die Sprachdaten werden zur Verarbeitung an deren Server gesendet. offline: alles passiert sicher auf dem Gerät des Nutzers. Das ist der entscheidende Vorteil für den Datenschutz.

**2. F: Warum sollte ich das nutzen? Czy to był das Besondere?**
A: **Datenschutz.** Ihre Sprachdaten werden zu 100% auf Ihrem lokalen Rechner verarbeitet und niemals in die Cloud gesendet. Das macht es absolut private und DSGVO-conform.

**3. F: Ist es kostenlos?**
Odp.: Ja, die Community Edition to vollständig kostenlos und Open-Source. Znajdź kod i instalator, który znajduje się na serwerze GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. F: Czy brauche ich, um es zu verwenden?**
Odp.: Jeden komputer i mikrofon. Für die beste Genauigkeit empfehlen wir dringend ein gutes Headset-Mikrofon anstelle des eingebauten Laptop-Mikrofons.

**5. F: Die Genauigkeit ist nicht perfekt. Czy możesz ich sie verbessern?**
A: Versuchen Sie, deutlich, in gleichmäßiger Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und ein besseres Mikrofon machen den größten Unterschied.

------------------------------------> Hier könnten wir erwähnen, dass wir verschiedene FuzzyMaps mit denen man die Genauigkeit erheblich verbessern kann orer sogar eigene Sprachen entwerfen kann






#### **Część 1: Allgemeine Fragen**

**F: Czy to był SL5 Auro?**
A: SL5 Auro ist ein systemweites Offline-Spracherkennungsprogramm. Es ermöglicht Ihnen, Text in jede beliebige Anwendung auf Ihrem Computer (z. B. E-Mail-Programm, Textverarbeitung, Code-Editor) zu diktieren, ohne eine Internetverbindung zu benötigen.

**F: Czy bedeutet był „offline” i był warum ist das wichtig?**
Odp.: „Offline” bedeutet, dass die gesamte Sprachverarbeitung direkt auf Ihrem Computer stattfindet. Ihre Sprachdaten werden **niemals** jest jednym z serwerów Cloud (np. Google, Amazon lub OpenAI). Dies bietet maximale Privatsphäre und Sicherheit, ideal für vertrauliche Informationen (z. B. für Anwälte, Ęrzte, Journalisten) und ist vollständig konform mit Datenschutzverordnungen wie der DSGVO.

**F: Ist es wirklich kostenlos? Wo ist der Haken?**
O: „Community Edition” jest w 100% kostenlosna i Open-Source. Es gibt keinen Haken. Wir glauben and die Stärke von Open-Source-Tools. Wenn Sie die Software nützlich finden und ihre Weiterentwicklung unterstützen möchten, können Sie dies über unsere [Ko-fi Seite](https://ko-fi.com/sl5) tun.

**F: Für wen ist diese Software gedacht?**
A: Für jeden, der viel schreibt und seine Effizienz steigern möchte: Autoren, Studenten, Programmierer, Juristen und Mediziner, Menschen mit körperlichen Einschränkungen oder jeder, der einfachlieber spricht als tippt.

#### **Część 2: Instalacja i konfiguracja**

**F: Welche Betriebssysteme werden unterstützt?**
Odp.: Oprogramowanie jest dostępne dla systemów Windows 11, Manjaro Linux, Ubuntu i macOS.

**F: Czy chcesz zainstalować system w systemie Windows?**
A: Wir bieten ein einfaches Ein-Klick-Installationsprogramm. Es ist ein Batch-Skript, das Administratorrechte benötigt, um die Umgebung einzurichten und die notwendigen Modelle herunterzuladen. Einmal ausgeführt, erledigt es alles für Sie.

**F: Der Download für die Modelle ist sehr groß. Waruma?**
A: Die Spracherkennungsmodelle ermöglichen es der Software, offline zu Arbeiten. Sie enthalten alle Daten, die die KI benötigt, um Ihre Sprache zu verstehen. Größere, präzisere Modelle können mehrere Gigabyte groß sein. Unser neuer Downloader teilt diese in kleinere, überprüfbare Teile auf, um einen zuverlässigen Download zu gewährleisten.

**F: Ich bin auf Linux. Wie gehe ich vor?**
Odp.: Linux klonen Sie typischerweise das Repository of GitHub i führen ein Setup-Skript wie aus. Dieses Skript jest pierwszą wersją Python-Umgebung, instalator Abhängigkeiten i startet den Diktier-Dienst.

**F: Wenn ich unter Windows auf eine `.py`-Datei doppelklicke, öffnet sie sich im Texteditor. Wie führe ich sie aus?**
Odp.: Das ist ein häufiges Windows-Problem, bei `.py`-Dateien nicht in Python-Interpreter zugeordnet sind. Sie sollten die einzelnen Python-Skripte nicht direkt ausführen. Verwenden Sie immer das bereitgestellte Haupt-Startskript (z.B. eine `.bat`-Datei), da dieses sicherstellt, dass zuerst die richtige Umgebung aktiviert wird.

#### **Część 3: Nutzung i funkcje**

**F: Wie benutze ich es, um zu diktieren?**
A: Zuerst starten Sie den "Diktier-Dienst" durch Ausführen des entsprechenden Skripts. Er läuft dann im Hintergrund. Danach verwenden Sie einen Auslöser (wie einen Hotkey lub ein spezielles Skript), um die Aufnahme zu starten i zu stoppen. Der erkannte Text wird dann automatisch in das gerade aktive Fenster geschrieben.

**F: Wie kann ich die Genauigkeit verbessern?**
A: 1. **Verwenden Sie ein gutes Mikrofon:** Ten zestaw słuchawkowy-Mikrofon jest lepszy niż eingebaute Mikrofon eines Laptops. 2. **Minimieren Sie Hintergrundgeräusche:** Eine ruhige Umgebung ist entscheidend. 3. **Sprechen Sie deutlich:** Sprechen Sie in einem gleichmäßigen Tempo und mit konstanter Lautstärke. Nuscheln oder Hetzen vermeiden.
Oprogramowanie-Anpassung (Die Stärke der Software): Für eine noch höhere Genauigkeit bietet SL5 Auro eine sehr mächtige Funkcja: FuzzyMaps. Stellen Sie sich diese wie Ihr persönliches, inteligentes Wörterbuch vor. Sie können einfache Textdateien mit Regeln erstellen, um typische, wiederkehrende Erkennungsfehler zu beheben.

Beispiel: Wenn die Software hartnäckig „get hap” statt „GitHub” versteht, można utworzyć regel w dowolnym FuzzyMap, automatycznie korygując.

Vorteil: Auf diese Weise können Sie der Software Ihren speziellen Fachjargon, Produktnamen, Abkürzungen oder sogar eigene "Sprachen" beibringen. Durch die Anpassung dieser Maps können Sie die Genauigkeit für Ihren persönlichen Anwendungsfall erheblich steigern.

**F: Kann ich die Sprache wechseln?**
O: Ja. Das System unterstützt das "Hot-Reloading" von Konfigurationsdateien im laufenden Betrieb. Sie können das Sprachmodell in der Konfiguration ändern, und der Dienst wechselt sofort und ohne Neustart zur neuen Sprache.

**F: Czy było to „LanguageTool”?**
A: LanguageTool jest narzędziem Open-Source-Prüfung für Grammatik und Stil, które jest zintegrowane z komputerem. Nachdem Ihre Sprache in Text umgewandelt wurde, korrigiert LanguageTool automatisch häufige Transkriptionsfehler (z. B. „seid” vs. „seit”) und die Zeichensetzung, był die finale Ausgabe erheblich verbessert.

#### **Część 4: Fehlerbehebung i wsparcie**

**F: Ich habe den Dienst gestartet, aber nichts passiert, wenn ich diktieren will.**
A: Überprüfen Sie bitte Folgendes:
1. Läuft der Dienst noch w Ihrem Terminal/Ihrer Konsole? Suchen Sie nach Fehlermeldungen.
2. Ihr Mikrofon korrekt als Standard-Eingabegerät in Ihrem Betriebssystem ausgewählt?
3. Ist das Mikrofon stummgeschaltet oder die Lautstärke zu niedrig eingestellt?

**F: Ich habe einen Fehler gefunden oder eine Idee für eine neue Funktion. Czy soll ich tun?**
O: Das ist großartig! Najlepszy Ort, um Fehler zu melden oder Funktionen vorzuschlagen, ist das Erstellen eines "Problemy" w unserem [GitHub Repository](https://github.com/sl5net/Vosk-System-Listener).





Absolut richtig, das ist ein entscheidender Punkt und eine unserer Stärken. Ich habe die Antwort überarbeitet, um die FuzzyMaps hervorzuheben.

***

### Odpowiedź na często zadawane pytania (Überarbeitete).

#### **Angielski:**

**5. F: Die Genauigkeit ist nicht perfekt. Czy możesz ich sie verbessern?**
A: Die Genauigkeit hängt sowohl von Ihrer Ausrüstung als auch von der Software-Anpassung ab.

* **Ihre Ausrüstung (Die Grundlagen):** Versuchen Sie, deutlich, in gleichmäßiger Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und die Verwendung eines guten Zestaw słuchawkowy-Mikrofons anstelle des eingebauten Laptop-Mikrofons machen den größten Unterschied.

* **Dodatkowe oprogramowanie (Die Stärke der Software):** Für eine noch höhere Genauigkeit bietet SL5 Auro eine sehr mächtige Funktion: **FuzzyMaps**. Stellen Sie sich diese wie Ihr persönliches, inteligentes Wörterbuch vor. Sie können einfache Textdateien mit Regeln erstellen, um typische, wiederkehrende Erkennungsfehler zu beheben.

* **Obejrzyj:** Wenn die Software hartnäckig „get hap” statt „GitHub” versteht, können Sie eine Regel in anlegen FuzzyMap, das das automatyczne korygowanie.
* **Vorteil:** Auf diese Weise können Sie der Software Ihren speziellen Fachjargon, Produktnamen, Abkürzungen oder sogar eigene „Sprachen” beibringen. Durch die Anpassung dieser Maps können Sie die Genauigkeit für Ihren persönlichen Anwendungsfall erheblich steigern.

XSPACEbreakX
# Live Hot-Reload dla konfiguracji

SL5 Aura bietet eine leistungsstarke Live Hot-Reload-Funktion für Konfigurationsänderungen, wie z.B. die Aktivierung oder Deaktivierung von Git-Kommandos. Dies bedeutet, dass Sie Anpassungen vornehmen können, ohne den SL5 Aura-Service neu starten zu müssen – ein großer Vorteil für die Produktivität!

Oto funkcje:
Um eine optymale Performance zu gewährleisten, werden Konfigurationsänderungen erst beim Start eines neuen Verarbeitungsdurchlaufs überprüft und angewendet. Ten beutet:

1 Ęnderung speichern: Sie ändern eine Einstellung (z.B. aktivieren Git-Kommandos).
2 Aktivierung: Die Ęnderung wird aktiv, sobald SL5 Aura das nächste Mal eine Aktion verarbeitet (z.B. Sie sprechen einen Befehl ein). Der Cache wird dann aktualisiert.

Wichtiger Hinweis: Ihre Ęnderungen sind sofort nach dem Speichern "vorgemerkt", werden aber erst mit der nächsten Interaktion aktiv. Es ist kein Neustart des Dienstes erforderlich.