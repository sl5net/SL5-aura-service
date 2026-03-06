# Feature Spotlight: Command Line Interface (CLI)-Integration

**Meinem sehr wichtigen Freund Lub gewidmet.**

Die neue FastAPI-basierte Befehlszeilenschnittstelle (CLI) bietet eine saubere, synchrone Möglichkeit, von jeder lokalen oder Remote-Shell aus mit unserem laufenden Kerntextverarbeitungsdienst zu interagieren. Dabei handelt es sich um eine robuste Lösung zur Integration der Kernlogik in Shell-Umgebungen.

---

## 1. Architektur und synchrones CLI-Konzept

Der Dienst wird vom **Uvicorn/FastAPI**-Server betrieben und verwendet einen benutzerdefinierten Endpunkt („/process_cli“), um ein synchrones (blockierendes) Ergebnis aus einem inhärent asynchronen, dateibasierten Hintergrundprozess zu liefern.

### Wait-and-Read-Polling-Strategie

1. **Eindeutige Ausgabeüberschreibung:** Die API erstellt für jede Anfrage ein eindeutiges temporäres Verzeichnis.
2. **Prozessstart:** Es ruft „process_text_in_background“ auf, um die Kernlogik in einem nicht blockierenden Thread auszuführen, und schreibt das Ergebnis in eine „tts_output_*.txt“-Datei in diesem eindeutigen Ordner.
3. **Synchronous Wait:** Die API-Funktion **blockiert** und fragt dann den eindeutigen Ordner ab, bis die Ausgabedatei erstellt wird oder ein Timeout erreicht wird.
4. **Ergebnislieferung:** Die API liest den Inhalt der Datei, führt die erforderliche Bereinigung durch (Löschen der Datei und des temporären Verzeichnisses) und gibt den endgültig verarbeiteten Text im Feld „result_text“ der JSON-Antwort zurück.

Dadurch wird sichergestellt, dass der CLI-Client erst eine Antwort erhält, *nachdem* die Textverarbeitung abgeschlossen ist, was ein zuverlässiges Shell-Erlebnis gewährleistet.

## 2. Fernzugriff und Netzwerk-Port-Zuordnung

Um den Zugriff von Remote-Clients wie dem Terminal von Lub zu ermöglichen, war die folgende Netzwerkkonfiguration erforderlich, um die allgemeine Einschränkung der begrenzten Verfügbarkeit externer Ports zu berücksichtigen:

### Lösung: Externe Portzuordnung

Da der Dienst intern auf **Port 8000** läuft und unsere Netzwerkumgebung den externen Zugriff auf einen bestimmten Portbereich (z. B. „88__-8831“) beschränkt, haben wir **Port Mapping** auf dem Router (Fritz!Box) implementiert.

| Endpunkt | Protokoll | Hafen | Beschreibung |
| :--- | :--- | :--- | :--- |
| **Extern/Öffentlich** | TCP | „88__“ (Beispiel) | Der Port, den der Client (Lub) verwenden muss. |
| **Intern/Lokal** | TCP | „8000“ | Der Port, den der FastAPI-Dienst tatsächlich überwacht („--port 8000“). |

Der Router übersetzt jede eingehende Verbindung am externen Port („88__“) in den internen Port („8000“) des Host-Computers und macht so den Dienst global zugänglich, ohne die Konfiguration des Kernservers zu ändern.

## 3. CLI-Client-Nutzung

Der Client muss mit der öffentlichen IP-Adresse, dem externen Port und dem richtigen API-Schlüssel konfiguriert sein.

### Endgültige Befehlssyntax

__CODE_BLOCK_0__