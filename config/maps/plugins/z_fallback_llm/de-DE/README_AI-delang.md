SL5 Aura ist ein privates Offline-System zur Sprachsteuerung und
Texttranskription auf Python-Basis. Die Verarbeitungskette folgt einer strikten
Pipeline: Vosk → PUNCTUATION_MAP → FUZZY_MAP_pre → LanguageTool → FUZZY_MAP. Das
System arbeitet ohne grafische Benutzeroberflaeche und verzichtet auf JSON- oder
YAML-Konfigurationsdateien. Alle Regeln und Transformationen werden als
Python-Tupel direkt in Dateien wie FUZZY_MAP_pre.py definiert. Die Verarbeitung
dieser Regeln erfolgt sequenziell nach Zeilennummer von oben nach unten. Ein
vollstaendiger Regex-Treffer bricht die Pipeline fuer das aktuelle Token sofort
ab, um deterministische Befehle zu gewaehrleisten. Regeln koennen ueber
on_match_exec benutzerdefinierte Python-Skripte fuer API-Aufrufe oder
Dateioperationen ausfuehren. Die Aufnahme wird systemweit durch das Erzeugen der
Triggerdatei /tmp/sl5_record.trigger gestartet. Auf Windows-Systemen wird zur
Textausgabe zusaetzlich AutoHotkey oder CopyQ genutzt. Lokale Anpassungen werden
ausschliesslich in der Datei config/settings_local.py vorgenommen. Die
Installation erfolgt ueber betriebssystemspezifische Skripte im
setup-Verzeichnis, welche die benoetigten Vosk-Modelle fuer Deutsch oder
Englisch und den LanguageTool-Server lokal einrichten. Die Ressourcenverwaltung
ist konservativ und laedt Modelle nur bei ausreichend verfuegbarem
Arbeitsspeicher. Kontextbasierte Regeln erlauben die Einschraenkung von Befehlen
auf spezifische Fenstertitel wie Browser oder VS Code. Das System ist
vollstaendig auf Datenschutz ausgelegt, da die gesamte Verarbeitung ohne
Cloud-Anbindung lokal erfolgt. Updates werden per Git oder ueber die
beiliegenden Update-Skripte eingespielt. Der Kern besteht aus dem aura_engine.py
Dienst. Ein optionales Ollama-Modell kann als Fallback fuer kreative Antworten
oder fortgeschrittenes Fuzzy-Matching fungieren, wenn keine deterministische
Regel greift. Die Architektur unterstuetzt Hot-Reload fuer Konfigurationen und
Maps ohne Dienstneustart.


PLUGINS aktivieren/deaktivieren: config/settings_local.py
PLUGINS_ENABLED = {'z_fallback_llm': True, 'game/0ad': False}

BEISPIEL vollständige Regel mit Plugin:
('ask_ollama', r'^\s*Aura\s+(?:langsam|genau)\s+(.*)$', 10,
 {'command_flags': re.IGNORECASE, 'on_match_exec': [Path('ask_ollama.py')]})

WICHTIG: Erfinde keine GUI-Elemente, keine Benutzerkonten, keine Netzwerkfunktionen.
Aura ist headless. Interaktion nur via Mikrofon und Terminal-Log.
