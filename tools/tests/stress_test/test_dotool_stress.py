#!/usr/bin/env python3
# tools/test_dotool_stress.py
# Stress-Test fuer dotool unter Wayland/X11.
# Schreibt 100 lange Saetze nacheinander in den tts_output-Ordner
# und protokolliert Timing-Anomalien.

import os
import sys
import time
import random
import uuid
from pathlib import Path
from datetime import datetime

# --- KONFIGURATION ---
OUTPUT_DIR = Path("/tmp/sl5_aura/tts_output")
LOG_FILE = Path("log/test_dotool_stress.log")
NUM_ITERATIONS = 100
MIN_SENTENCE_WORDS = 15
MAX_SENTENCE_WORDS = 35
PAUSE_BETWEEN_SENTENCES_SEC = 0.8  # Zeit fuer type_watcher zum Tippen
TIMEOUT_PER_SENTENCE_SEC = 8.0     # Max. Zeit, die ein Satz zum Tippen brauchen darf

# Lange deutsche Woerter fuer realistische Last
WORD_POOL = [
    "Programmierung", "Entwicklung", "Software", "Anwendung", "Benutzer",
    "Oberflaeche", "Funktionalitaet", "Implementierung", "Architektur",
    "Komponente", "Schnittstelle", "Datenbank", "Algorithmus", "Variable",
    "Funktion", "Methode", "Klasse", "Objekt", "Vererbung", "Polymorphie",
    "Kapselung", "Modularitaet", "Wiederverwendbarkeit", "Effizienz",
    "Performance", "Optimierung", "Refactoring", "Debugging", "Testing",
    "Deployment", "Integration", "Versionskontrolle", "Repository",
    "Branch", "Commit", "Merge", "Konflikt", "Pull", "Request",
    "Dokumentation", "Spezifikation", "Anforderung", "Use", "Case",
    "User", "Story", "Sprint", "Backlog", "Scrum", "Agil", "Wasserfall",
    "Modell", "Prozess", "Workflow", "Automatisierung", "Skript",
    "Konfiguration", "Parameter", "Argument", "Rueckgabewert",
    "Exception", "Fehlerbehandlung", "Logging", "Monitoring",
    "Skalierbarkeit", "Verfuegbarkeit", "Zuverlaessigkeit", "Sicherheit"
]

PUNCTUATION = [".", "!", "?", ";"]


def generate_sentence():
    """Generiert einen zufaelligen, langen deutschen Satz."""
    num_words = random.randint(MIN_SENTENCE_WORDS, MAX_SENTENCE_WORDS)
    words = [random.choice(WORD_POOL) for _ in range(num_words)]
    sentence = " ".join(words) + random.choice(PUNCTUATION)
    return sentence


def log_message(msg: str):
    """Schreibt eine Zeile ins Log und auf stdout."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def wait_for_file_consumption(filepath: Path, timeout_sec: float) -> bool:
    """
    Wartet bis die Datei vom type_watcher konsumiert (geloescht) wurde.
    Gibt True zurueck, wenn die Datei rechtzeitig verschwunden ist.
    """
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if not filepath.exists():
            return True
        time.sleep(0.05)
    return False


def main():
    os.environ["PYTHONUTF8"] = "1"

    # Sicherstellen, dass der Output-Ordner existiert
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    log_message("=" * 60)
    log_message(f"STRESS-TEST START: {NUM_ITERATIONS} Iterationen")
    log_message(f"Output-Dir: {OUTPUT_DIR}")
    log_message(f"Log-File:   {LOG_FILE}")
    log_message("=" * 60)

    anomalies = []
    total_start = time.time()

    for i in range(1, NUM_ITERATIONS + 1):
        sentence = generate_sentence()
        unique_id = uuid.uuid4().hex[:8]
        filename = f"tts_output_{int(time.time() * 1000)}_{unique_id}.txt"
        filepath = OUTPUT_DIR / filename

        iter_start = time.time()

        # Datei schreiben
        filepath.write_text(sentence, encoding="utf-8")
        log_message(f"[{i}/{NUM_ITERATIONS}] WRITTEN  ({len(sentence)} chars): {filename[:40]}...")

        # Warten bis type_watcher die Datei konsumiert hat
        consumed = wait_for_file_consumption(filepath, TIMEOUT_PER_SENTENCE_SEC)
        iter_duration = time.time() - iter_start

        if not consumed:
            warning = f"[{i}/{NUM_ITERATIONS}] TIMEOUT: Datei nach {TIMEOUT_PER_SENTENCE_SEC:.1f}s noch vorhanden!"
            log_message(f"  ANOMALIE: {warning}")
            anomalies.append({
                "iteration": i,
                "type": "timeout",
                "filename": filename,
                "duration_sec": iter_duration,
                "text_length": len(sentence)
            })
            # Versuchen, die Datei zu bereinigen, damit der Test weiterlaeuft
            try:
                filepath.unlink(missing_ok=True)
            except Exception:
                pass
        else:
            log_message(f"[{i}/{NUM_ITERATIONS}] CONSUMED in {iter_duration:.2f}s")

            # Warnung bei ungewoehnlich langer Verarbeitungszeit
            if iter_duration > TIMEOUT_PER_SENTENCE_SEC * 0.5:
                warning = f"[{i}/{NUM_ITERATIONS}] SLOW: {iter_duration:.2f}s fuer {len(sentence)} Zeichen"
                log_message(f"  WARNUNG: {warning}")
                anomalies.append({
                    "iteration": i,
                    "type": "slow",
                    "filename": filename,
                    "duration_sec": iter_duration,
                    "text_length": len(sentence)
                })

        # Kurze Pause, bevor der naechste Satz kommt
        time.sleep(PAUSE_BETWEEN_SENTENCES_SEC)

    total_duration = time.time() - total_start

    # Zusammenfassung
    log_message("=" * 60)
    log_message("STRESS-TEST BEENDET")
    log_message(f"Gesamtdauer:     {total_duration:.1f}s")
    log_message(f"Iterationen:     {NUM_ITERATIONS}")
    log_message(f"Anomalien:       {len(anomalies)}")
    if anomalies:
        log_message("Anomalien-Details:")
        for a in anomalies:
            log_message(f"  - Iter {a['iteration']}: {a['type']} | "
                        f"{a['duration_sec']:.2f}s | {a['text_length']} chars")
    else:
        log_message("Keine Anomalien festgestellt.")
    log_message("=" * 60)

    # Exit-Code: 1 wenn Anomalien gefunden
    sys.exit(1 if anomalies else 0)


if __name__ == "__main__":
    main()
