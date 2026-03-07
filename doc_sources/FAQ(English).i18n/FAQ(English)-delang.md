### FAQ (Englisch) 3.8.2025 So

**1. F: Was ist SL5 Aura?**
A: Es handelt sich um ein systemweites Offline-Sprach-zu-Text-Programm. Damit können Sie in jede Anwendung auf Ihrem Computer (Windows, macOS, Linux) diktieren, ohne dass eine Internetverbindung erforderlich ist.

**2. F: Warum sollte ich das verwenden? Was macht es besonders?**
A: **Datenschutz.** Ihre Sprachdaten werden zu 100 % auf Ihrem lokalen Computer verarbeitet und niemals an die Cloud gesendet. Dies macht es vollständig privat und DSGVO-konform.

**3. F: Ist es kostenlos?**
A: Ja, die Community Edition ist völlig kostenlos und Open Source. Den Code und das Installationsprogramm finden Sie auf unserem GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. F: Was brauche ich, um es zu verwenden?**
A: Ein Computer und ein Mikrofon. Für optimale Genauigkeit empfehlen wir dringend ein spezielles Headset-Mikrofon anstelle eines eingebauten Laptop-Mikrofons.

**5. F: Die Genauigkeit ist nicht perfekt. Wie kann ich es verbessern?**
A: Versuchen Sie, deutlich und in gleichbleibender Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und die Verwendung eines besseren Mikrofons machen den größten Unterschied.
Software-Anpassung (Advanced Power): Für ein Höchstmaß an Genauigkeit nutzt SL5 Aura eine leistungsstarke Funktion namens FuzzyMaps. Betrachten Sie diese als Ihr persönliches, intelligentes Wörterbuch. Sie können einfache Textdateien mit Regeln erstellen, um häufige, wiederkehrende Erkennungsfehler zu beheben.

Beispiel: Wenn die Software oft „get hap“ anstelle von „GitHub“ hört, können Sie eine Regel hinzufügen, die dies jedes Mal automatisch korrigiert.

Vorteil: Dadurch können Sie der Software Ihren spezifischen Fachjargon, Produktnamen und Abkürzungen „beibringen“ oder sogar Regelsätze für einzigartige Vokabulare erstellen. Durch die Anpassung dieser Karten können Sie die Genauigkeit für Ihren spezifischen Anwendungsfall erheblich verbessern.

***

#### **Teil 1: Allgemeine Fragen**

**F: Was ist SL5 Auro?**
A: SL5 Auro ist ein systemweites Offline-Sprach-zu-Text-Programm. Damit können Sie Text in jede Anwendung auf Ihrem Computer diktieren (z. B. Ihren E-Mail-Client, ein Textverarbeitungsprogramm, einen Code-Editor), ohne dass eine Internetverbindung erforderlich ist.

**F: Was bedeutet „offline“ und warum ist es wichtig?**
A: „Offline“ bedeutet, dass die gesamte Sprachverarbeitung direkt auf Ihrem Computer erfolgt. Ihre Sprachdaten werden **niemals** an einen Cloud-Server (wie Google, Amazon oder OpenAI) gesendet. Dies bietet maximale Privatsphäre und Sicherheit und ist daher ideal für vertrauliche Informationen (z. B. für Anwälte, Ärzte, Journalisten) und vollständig konform mit Datenschutzbestimmungen wie der DSGVO.

