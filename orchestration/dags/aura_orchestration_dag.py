"""
aura_orchestration_dag.py
=========================
Apache Airflow DAG für das SL5 Aura Framework.

Pipelines:
  1. WIKIPEDIA-UPDATE   – Prüft auf neue .zim-Datei, baut Such-Index neu auf.
  2. QUIZ-VALIDIERUNG   – Extrahiert, validiert und veröffentlicht quiz_db.json.

Autor : SL5 / Senior Software Engineer AI/Cloud
Airflow: 2.x  |  Python: 3.10+
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from airflow import DAG
from airflow.decorators import task
from airflow.exceptions import AirflowSkipException
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

# ---------------------------------------------------------------------------
# Globale Konfiguration – per Airflow Variable überschreibbar
# ---------------------------------------------------------------------------

# Airflow Variables
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

AURA_BASE_DIR   = PROJECT_ROOT
ZIM_WATCH_DIR   = PROJECT_ROOT / "data"
QUIZ_DB_PATH    = PROJECT_ROOT / "config/maps/plugins/anki_quiz/de-DE/quiz_db.json"
QUIZ_PUB_PATH   = PROJECT_ROOT / "config/maps/plugins/anki_quiz/de-DE/quiz_db_published.json"
INDEX_BUILD_CMD = "echo '[SIMULATED] Rebuilding Aura search index…'"


# AURA_BASE_DIR   = Path(Variable.get("aura_base_dir",   default_var="/opt/aura"))
# ZIM_WATCH_DIR   = Path(Variable.get("zim_watch_dir",   default_var=str(AURA_BASE_DIR / "data/zim")))
# QUIZ_DB_PATH    = Path(Variable.get("quiz_db_path",    default_var=str(AURA_BASE_DIR / "data/quiz_db.json")))
# QUIZ_PUB_PATH   = Path(Variable.get("quiz_pub_path",   default_var=str(AURA_BASE_DIR / "published/quiz_db.json")))
# INDEX_BUILD_CMD = Variable.get("index_build_cmd",      default_var="echo '[SIMULATED] Rebuilding Aura search index…'")

log = logging.getLogger("aura.dag")

# ---------------------------------------------------------------------------
# Standard-Argumente – gelten für jeden Task im DAG
# ---------------------------------------------------------------------------

DEFAULT_ARGS: dict[str, Any] = {
    "owner"           : "aura-team",
    "depends_on_past" : False,                  # kein Task wartet auf Vortag
    "retries"         : 2,                      # 2 Wiederholungen bei Fehler
    "retry_delay"     : timedelta(minutes=5),
    "email_on_failure": False,                  # auf True + SMTP setzen für Prod
}

# ---------------------------------------------------------------------------
# JSON-Schema für quiz_db.json  (vereinfachter Schema-Validator ohne Deps)
# ---------------------------------------------------------------------------

QUIZ_SCHEMA: dict[str, Any] = {
    "required_keys_per_item": ["display", "correct"],
    "min_questions": 1,
}

def _validate_quiz_schema(data: list) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, list):
        errors.append("Root muss eine Liste sein.")
        return errors
    if len(data) < QUIZ_SCHEMA["min_questions"]:
        errors.append(f"Mindestens {QUIZ_SCHEMA['min_questions']} Frage(n) erforderlich.")
    for i, q in enumerate(data):
        for field in QUIZ_SCHEMA["required_keys_per_item"]:
            if field not in q:
                errors.append(f"Frage[{i}]: Fehlendes Feld '{field}'.")
    return errors


# ===========================================================================
# PIPELINE 1 – WIKIPEDIA-UPDATE
# ===========================================================================

with DAG(
    dag_id="aura_wikipedia_update",
    description="Prüft auf neue wikipedia_de_all_mini.zim und baut den Aura-Suchindex neu.",
    schedule="@daily",                          # täglich um Mitternacht
    start_date=datetime(2024, 1, 1),
    catchup=False,                              # kein Backfill vergangener Runs
    tags=["aura", "wikipedia", "index"],
    default_args=DEFAULT_ARGS,
    doc_md=__doc__,
) as wiki_dag:

    # --- Task 1: Prüfe, ob neue .zim-Datei vorhanden ---

    @task(task_id="check_new_zim_file")
    def check_new_zim_file() -> str:
        """
        Sucht nach 'wikipedia_de_all_mini.zim' im Watch-Verzeichnis.
        Gibt den vollständigen Pfad zurück, wenn gefunden.
        Wirft AirflowSkipException → alle nachgelagerten Tasks werden übersprungen.
        """
        zim_path = ZIM_WATCH_DIR / "wikipedia_de_all_mini.zim"
        log.info("Suche ZIM-Datei unter: %s", zim_path)

        if not zim_path.exists():
            log.info("Keine neue ZIM-Datei gefunden. Pipeline wird übersprungen.")
            raise AirflowSkipException("wikipedia_de_all_mini.zim nicht vorhanden.")

        file_size_mb = zim_path.stat().st_size / (1024 ** 2)
        log.info("ZIM-Datei gefunden: %s (%.1f MB)", zim_path, file_size_mb)
        return str(zim_path)           # Rückgabewert → XCom

    # --- Task 2: Such-Index neu aufbauen ---

    @task(task_id="rebuild_search_index")
    def rebuild_search_index(zim_path: str) -> None:
        """
        Triggert den Index-Rebuild für Aura.
        Erhält den ZIM-Pfad über XCom vom vorherigen Task.
        Im Produktionsbetrieb: subprocess.run([...], check=True).
        """
        log.info("Starte Index-Rebuild für: %s", zim_path)
        # Simulierter Aufruf – in Prod: subprocess.run(INDEX_BUILD_CMD, shell=True, check=True)
        simulated_output = f"[SIMULATED] Index für {Path(zim_path).name} erfolgreich aufgebaut."
        log.info(simulated_output)

    # --- Task 3: Erfolgsmeldung ---

    @task(task_id="notify_success")
    def notify_success() -> None:
        """Loggt eine Erfolgsmeldung. Erweiterbar mit Slack/E-Mail-Hook."""
        log.info("✅ AURA WIKIPEDIA-UPDATE abgeschlossen – Suchindex ist aktuell.")

    # --- DAG-Fluss verdrahten ---
    zim_path_xcom = check_new_zim_file()
    rebuild_search_index(zim_path_xcom) >> notify_success()


# ===========================================================================
# PIPELINE 2 – QUIZ-DATEN-VALIDIERUNG (Data Quality Gate)
# ===========================================================================

with DAG(
    dag_id="aura_quiz_validation",
    description="Extrahiert, validiert und veröffentlicht quiz_db.json für Aura.",
    schedule="0 3 * * *",                       # täglich 03:00 Uhr
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["aura", "quiz", "data-quality"],
    default_args=DEFAULT_ARGS,
    doc_md=__doc__,
) as quiz_dag:

    start = EmptyOperator(task_id="start")      # visueller Einstiegspunkt im UI

    # --- Task 1: Daten extrahieren ---

    @task(task_id="extract_quiz_data")
    def extract_quiz_data() -> list:
        """
        Liest quiz_db.json ein und gibt den Inhalt als Dictionary zurück.
        Fehler beim Lesen → Task schlägt fehl (kein Retry sinnvoll → retries=0 wäre hier optional).
        """
        log.info("Lese Quiz-Datenbank: %s", QUIZ_DB_PATH)

        if not QUIZ_DB_PATH.exists():
            raise FileNotFoundError(f"quiz_db.json nicht gefunden: {QUIZ_DB_PATH}")

        with QUIZ_DB_PATH.open(encoding="utf-8") as fh:
            data = json.load(fh)

        log.info("Erfolgreich geladen: %d Frage(n) gefunden.", len(data))
        return data   # → XCom (serialisiert als JSON)

    # --- Task 2: Schema validieren ---

    @task(task_id="validate_quiz_schema")
    def validate_quiz_schema(data: dict) -> dict:
        """
        Data-Quality-Gate: Validiert Struktur und Vollständigkeit der Quiz-Daten.
        Bei Fehlern wird eine ValueError mit Detailbericht geworfen → Task schlägt fehl.
        Gibt die validierten Daten weiter (Pass-through-Pattern).
        """
        log.info("Starte Schema-Validierung…")
        errors = _validate_quiz_schema(data)

        if errors:
            error_report = "\n  – ".join([""] + errors)
            log.error("Schema-Validierung fehlgeschlagen:%s", error_report)
            raise ValueError(f"Quiz-Daten ungültig ({len(errors)} Fehler). Details: {error_report}")

        log.info("✅ Schema-Validierung bestanden. %d Frage(n) korrekt.", len(data["questions"]))
        return data

    # --- Task 3: Daten veröffentlichen ---

    @task(task_id="publish_quiz_data")
    def publish_quiz_data(validated_data: dict) -> None:
        """
        Schreibt validierte Daten in das Aura-Published-Verzeichnis.
        Atomares Schreiben via temporäre Datei + Rename verhindert korrupte Reads.
        """
        QUIZ_PUB_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = QUIZ_PUB_PATH.with_suffix(".tmp")

        with tmp_path.open("w", encoding="utf-8") as fh:
            json.dump(validated_data, fh, ensure_ascii=False, indent=2)

        tmp_path.rename(QUIZ_PUB_PATH)          # atomarer Swap
        log.info("✅ Quiz-Daten veröffentlicht nach: %s", QUIZ_PUB_PATH)

    # --- Fehler-Handler (läuft auch bei Skip/Failure) ---

    @task(task_id="handle_validation_error", trigger_rule=TriggerRule.ONE_FAILED)
    def handle_validation_error() -> None:
        """
        Wird nur ausgelöst, wenn ein vorgelagerter Task fehlschlägt.
        TriggerRule.ONE_FAILED = Gegenstück zu ALL_SUCCESS (Standard).
        Erweiterbar: PagerDuty, Slack-Alert, Dead-Letter-Queue.
        """
        log.error("❌ AURA QUIZ-PIPELINE fehlgeschlagen – manuelle Prüfung erforderlich.")

    # --- DAG-Fluss verdrahten ---
    raw_data      = extract_quiz_data()
    valid_data    = validate_quiz_schema(raw_data)
    publish       = publish_quiz_data(valid_data)

    # Fehler-Branch parallel zur Happy-Path verdrahten
    start >> raw_data
    [publish, raw_data, valid_data] >> handle_validation_error()
