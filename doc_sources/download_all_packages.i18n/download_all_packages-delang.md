## Projektdienstprogramme: Dateisplitter und Downloader

Dieses Repository enthält zwei leistungsstarke Python-Skripte, die für die Verwaltung der Verteilung und des Downloads großer Dateien über GitHub-Releases entwickelt wurden.

1. **`split_and_hash.py`**: Ein Dienstprogramm für Repository-Besitzer, um große Dateien in kleinere Teile aufzuteilen und ein vollständiges und überprüfbares Prüfsummenmanifest zu generieren.
2. **`download_all_packages.py`**: Ein robustes Tool für Endbenutzer, um diese mehrteiligen Dateien automatisch herunterzuladen, zu überprüfen und wieder zusammenzusetzen und so die Datenintegrität von Anfang bis Ende sicherzustellen.

---

### 1. Skript zur Dateiaufteilung und Prüfsummengenerierung („split_and_hash.py“)

Dieses Skript ist für den **Repository-Betreuer** gedacht. Es bereitet große Dateien für die Verteilung auf Plattformen wie GitHub Releases vor, für die individuelle Dateigrößenbeschränkungen gelten.

#### Zweck

Das Hauptziel besteht darin, eine einzelne große Datei (z. B. „vosk-model-de-0.21.zip“) zu nehmen und zwei wichtige Aktionen auszuführen:
1. Teilen Sie die Datei in eine Reihe kleinerer, nummerierter Teile auf.
2. Generieren Sie eine einzelne, umfassende Manifestdatei („.sha256sums.txt“), die die Prüfsummen für **sowohl die ursprüngliche, vollständige Datei als auch jeden einzelnen Teil** enthält.

Dieses vollständige Manifest ist der Schlüssel zur Gewährleistung einer 100-prozentigen Datenintegrität für den Endbenutzer.

#### Hauptmerkmale

* **Standardisierte Aufteilung:** Teilt Dateien in 100-MB-Blöcke auf (im Skript konfigurierbar).
* **Konsistente Benennung:** Erstellt Teile mit einem „Z_“-Präfix (z. B. „Z_vosk-model-de-0.21.zip.part.aa“). Das Präfix „Z_“ gewährleistet die ordnungsgemäße Sortierung und Handhabung in verschiedenen Systemen.
* **Vollständiges Integritätsmanifest:** Die generierte Datei „.sha256sums.txt“ ist für maximale Zuverlässigkeit strukturiert. Es beinhaltet:
* Der SHA256-Hash der **originalen, vollständigen Datei**.
* Der SHA256-Hash von **jedem einzelnen Teil**, der erstellt wurde.

#### Verwendung für eine GitHub-Version

1. Platzieren Sie die große Datei (z. B. „vosk-model-de-0.21.zip“) in einem Verzeichnis mit dem Skript „split_and_hash.py“.
2. Führen Sie das Skript von Ihrem Terminal aus:
    ```bash
    python split_and_hash.py <your-large-file.zip>
    ```
3. Das Skript generiert alle „Z_...part.xx“-Dateien und die entsprechende „...sha256sums.txt“-Datei.
4. Wenn Sie eine neue GitHub-Version erstellen, laden Sie **alle** generierten Dateien hoch: die Teildateien und die einzelne Manifestdatei.
5. Wiederholen Sie diesen Vorgang für jede große Datei, die Sie verteilen möchten.

---

### 2. Automatisierter Paket-Downloader und Verifizierer („download_all_packages.py“)

Dieses Skript ist für den **Endbenutzer** gedacht. Es bietet eine einfache Ein-Befehl-Lösung zum zuverlässigen Herunterladen und erneuten Zusammenstellen aller im GitHub-Release angebotenen Pakete.

#### Zweck

Es automatisiert den ansonsten komplexen und fehleranfälligen Prozess des Herunterladens Dutzender Dateiteile, der Überprüfung jedes einzelnen und der korrekten Wiederzusammenstellung. Es verwendet die in der Version bereitgestellten Prüfsummenmanifeste, um sicherzustellen, dass die endgültige, zusammengestellte Datei eine perfekte, unbeschädigte Kopie des Originals ist.

#### Hauptmerkmale

* **Automatische Erkennung:** Das Skript stellt eine Verbindung zur GitHub-API her, um automatisch alle verfügbaren „Pakete“ in der Version zu finden, indem es nach „.sha256sums.txt“-Dateien sucht. Es ist keine manuelle Konfiguration der Dateinamen erforderlich.
* **Integrity-First-Prozess:** Für jedes Paket wird *zuerst* die Manifestdatei heruntergeladen, um die Liste der erforderlichen Teile und deren korrekte Prüfsummen zu erhalten.
* **Teilweise Überprüfung:** Es lädt jeweils einen Teil herunter und überprüft sofort seinen SHA256-Hash.
* **Automatischer Wiederholungsversuch bei Beschädigung:** Wenn ein heruntergeladener Teil beschädigt ist (der Hash stimmt nicht überein), löscht das Skript ihn automatisch und lädt ihn erneut herunter, um einen sauberen Download sicherzustellen.
* **Intelligente Neuzusammenstellung:** Sobald alle Teile eines Pakets heruntergeladen und überprüft wurden, werden sie in der richtigen alphabetischen Reihenfolge (`.aa`, `.ab`, `.ac`...) zusammengeführt, um die ursprüngliche große Datei wiederherzustellen.
* **Endgültige Überprüfung:** Nach der erneuten Zusammenstellung wird der SHA256-Hash der endgültigen, vollständigen Datei berechnet und mit dem im Manifest gefundenen Master-Hash verglichen. Dies stellt eine durchgängige Erfolgsbestätigung dar.
* **Belastbar und tolerant:** Das Skript ist robust gegenüber geringfügigen Namensinkonsistenzen wie „Z_“ vs. „z_“ und sorgt so für ein reibungsloses Benutzererlebnis.
* **Automatisierte Bereinigung:** Nachdem ein Paket erfolgreich erstellt und überprüft wurde, löscht das Skript die heruntergeladenen Teildateien, um Speicherplatz zu sparen.

#### Voraussetzungen

Der Benutzer muss Python und die Bibliotheken „requests“ und „tqdm“ installiert haben. Sie können mit pip installiert werden:
```bash
pip install requests tqdm
```

#### Verwendung

1. Laden Sie das Skript „download_all_packages.py“ herunter.
2. Führen Sie es vom Terminal aus ohne Argumente aus:
    ```bash
    python download_all_packages.py
    ```
3. Das Skript erledigt den Rest und zeigt Fortschrittsbalken und Statusmeldungen an. Nach Abschluss stehen dem Benutzer alle endgültigen, überprüften ZIP-Dateien im selben Verzeichnis zur Verwendung bereit.