**F: Ist es wirklich kostenlos? Was ist der Haken?**
A: Die „Community Edition“ ist 100 % kostenlos und Open Source. Es gibt keinen Haken. Wir glauben an die Leistungsfähigkeit von Open-Source-Tools. Wenn Sie die Software wertvoll finden und ihre Weiterentwicklung unterstützen möchten, können Sie dies über unseren [Ko-fi page](https://ko-fi.com/sl5) tun.

**F: Für wen ist diese Software gedacht?**
A: Es ist für alle gedacht, die viel schreiben und ihre Effizienz steigern möchten: Schriftsteller, Studenten, Programmierer, Juristen und Mediziner, Menschen mit körperlichen Einschränkungen oder alle, die einfach lieber sprechen als tippen.

#### **Teil 2: Installation und Einrichtung**

**F: Welche Betriebssysteme werden unterstützt?**
A: Die Software wurde getestet und bestätigt, dass sie unter Windows 11, Manjaro Linux sowie Ubuntu und macOS funktioniert.

**F: Wie installiere ich es unter Windows?**
A: Wir bieten ein einfaches Ein-Klick-Installationsprogramm. Es handelt sich um ein .Bat-Skript, das Administratorrechte erfordert, um die Umgebung einzurichten und die erforderlichen Modelle herunterzuladen. Sobald es ausgeführt wird, erledigt es alles für Sie.

**F: Der Download für die Modelle ist sehr groß. Warum?**
A: Die Spracherkennungsmodelle ermöglichen es der Software, offline zu arbeiten. Sie enthalten alle notwendigen Daten, damit die KI Ihre Sprache versteht. Größere, präzisere Modelle können mehrere Gigabyte groß sein. Unser neuer Downloader teilt diese in kleinere, überprüfbare Teile auf, um einen zuverlässigen Download zu gewährleisten.

**F: Ich verwende Linux. Wie ist der Prozess?**
A: Unter Linux klonen Sie normalerweise das Repository von GitHub und führen ein Setup-Skript aus. Dieses Skript erstellt eine virtuelle Python-Umgebung, installiert Abhängigkeiten und startet den Diktierdienst.

**F: Wenn ich unter Windows auf eine „.py“-Datei doppelklicke, wird sie in einem Texteditor geöffnet. Wie führe ich es aus?**
A: Dies ist ein häufiges Windows-Problem, bei dem „.py“-Dateien nicht mit dem Python-Interpreter verknüpft sind. Sie sollten die einzelnen Python-Skripte nicht direkt ausführen. Verwenden Sie immer das bereitgestellte Hauptstartskript (z. B. eine „.bat“-Datei), da so sichergestellt wird, dass zuerst die richtige Umgebung aktiviert wird.

#### **Teil 3: Verwendung und Funktionen**

**F: Wie verwende ich es eigentlich zum Diktieren?**
A: Zuerst starten Sie den „Diktierdienst“, indem Sie das entsprechende Skript ausführen. Es wird im Hintergrund ausgeführt. Anschließend verwenden Sie einen Auslöser (z. B. einen Hotkey oder ein spezielles Skript), um die Aufzeichnung zu starten und zu stoppen. Der erkannte Text wird dann automatisch in das gerade aktive Fenster eingegeben.

**F: Wie kann ich die Genauigkeit verbessern?**
A: 1. **Verwenden Sie ein gutes Mikrofon:** Ein Headset-Mikrofon ist weitaus besser als das eingebaute Mikrofon eines Laptops. 2. **Hintergrundgeräusche minimieren:** Eine ruhige Umgebung ist der Schlüssel. 3. **Sprechen Sie deutlich:** Sprechen Sie in gleichmäßigem Tempo und gleichbleibender Lautstärke. Murmeln Sie nicht und beeilen Sie sich nicht.
Software-Anpassung (Advanced Power): Für ein Höchstmaß an Genauigkeit nutzt SL5 Auro eine leistungsstarke Funktion namens FuzzyMaps. Betrachten Sie diese als Ihr persönliches, intelligentes Wörterbuch. Sie können einfache Textdateien mit Regeln erstellen, um häufige, wiederkehrende Erkennungsfehler zu beheben.

Beispiel: Wenn die Software oft „get hap“ anstelle von „GitHub“ hört, können Sie eine Regel hinzufügen, die dies jedes Mal automatisch korrigiert.

Vorteil: Dadurch können Sie der Software Ihren spezifischen Fachjargon, Produktnamen und Abkürzungen „beibringen“ oder sogar Regelsätze für einzigartige Vokabulare erstellen. Durch die Anpassung dieser Karten können Sie die Genauigkeit für Ihren spezifischen Anwendungsfall erheblich verbessern.

**F: Kann ich die Sprache wechseln?**
A: Ja. Das System unterstützt das Live-„Hot-Reloading“ von Konfigurationsdateien. Sie können das Sprachmodell in der Konfiguration ändern und der Dienst wechselt sofort zu diesem Modell, ohne dass ein Neustart erforderlich ist.

**F: Was ist „LanguageTool“?**
A: LanguageTool ist ein von uns integrierter Open-Source-Grammatik- und Stilprüfer. Nachdem Ihre Rede in Text umgewandelt wurde, korrigiert LanguageTool automatisch häufige Transkriptionsfehler (z. B. „richtig“ vs. „schreiben“) und korrigiert die Zeichensetzung, wodurch die Endausgabe erheblich verbessert wird.

#### **Teil 4: Fehlerbehebung und Support**

**F: Ich habe den Dienst gestartet, aber beim Diktieren passiert nichts.**
A: Überprüfen Sie Folgendes:
1. Läuft der Dienst noch auf Ihrem Terminal/Ihrer Konsole? Suchen Sie nach Fehlermeldungen.
2. Ist Ihr Mikrofon in Ihrem Betriebssystem korrekt als Standardeingabegerät ausgewählt?
3. Ist das Mikrofon stummgeschaltet oder die Lautstärke zu niedrig eingestellt?

**F: Ich habe einen Fehler gefunden oder habe eine Idee für eine neue Funktion. Was soll ich tun?**
A: Das ist großartig! Der beste Ort, um Fehler zu melden oder Funktionen vorzuschlagen, ist das Öffnen eines „Problems“ auf unserem [GitHub repository](https://github.com/sl5net/Vosk-System-Listener).



**5. F: Die Genauigkeit ist nicht perfekt. Wie kann ich es verbessern?**
A: Die Genauigkeit hängt sowohl von Ihrem Setup als auch von der Softwareanpassung ab.

* **Ihr Setup (die Grundlagen):** Versuchen Sie, klar und deutlich in gleichbleibender Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und die Verwendung eines guten Headset-Mikrofons anstelle des eingebauten Mikrofons eines Laptops machen einen großen Unterschied.

* **Software-Anpassung (Advanced Power):** Für höchste Genauigkeit nutzt SL5 Auro eine leistungsstarke Funktion namens **FuzzyMaps**. Betrachten Sie diese als Ihr persönliches, intelligentes Wörterbuch. Sie können einfache Textdateien mit Regeln erstellen, um häufige, wiederkehrende Erkennungsfehler zu beheben.

* **Beispiel:** Wenn die Software oft „get hap“ anstelle von „GitHub“ hört, können Sie eine Regel hinzufügen, die dies jedes Mal automatisch korrigiert.
* **Vorteil:** Dadurch können Sie der Software Ihren spezifischen Fachjargon, Produktnamen und Abkürzungen „beibringen“ oder sogar Regelsätze für einzigartige Vokabulare erstellen. Durch die Anpassung dieser Karten können Sie die Genauigkeit für Ihren spezifischen Anwendungsfall erheblich verbessern.




### Architectural Deep Dive: Kontinuierliche Aufnahme im „Walkie-Talkie“-Stil

Unser Diktierdienst implementiert eine robuste, zustandsgesteuerte Architektur, um ein nahtloses, kontinuierliches Aufnahmeerlebnis zu ermöglichen, ähnlich der Verwendung eines Walkie-Talkies. Das System ist immer bereit, Audio aufzunehmen, verarbeitet es jedoch nur, wenn es explizit ausgelöst wird, was eine hohe Reaktionsfähigkeit und einen geringen Ressourcenverbrauch gewährleistet.

Dies wird erreicht, indem die Audio-Hörschleife vom Verarbeitungsthread entkoppelt und der Systemstatus mit zwei Schlüsselkomponenten verwaltet wird: einem „active_session“-Ereignisflag und unserem „audio_manager“ für die Mikrofonsteuerung auf Betriebssystemebene.

**Die Logik der Zustandsmaschine:**

Das System arbeitet in einer Dauerschleife und wird von einem einzigen Hotkey verwaltet, der zwischen zwei Primärzuständen umschaltet:

1. **LISTENING-Status (Standard/Bereit):**
* **Bedingung:** Das Flag „active_session“ ist „False“.
* **Mikrofonstatus:** Das Mikrofon ist **stummgeschaltet** auf „Stummschaltung des Mikrofons aufheben()“. Der Vosk-Listener ist aktiv und wartet auf Audioeingabe.
* **Aktion:** Wenn der Benutzer den Hotkey drückt, wechselt der Status. Das Flag „active_session“ ist auf „True“ gesetzt und signalisiert den Beginn eines „echten“ Diktats.

2. **VERARBEITUNGSstatus (Benutzer hat mit dem Sprechen fertig):**
* **Bedingung:** Der Benutzer drückt den Hotkey, während das Flag „active_session“ „True“ ist.
* **Mikrofonstatus:** Die **erste Aktion** besteht darin, das Mikrofon über „mute_microphone()“ sofort **stummzuschalten**. Dadurch wird der Audiostream zur Vosk-Engine sofort gestoppt.
*   **Aktion:**
* Das Flag „active_session“ ist auf „False“ gesetzt.
* Der letzte erkannte Audioblock wird von Vosk abgerufen.
* Der Verarbeitungsthread wird mit diesem endgültigen Text gestartet.
* Entscheidend ist, dass der Verarbeitungsthread innerhalb eines „finally“-Blocks nach Abschluss „unmute_microphone()“ ausführt.

**Die „Magie“ des Aufhebungssignals:**

Der Schlüssel zur Endlosschleife ist der letzte Aufruf von „unmute_microphone()“. Sobald die Verarbeitung des Diktats „A“ abgeschlossen ist und die Stummschaltung des Mikrofons aufgehoben ist, kehrt das System automatisch und sofort in den Zustand **HÖREN** zurück. Der Vosk-Zuhörer, der geduldig wartete, beginnt sofort wieder mit dem Audioempfang und ist bereit, das Diktat „B“ aufzunehmen.

Dadurch entsteht ein äußerst reaktionsfähiger Zyklus:
„Drücken Sie -> Sprechen -> Drücken Sie -> (Stummschalten und verarbeiten) -> (Stummschaltung aufheben und zuhören)“.

Diese Architektur stellt sicher, dass das Mikrofon immer nur für die kurze Dauer der Textverarbeitung stummgeschaltet wird, sodass sich das System für den Benutzer augenblicklich anfühlt, während gleichzeitig eine robuste Kontrolle gewährleistet ist und außer Kontrolle geratene Aufnahmen verhindert werden.