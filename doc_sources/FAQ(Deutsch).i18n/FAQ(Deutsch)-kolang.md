### FAQ(독일어) 3.8.'2025 Sun

**1. F: SL5 Aura가 아니었나요?**
A: 시스템은 오프라인-Spracherkennungs 프로그램과 동일합니다. Ihrem Computer(Windows, macOS, Linux)에 대한 믿음이 있는 경우에는 Internetverbindung zu benötigen에서 확인하세요.

F: 오프라인 Spracherkennung Alexa/Siri 및 Konsorten이 있습니까?
답: 구테 프라지. Nein, es ist das genaue Gegenteil. Alexa/Siri는 cloudbasiert를 사용합니다. Die Sprachdaten werden zur Verarbeitung an deren Server gesendet. 오프라인: alles passiert sicher auf dem Gerät des Nutzers. Das ist der entscheidende Vorteil für den Datenschutz.

**2. F: Warum sollte ich das nutzen? 그게 Besondere였나요?**
A: **Datenschutz.** Ihre Sprachdaten werden zu 100% auf Ihrem lokalen Rechner verarbeitet und niemals in die Cloud gesendet. Das macht esabsolut privat und DSGVO-konform.

**3. F: es kostenlos인가요?**
A: 예, Community Edition은 vollständig kostenlos 및 Open-Source입니다. Den Code 및 den Installer finden Sie auf unserem GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. F: brauche ich, um es zu verwenden이었나?**
A: Einen Computer와 ein Mikrofon입니다. 최고의 Genauigkeit empfehlen wir dringend ein Gutes 헤드셋 마이크와 노트북 마이크를 사용하세요.

**5. F: Die Genauigkeit은 완벽하지 않습니다. Wie kann ich sie verbessern?**
A: Versuchen Sie, deutlich, in gleichmäßiger Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und ein besseres Mikrofon machen den größten Unterschied.

--------------------------> Hier könnten wir erwähnen, dass wir verschiedene FuzzyMaps mit denen man die Genauigkeit erheblich verbessern kann oder sogar eigene Sprachen entwerfen kann






#### **부분 1: Allgemeine Fragen**

**F: SL5 Auro가 아니었나요?**
A: SL5 Auro는 오프라인 시스템 프로그램입니다. Es ermöglicht Ihnen, Text in jede beliebige Anwendung auf Ihrem Computer (z. B. E-Mail-Programm, Textverarbeitung, Code-Editor) zu diktieren, ohne eine Internetverbindung zu benötigen.

**F: bedeutet은 "오프라인"이었고 warum은 어디에 있었나요?**
A: "오프라인" bedeutet, dass die gesamte Sprachverarbeitung direkt auf Ihrem Computer stattfindet. Sprachdaten은 **niemals** 및 einen Cloud-Server(Google, Amazon 또는 OpenAI) 서비스를 제공합니다. Dies bietet maximale Privatsphäre und Sicherheit, Ideal für vertrauliche Informationen(z. B. für Anwälte, ärzte, Journalisten) 및 ist vollständig konform mit Datenschutzverordnungen wie der DSGVO.

