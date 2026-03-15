# scripts/py/func/checks/test_trigger_end_to_end.py
"""
End-to-End Trigger Test für SL5 Aura – Abgeschnittene Wörter
=============================================================

WAS DIESER TEST PRÜFT
---------------------
Das bekannte Problem: Bei manchen Aufnahmen fehlt das letzte Wort im Output.

Ablauf:
1. Zeilenzahl von log/aura_engine.log merken
2. Settings auf MIC_AND_DESKTOP setzen (automatisch, wird zurückgesetzt)
3. touch /tmp/sl5_record.trigger  → Aura startet Session + erstellt mic_and_desktop_Sink
4. Warten bis mic_and_desktop_Sink existiert
5. WAV-Datei auf mic_and_desktop_Sink spielen
6. touch /tmp/sl5_record.trigger  → Aufnahme stoppen
7. Warten bis Aura "wrote to" ins Log schreibt
8. Output-Datei lesen
9. YouTube-Transcript für denselben Zeitraum holen
10. Vergleich: fehlt ein Wort am Ende?

VORAUSSETZUNGEN
---------------
- Aura muss laufen (./scripts/restart_venv_and_run-server.sh)
- WAV-Cache muss existieren (erst test_youtube_audio_regression.py laufen lassen)

STARTEN
-------
    SDL_VIDEODRIVER=dummy \\
      .venv/bin/pytest scripts/py/func/checks/test_trigger_end_to_end.py -v -s

WICHTIG
-------
Nicht sprechen während der Test läuft — Aura hört auf MIC_AND_DESKTOP (Mikrofon + Desktop).
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

import pytest

from ..manage_audio_routing import manage_audio_routing
from ..process_text_in_background import settings

# ---------------------------------------------------------------------------
# Pfade
# ---------------------------------------------------------------------------

REPO_ROOT    = Path(__file__).resolve().parents[4]
FIXTURE_DIR  = Path(__file__).parent / "fixtures" / "youtube_clips"
TRIGGER_FILE = Path("/tmp/sl5_record.trigger")
AURA_LOG     = REPO_ROOT / "log" / "aura_engine.log"


# ---------------------------------------------------------------------------
# Hilfsfunktionen – Log
# ---------------------------------------------------------------------------



def _log_line_count() -> int:
    if not AURA_LOG.exists():
        return 0
    with open(AURA_LOG, "r", encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def _new_log_lines(from_line: int) -> list[str]:
    if not AURA_LOG.exists():
        return []
    with open(AURA_LOG, "r", encoding="utf-8", errors="replace") as f:
        all_lines = f.readlines()
    return all_lines[from_line:]


def _wait_for_output(from_time: float, timeout: float = 30.0) -> Path | None:
    """
    Wartet auf eine neue tts_output_*.txt in /tmp/sl5_aura/
    die nach from_time erstellt wurde.
    """
    output_dir = Path("/tmp/sl5_aura/tts_output")

    deadline = time.time() + timeout
    while time.time() < deadline:
        if output_dir.exists():
            matches = [
                # tts_output_1773585429_0664139.txt
                f for f in output_dir.glob("tts_output_*.txt")
                if f.stat().st_mtime > from_time
            ]
            if matches:
                return max(matches, key=lambda f: f.stat().st_mtime)
        time.sleep(0.5)
    return None


# ---------------------------------------------------------------------------
# Hilfsfunktionen – Audio
# ---------------------------------------------------------------------------



def _wait_for_mic_and_desktop_sink(timeout: float = 8.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = subprocess.run(
            ["pactl", "list", "sinks", "short"],
            capture_output=True, text=True
        )
        if "mic_and_desktop_Sink" in result.stdout:
            return True
        time.sleep(0.3)
    return False


def _pulse_running() -> bool:
    result = subprocess.run(["pactl", "info"], capture_output=True, text=True)
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Hilfsfunktionen – Settings
# ---------------------------------------------------------------------------

def _set_audio_input_device(value: str) -> None:
    settings_file = REPO_ROOT / "config" / "settings_local.py"
    content = settings_file.read_text(encoding="utf-8") if settings_file.exists() else ""
    marker_start = "# AURA_TEST_OVERRIDE_START"
    marker_end = "# AURA_TEST_OVERRIDE_END"
    clean = re.sub(rf"{marker_start}.*?{marker_end}\n?", "", content, flags=re.DOTALL)
    new_content = clean.rstrip() + f"\n{marker_start}\nAUDIO_INPUT_DEVICE = '{value}'\n{marker_end}\n"
    settings_file.write_text(new_content, encoding="utf-8")


def _remove_audio_input_device_override() -> None:
    settings_file = REPO_ROOT / "config" / "settings_local.py"
    if not settings_file.exists():
        return
    content = settings_file.read_text(encoding="utf-8")
    marker_start = "# AURA_TEST_OVERRIDE_START"
    marker_end = "# AURA_TEST_OVERRIDE_END"
    clean = re.sub(rf"{marker_start}.*?{marker_end}\n?", "", content, flags=re.DOTALL)
    settings_file.write_text(clean, encoding="utf-8")
    
def _create_mic_and_desktop_sink() -> bool:
    subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
    subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
    time.sleep(0.3)
    r1 = subprocess.run([
        "pactl", "load-module", "module-null-sink",
        "sink_name=mic_and_desktop_Sink"
    ], capture_output=True, text=True)
    if r1.returncode != 0:
        return False
    r2 = subprocess.run([
        "pactl", "load-module", "module-loopback",
        "source=@DEFAULT_SOURCE@",
        "sink=mic_and_desktop_Sink"
    ], capture_output=True, text=True)
    return r2.returncode == 0

# ---------------------------------------------------------------------------
# Hilfsfunktionen – YouTube Transcript
# ---------------------------------------------------------------------------

def _fetch_yt_transcript_segment(
    video_id: str, start_sec: float, end_sec: float, language: str = "de"
) -> str:
    cache = FIXTURE_DIR / f"trigger_test_{video_id}_{int(start_sec)}_{int(end_sec)}.transcript.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))["text"]

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        transcript_list = list(api.fetch(video_id, languages=[language, "en"]))
    except Exception as exc:
        pytest.skip(f"YouTube-Transcript nicht abrufbar: {exc}")

    words = []
    for entry in transcript_list:
        entry_start = entry.start
        entry_end = entry_start + getattr(entry, "duration", 0)
        if entry_end >= start_sec and entry_start <= end_sec:
            words.append(entry.text.strip())

    text = " ".join(words)
    text = re.sub(r'>>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    cache.write_text(
        json.dumps({"text": text}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return text


# ---------------------------------------------------------------------------
# Der Test
# ---------------------------------------------------------------------------

def test_trigger_no_word_cutoff():
    """
    Spielt eine WAV-Datei über mic_and_desktop_Sink ein,
    triggert Aura wie im echten Betrieb (touch trigger-file zweimal),
    und prüft ob das letzte Wort im Output fehlt.
    """

    # --- Voraussetzungen prüfen ---
    if not AURA_LOG.exists():
        pytest.skip("log/aura_engine.log nicht gefunden — läuft Aura?")

    if not _pulse_running():
        pytest.skip("PulseAudio/PipeWire läuft nicht (pactl info fehlgeschlagen)")

    wav_file = FIXTURE_DIR / "sl5_aura_demo_en_v1_aura.wav"
    if not wav_file.exists():
        pytest.skip(
            f"WAV-Datei nicht gefunden: {wav_file}\n"
            "Erst test_youtube_audio_regression.py laufen lassen."
        )

    # --- Konfiguration ---
    VIDEO_ID     = "sOjRNICiZ7Q"
    START_SEC    = 60.0
    END_SEC      = 70.0
    WAV_DURATION = 10.0

    # --- YouTube-Transcript als Referenz ---
    yt_ref = _fetch_yt_transcript_segment(VIDEO_ID, START_SEC, END_SEC, language="de")
    yt_words = yt_ref.lower().split()
    print(f"\nYT ref ({len(yt_words)} Wörter): ...{' '.join(yt_words[-5:])}")

    # --- Log-Position merken ---
    # log_line_before = _log_line_count()
    time_before = time.time()
    print(f"time_before vor Test: {time_before}")

    original_default_source = subprocess.check_output(["pactl", "get-default-source"]).decode().strip()
    try:


        # TRIGGER_FILE.touch()
        # time.sleep(1.0)

        mode="MIC_AND_DESKTOP"
        _set_audio_input_device(mode)
        time.sleep(3)

        # manage_audio_routing(mode)
        manage_audio_routing(settings.AUDIO_INPUT_DEVICE)

        # time.sleep(0.5)

        TRIGGER_FILE.touch()
        print("Trigger 1 gesetzt")


        time.sleep(0.1)


        if not _wait_for_mic_and_desktop_sink(timeout=8.0):
            pytest.skip("mic_and_desktop_Sink nicht gefunden")
        print("mic_and_desktop_Sink bereit")

        # TRIGGER_FILE.touch()
        # print("Trigger 1b gesetzt")


        # --- WAV einspeisen ---
        print(f"Spiele WAV ein: {wav_file.name}")
        play_proc = subprocess.Popen([
            "paplay",
            "--device", "mic_and_desktop_Sink",
            str(wav_file)
        ])
        try:
            play_proc.wait(timeout=WAV_DURATION + 5)
        except subprocess.TimeoutExpired:
            play_proc.kill()
            play_proc.wait()
        print("WAV-Wiedergabe beendet")

        time.sleep(0.01)

        # --- Trigger 2: Aufnahme stoppen ---
        TRIGGER_FILE.touch()
        print("Trigger 2 gesetzt")

        # --- Warten auf Aura-Output ---
        print("Warte auf Aura-Output (max 30s)...")
        output_file = _wait_for_output(time_before, timeout=30.0)

        if output_file is None:
            pytest.fail(
                "Aura hat innerhalb von 30s keinen Output produziert.\n"
            )

        # --- Output lesen ---
        aura_text = output_file.read_text(encoding="utf-8-sig").strip()
        aura_words = aura_text.lower().split()

        # --- Ergebnis ausgeben ---
        print(f"\n{'=' * 60}")
        print(f"YT ref  : {yt_ref}")
        print(f"Aura    : {aura_text}")
        print(f"YT  letztes Wort : '{yt_words[-1] if yt_words else '?'}'")
        print(f"Aura letztes Wort: '{aura_words[-1] if aura_words else '?'}'")
        print(f"YT  Wortanzahl   : {len(yt_words)}")
        print(f"Aura Wortanzahl  : {len(aura_words)}")
        if yt_words:
            print(f"Wort-Abdeckung   : {len(aura_words) / len(yt_words):.1%}")
        print(f"{'=' * 60}")

        # --- Assertions ---
        assert aura_text, "Aura hat leeren Output produziert"

        if yt_words:
            coverage = len(aura_words) / len(yt_words)
            assert coverage >= 0.50, (
                f"Aura Output hat nur {coverage:.1%} der erwarteten Wortanzahl.\n"
                f"YT  : {yt_ref}\n"
                f"Aura: {aura_text}"
            )

    except Exception as e:
        print(f"ERROR: {e}")


    finally:
        _remove_audio_input_device_override()
        time.sleep(0.05)
        manage_audio_routing(settings.AUDIO_INPUT_DEVICE)
        subprocess.run(["pactl", "set-default-source", original_default_source], capture_output=True)

        print("Test beendet")
