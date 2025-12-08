# Feature-Spotlight: Command Line Interface (CLI)-Integration

**Gewidmet meinem sehr wichtigen Freund, Lub.**

Die neue, auf FastAPI basierende Command Line Interface (CLI)-Integration bietet eine saubere, synchrone Möglichkeit, unseren laufenden Kern-Textverarbeitungs-Service von jeder lokalen oder Remote-Shell aus anzusprechen. Diese robuste Lösung ist darauf ausgelegt, die Kernlogik nahtlos in Shell-Umgebungen zu integrieren.

---

## 1. Architektur und Synchrone CLI-Konzept

Der Service wird durch den **Uvicorn/FastAPI**-Server betrieben und verwendet einen benutzerdefinierten Endpunkt (`/process_cli`), um ein synchrones (blockierendes) Ergebnis von einem im Grunde asynchronen, dateibasierten Hintergrundprozess zu liefern.

### Strategie: Warten und Lesen (Polling)

Anstatt sofort zurückzukehren, implementiert der Endpunkt die folgenden Schritte, um die synchrone Erfahrung zu gewährleisten:

1.  **Eindeutiges Ausgabe-Override:** Die API erstellt für jede Anfrage ein eindeutiges temporäres Verzeichnis.
2.  **Prozessstart:** Sie ruft `process_text_in_background` auf, um die Kernlogik in einem nicht-blockierenden Thread auszuführen, der das Ergebnis in eine `tts_output_*.txt`-Datei innerhalb des eindeutigen Ordners schreibt.
3.  **Synchrones Warten:** Die API-Funktion **blockiert** dann und prüft ("pollt") das eindeutige Verzeichnis kontinuierlich, bis die Ausgabedatei erstellt oder ein Timeout erreicht wird.
4.  **Ergebnislieferung:** Die API liest den Inhalt der Datei, führt notwendige Aufräumarbeiten durch (Löschen der Datei und des temporären Verzeichnisses) und gibt den final verarbeiteten Text im Feld `result_text` der JSON-Antwort zurück.

Dies stellt sicher, dass der CLI-Client erst eine Antwort erhält, **nachdem** die Textverarbeitung abgeschlossen ist, und garantiert so ein zuverlässiges Shell-Erlebnis.

## 2. Fernzugriff und Netzwerk-Port-Mapping

Demo(manchmal online):

### SL5 Aura (external interface to the core logic)
**WICHTIG:** Die öffentliche IP-Adresse ändert sich täglich (DSL-Zwangstrennung).

Die aktuelle IP-Adresse für den Zugriff auf Port `8___` findest Du in dieser Textdatei:

[**Aktuelle IP-Adresse** (Klicken Sie hier)](http://88.130.216.60:8831/)

*Die IP-Adresse wird bei jedem Neustart des Dienstes automatisch aktualisiert (via GitHub Commit).*


Um den Zugriff von Remote-Clients zu ermöglichen, war die folgende Netzwerkkonfiguration erforderlich, die der gängigen Einschränkung begrenzter externer Port-Verfügbarkeit Rechnung trägt:

### Lösung: Externes Port-Mapping

Da der Service intern auf **Port 8000** läuft und unsere Netzwerkumgebung den externen Zugriff auf einen bestimmten Portbereich beschränkt (z.B. `88__-8831`), wurde ein **Port-Mapping** auf dem Router (Fritz!Box) implementiert.

| Endpunkt | Protokoll | Port | Beschreibung |
| :--- | :--- | :--- | :--- |
| **Extern/Öffentlich** | TCP | `88__` (Beispiel) | Der Port, den der Client (Lub) verwenden muss. |
| **Intern/Lokal** | TCP | `8000` | Der Port, auf dem der FastAPI-Service tatsächlich lauscht (`--port 8000`). |

Der Router übersetzt nun jede eingehende Verbindung auf dem externen Port (`88__`) auf den internen Port (`8000`) des Host-Rechners, wodurch der Service global zugänglich wird, ohne die Kernkonfiguration des Servers zu ändern.

## 3. Nutzung des CLI-Clients

Der Client muss mit der öffentlichen IP-Adresse, dem externen Port und dem korrekten API-Key konfiguriert werden.

### Finale Befehlssyntax

```bash
# Beachten Sie die Verwendung des externen Ports 88__ für den Fernzugriff
python3 cli_client.py "Was ist ein Haus" --lang "de-DE"
