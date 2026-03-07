# VirtualBox-Setup-Anleitung für STT-Projekttests

Dieses Handbuch enthält die empfohlenen Schritte zum Einrichten einer stabilen und leistungsstarken virtuellen Ubuntu 24.04-Maschine in VirtualBox. Wenn Sie diese Anweisungen befolgen, wird eine konsistente Umgebung zum Testen der STT-Anwendung erstellt und häufige Probleme wie langsame Installation, Systemabstürze und fehlende Funktionalität der Zwischenablage vermieden.

## Voraussetzungen

- VirtualBox auf dem Host-Computer installiert.
- Eine Ubuntu 24.04 Desktop ISO-Datei heruntergeladen.

## Referenz-Host-Hardware

Diese Konfiguration wurde auf dem folgenden Hostsystem getestet und validiert. Die Leistung kann auf anderer Hardware variieren, die Stabilitätseinstellungen sollten jedoch allgemein gelten.

- **Betriebssystem:** Manjaro Linux
- **Kernel:** 6.6.94
- **Prozessor:** 16 × AMD Ryzen 7 3700X
- **Speicher:** 31,3 GiB RAM
- **Grafikprozessor:** NVIDIA GeForce GTX 1050 Ti

---

## Teil 1: VM-Erstellung und -Konfiguration

Diese Einstellungen sind entscheidend für Leistung und Stabilität.

### Schritt 1.1: Erstellen Sie die neue virtuelle Maschine

1. Klicken Sie in VirtualBox auf **Neu**.
2. **Name:** „Ubuntu STT Tester“ (oder ähnlich).
3. **ISO-Image:** Lassen Sie dieses Feld leer.
4. Aktivieren Sie das Kontrollkästchen: **„Unbeaufsichtigte Installation überspringen“**.
5. Klicken Sie auf **Weiter**.
6. **Hardware:**
- **Basisspeicher:** „4096 MB“ oder mehr.
- **Prozessoren:** „4“ oder mehr.
7. Klicken Sie auf **Weiter**.

### Schritt 1.2: Erstellen Sie die virtuelle Festplatte (KRITISCH)

Dies ist der wichtigste Schritt für eine schnelle Installation und Leistung.

1. Wählen Sie **„Jetzt eine virtuelle Festplatte erstellen“**.
2. Stellen Sie die Festplattengröße auf **40 GB** oder mehr ein.
3. Ändern Sie im nächsten Bildschirm den Speichertyp in „Feste Größe“**.
> **Warum?** Eine Festplatte mit fester Größe wird vorab zugewiesen und verhindert den massiven E/A-Engpass, der auftritt, wenn die Größe einer „dynamisch zugewiesenen“ Festplatte während der Installation ständig geändert wird.
4. Klicken Sie auf **Erstellen** und warten Sie, bis der Vorgang abgeschlossen ist.

### Schritt 1.3: Endgültige VM-Einstellungen

Wählen Sie die neu erstellte VM aus und klicken Sie auf **Einstellungen**. Konfigurieren Sie Folgendes:

- **System -> Motherboard:**
- **Chipsatz:** `ICH9`
- Aktivieren Sie **„EFI aktivieren (nur spezielle Betriebssysteme)“**.

- **Anzeige -> Bildschirm:**
- **Grafikcontroller:** `VMSVGA`
- **Deaktivieren Sie „3D-Beschleunigung aktivieren“**.
> **Warum?** 3D-Beschleunigung ist eine häufige Ursache für Systemabstürze und -einfrierungen bei Linux-Gästen. Durch die Deaktivierung wird die Stabilität erheblich verbessert.

-   **Lagerung:**
- Wählen Sie den **SATA-Controller**. Aktivieren Sie das Kontrollkästchen **"Host-E/A-Cache verwenden"**.
- Wählen Sie die virtuelle Festplattendatei („.vdi“) aus. Aktivieren Sie das Kontrollkästchen **„Solid-State-Laufwerk“**.
- Wählen Sie das optische Laufwerk **Leer**. Klicken Sie rechts auf das CD-Symbol und **"Wählen Sie eine Datenträgerdatei..."**, um Ihr Ubuntu 24.04 ISO anzuhängen.

Klicken Sie auf **OK**, um alle Einstellungen zu speichern.

---

## Teil 2: Installation des Ubuntu-Betriebssystems

1. Starten Sie die VM.
2. Fahren Sie mit der Sprach- und Tastatureinrichtung fort.
3. Wenn Sie „Updates und andere Software“ erreichen, wählen Sie:
- **Minimale Installation**.
- **Deaktivieren** Sie „Updates während der Installation von Ubuntu herunterladen“.
4. Fahren Sie mit der Installation fort, bis sie abgeschlossen ist.
5. Wenn Sie fertig sind, starten Sie die VM neu. Entfernen Sie an der Eingabeaufforderung das Installationsmedium (drücken Sie die Eingabetaste).

---

## Teil 3: Nach der Installation (Gastbeiträge)

Dieser Schritt ermöglicht die gemeinsame Nutzung der Zwischenablage, Drag-and-Drop und die automatische Größenänderung des Bildschirms.

### Schritt 3.1: Guest Additions ISO auf dem Host installieren (falls erforderlich)

Stellen Sie sicher, dass auf Ihrem **Hostcomputer** das Guest Additions ISO-Paket installiert ist.

- **Auf Arch / Manjaro:**
    ```bash
    sudo pacman -S virtualbox-guest-iso
    ```
- **Unter Debian / Ubuntu:**
    ```bash
    sudo apt install virtualbox-guest-additions-iso
    ```

### Schritt 3.2: Gastzusätze in der Ubuntu-VM installieren

Führen Sie diese Schritte **in Ihrer laufenden Ubuntu-VM** aus.

1. **Ubuntu vorbereiten:** Öffnen Sie ein Terminal und führen Sie die folgenden Befehle aus, um Build-Abhängigkeiten zu installieren.
    ```bash
    sudo apt update
    sudo apt install build-essential dkms linux-headers-$(uname -r)
    ```
2. **Legen Sie die CD ein:** Gehen Sie im oberen Menü von VirtualBox zu **Geräte -> CD-Image für Gastzusätze einfügen...**.
3. **Führen Sie das Installationsprogramm aus:**
- Möglicherweise wird ein Dialogfeld angezeigt, in dem Sie aufgefordert werden, die Software auszuführen. Klicken Sie auf **Ausführen**.
- Wenn kein Dialogfeld angezeigt wird, öffnen Sie den Dateimanager, klicken Sie mit der rechten Maustaste auf die CD „VBox_GAs...“, wählen Sie „Im Terminal öffnen“** und führen Sie den Befehl aus:
      ```bash
      sudo ./VBoxLinuxAdditions.run
      ```
4. **Neustart:** Nachdem die Installation abgeschlossen ist, starten Sie die VM neu.
    ```bash
    reboot
    ```
5. **Funktionen aktivieren:** Gehen Sie nach dem Neustart zum Menü **Geräte** und aktivieren Sie **Freigegebene Zwischenablage -> Bidirektional** und **Drag and Drop -> Bidirektional**.

Ihre stabile, leistungsstarke Testumgebung ist jetzt bereit.