**F: Wirklich kostenlos인가요? Wo ist der Haken?**
A: "Community Edition"은 100% 기술 및 오픈 소스입니다. Es gibt keinen Haken. Wir glauben an die Stärke von 오픈 소스 도구. Wenn Sie die Software nützlich finden und ihre Weiterentwicklung unterstützen möchten, können Sie dies über unsere [Ko-fi Seite](https://ko-fi.com/sl5) tun.

**F: Für wen ist diese Software gedacht?**
A: Für jeden, der viel schreibt und seine Effizienz steigern möchte: Autoren, Studenten, Programmierer, Juristen und Mediziner, Menschen mit körperlichen Einschränkungen oder jeder, der einfach lieber spricht alstippt.

#### **부분 2: 설치 및 Einrichtung**

**F: Welche Betriebssysteme werden unterstützt?**
A: Windows 11, Manjaro Linux, Ubuntu 및 macOS getestet에서 소프트웨어를 사용할 수 있습니다.

**F: Windows에 설치하는 방법은 무엇입니까?**
A: Wir bieten ein einfaches Ein-Klick-Installationsprogramm. Es ist ein Batch-Skript, das Administratorrechte benötigt, um die Umgebung einzurichten und die notwendigen Modelle herunterzuladen. Einmal ausgeführt, erledigt es alles für Sie.

**F: Der Download für die Modelle ist sehr groß. 워럼?**
A: Die Spracherkennungsmodelle ermöglichen es der Software, 오프라인 zu arbeiten. Sie enthalten alle Daten, die die KI benötigt, um Ihre Sprache zu verstehen. Größere, präzisere Modelle können mehrere Gigabyte groß sein. Unser neuer Downloader teilt diese in kleinere, überprüfbare Teile auf, um einen zuverlässigen Download zu gewährleisten.

**F: Linux에 대한 내용입니다. 그게 뭐야?**
A: GitHub의 Linux 복제 유형 저장소와 aus의 설정 스크립트를 확인하세요. Dises Skript는 Python-Umgebung의 장점을 설명하고 Abhängigkeiten을 설치하고 Diktier-Dienst를 시작합니다.

**F: Windows에서 `.py`를 사용하는 경우 -Datei doppelklicke, öffnet sie sich im Texteditor. Wie führe ich sie aus?**
A: Das ist ein häufiges Windows-Problem, bei dem `.py`-Dateien nicht dem Python-Interpreter zugeordnet sind. Sie sollten die einzelnen Python-Skripte nicht direkt ausführen. Verwenden Sie immer das bereitgestellte Haupt-Startskript (z.B. eine `.bat`-Datei), da dieses sicherstellt, dass zuerst die richtige Umgebung aktiviert wird.

#### **3부: Nutzung & Funktionen**

**F: Wie benutze ich es, um zu diktieren?**
A: Zuerst는 Ausführen des entsprechenden Skripts를 통해 Sie den "Diktier-Dienst"를 시작했습니다. Er lauft dann im Hintergrund. Danach verwenden Sie einen Auslöser(wie einen Hotkey oder ein spezielles Skript), um die Aufnahme zu starten und zu stoppen. Der erkannte 텍스트는 das gerade 활성 Fenster geschrieben에서 자동으로 작성됩니다.

**F: Wie kann ich die Genauigkeit verbessern?**
A: 1. **Verwenden Sie ein Gutes Mikrofon:** Ein 헤드셋-Mikrofon ist weitaus besser als das eingebaute Mikrofon eines Laptops. 2. **Minimieren Sie Hintergrundgeräusche:** Eine ruhige Umgebung ist entscheidend. 3. **Sprechen Sie deutlich:** Sprechen Sie in einem gleichmäßigen Tempo und mit konstanter Lautstärke. Nuscheln oder Hetzen vermeiden.
Software-Anpassung(Die Stärke der Software): Für eine noch höhere Genauigkeit bietet SL5 Auro eine sehr mächtige Funktion: FuzzyMaps. Stellen Sie sich diese wie Ihr persönliches, Intelligencetes Wörterbuch vor. Sie können einfache Textdateien mit Regeln erstellen, um typische, wiederkehrende Erkennungsfehler zu beheben.

Beispiel: Wenn die Software hartnäckig "get hap" statt "GitHub" versteht, Kunnen Sie eine Regel in einer FuzzyMap anlegen, die das automatisch korrigiert.

Vorteil: Auf diese Weise können Sie der Software Ihren speziellen Fachjargon, Produktnamen, Abkürzungen oder sogar eigene "Sprachen" beibringen. Durch die Anpassung dieser 지도 können Sie die Genauigkeit für Ihren persönlichen Anwendungsfall erheblich steigern.

**F: Kann ich die Sprache wechseln?**
답: 자. Das System unterstützt das "Hot-Reloading" von Konfigurationsdateien im laufenden Betrieb. Sie können das Sprachmodell in der Konfiguration ändern, und der Dienst wechselt sofort und ohne Neustart zur neuen Sprache.

**F: "LanguageTool"이 아니었나요?**
A: LanguageTool은 Grammatik und Stil을 위한 Open-Source-Prüfung이며, 통합 기능을 제공합니다. Nachdem Ihre Sprache in Text umgewandelt wurde, korrigiert LanguageTool automatisch häufige Transkriptionsfehler (z. B. "seid" vs. "seit") und die Zeichensetzung, was die finale Ausgabe erheblich verbessert.

#### **4부: Fehlerbehebung 및 지원**

**F: Ich habe den Dienst gestartet, aber nichts passiert, wenn ich diktieren will.**
A: Überprüfen Sie bitte Folgendes:
1. Ihrem Terminal/Ihrer Konsole의 Läuft der Dienst noch? Suchen Sie nach Fehlermeldungen.
2. Ihr Mikrofon korrekt는 Ihrem Betriebssystem ausgewählt의 Standard-Eingabegerät입니까?
3. Ist das Mikrofon stummgeschaltet oder die Lautstärke zu niedrig eingestellt?

**F: Ich habe einen Fehler gefunden oder eine Idee für eine neue Funktion. 정말 그랬나요?**
A: 너무 심하지 않아요! Der beste Ort, um Fehler zu melden oder Funktionen vorzuschlagen, ist das Erstellen eines "Issues" in unserem [GitHub Repository](https://github.com/sl5net/Vosk-System-Listener).





Absolut richtig, das ist ein entscheidender Punkt und eine unserer Stärken. 나는 Antwort überarbeitet에 대해 알고 있고, um die FuzzyMaps hervorzuheben.

***

### Überarbeitete FAQ-Antwort

#### **영어:**

**5. F: Die Genauigkeit은 완벽하지 않습니다. Wie kann ich sie verbessern?**
A: Die Genauigkeit hängt sowohl von Ihrer Ausrüstung als auch von der Software-Anpassung ab.

* **Ihre Ausrüstung(Die Grundlagen):** Versuchen Sie, deutlich, in gleichmäßiger Lautstärke und Geschwindigkeit zu sprechen. Die Reduzierung von Hintergrundgeräuschen und die Verwendung eines Guten 헤드셋-Mikrofons anstelle des eingebauten 노트북-Mikrofons machen den größten Unterschied.

* **Software-Anpassung(Die Stärke der Software):** Für eine noch höhere Genauigkeit bietet SL5 Auro eine sehr mächtige Funktion: **FuzzyMaps**. Stellen Sie sich diese wie Ihr persönliches, Intelligencetes Wörterbuch vor. Sie können einfache Textdateien mit Regeln erstellen, um typische, wiederkehrende Erkennungsfehler zu beheben.

* **Beispiel:** Wenn die Software hartnäckig "get hap" statt "GitHub" versteht, können Sie eine Regel in einer FuzzyMap anlegen, die das automatisch korrigiert.
* **Vorteil:** Auf diese Weise können Sie der Software Ihren speziellen Fachjargon, Produktnamen, Abkürzungen oder sogar eigene "Sprachen" beibringen. Durch die Anpassung dieser 지도 können Sie die Genauigkeit für Ihren persönlichen Anwendungsfall erheblich steigern.

XSPACEbreakX
# 구성을 위한 실시간 핫 리로드

SL5 Aura bietet eine leistungsstarke Live Hot-Reload-Funktion für Konfigurationsänderungen, wie z.B. Die Aktivierung oder Deaktivierung von Git-Kommandos. Dies bedeutet, dass Sie Anpassungen vornehmen können, ohne den SL5 Aura-Service neu starten zu müssen – ein großer Vorteil für die Produktivität!

기능적으로는 다음과 같습니다.
Um eine Optimale Performance zu gewährleisten, werden Konfigurationsänderungen erst beim Start eines neuen Verarbeitungsdurchlaufs überprüft und angewendet. 다스 베들텟:

1 änderung speichern: Sie ändern eine Einstellung (z.B. aktivieren Git-Kommandos).
2 활동: Die änderung wird aktiv, sobald SL5 Aura das nächste Mal eine Aktion verarbeitet (z.B. Sie sprechen einen Befehl ein). Der Cache는 실제로 작동할 수 있습니다.

Wichtiger Hinweis: Ihre änderungen sind sofort nach dem Speichern "vorgemerkt", werden aber erst mit der nächsten Interaktion aktiv. 이것은 Neustart des Dienstes erforderlich의 핵심입니다.