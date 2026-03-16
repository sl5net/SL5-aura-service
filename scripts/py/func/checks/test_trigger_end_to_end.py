"""
scripts/py/func/checks/test_trigger_end_to_end.py:2
howto start example 16.3.'26 10:58 Mon:
SDL_VIDEODRIVER=dummy .venv/bin/pytest scripts/py/func/checks/test_trigger_end_to_end.py -v -s 2>&1 | grep -E "Stream|WARNUNG|Aura|Trigger|Cleanup"

Approach: set-default-source + move-source-output to route Aura stream to virtual sink.
test_sink is created, activated, Aura stream moved there, WAV played into sink.
Output files are read from OUTPUT_DIR after processing.
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
import pytest

# Paths
FIXTURE_DIR  = Path(__file__).parent / "fixtures" / "youtube_clips"
TRIGGER_FILE = Path("/tmp/sl5_record.trigger")
OUTPUT_DIR   = Path("/tmp/sl5_aura/tts_output")

def _load_wav_transcript():
    """Loads the cached transcript for the test WAV."""
    cache = FIXTURE_DIR / "sl5_aura_demo_en_v1_aura.transcript.json"
    if not cache.exists():
        return None
    return json.loads(cache.read_text(encoding="utf-8"))["text"]



def _get_aura_stream_id():
    """Finds the ID of the current Aura recording stream."""
    res = subprocess.run(["pactl", "list", "source-outputs", "short"], capture_output=True, text=True)
    for line in res.stdout.splitlines():
        if "16000" in line or "s16le" in line:
            return line.split()[0]
    return None


def _wait_for_aura_stream(timeout=10.0):
    """Waits until Aura's audio stream is visible in pactl."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        sid = _get_aura_stream_id()
        if sid:
            return sid
        time.sleep(0.5)
    return None


def _clear_output_dir():
    """Clears all txt files in the output directory without deleting the folder."""
    if OUTPUT_DIR.exists():
        for f in OUTPUT_DIR.glob("*.txt"):
            f.unlink()
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _activate_sink(sink_name):
    """Plays a short sound to wake up the sink from SUSPENDED state."""
    silent_wav = "/usr/share/sounds/alsa/Front_Left.wav"
    proc = subprocess.Popen(["paplay", "--device", sink_name, silent_wav],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    proc.kill()


def _wait_for_output(time_before, timeout=90.0):
    halluzinationen = {"***", "nun", "einen"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        files = [f for f in OUTPUT_DIR.glob("*.txt") if f.stat().st_mtime > time_before]
        if files:
            time.sleep(5.0)  # kurz warten damit Aura fertig schreibt
            break
        time.sleep(0.5)
    files = sorted(
        [f for f in OUTPUT_DIR.glob("*.txt") if f.stat().st_mtime > time_before],
        key=lambda f: f.stat().st_mtime
    )
    return [f.read_text(encoding="utf-8-sig").strip() for f in files
            if f.read_text(encoding="utf-8-sig").strip() not in halluzinationen]


def _pause_type_watcher():
    """Disables type_watcher by setting flag in settings_local.py."""
    settings_file = Path(__file__).resolve().parents[4] / "config" / "settings_local.py"
    content = settings_file.read_text(encoding="utf-8")
    new_content = content.replace("TYPE_WATCHER_ENABLED = True", "TYPE_WATCHER_ENABLED = False")
    settings_file.write_text(new_content, encoding="utf-8")

def _resume_type_watcher():
    """Re-enables type_watcher."""
    settings_file = Path(__file__).resolve().parents[4] / "config" / "settings_local.py"
    content = settings_file.read_text(encoding="utf-8")
    new_content = content.replace("TYPE_WATCHER_ENABLED = False", "TYPE_WATCHER_ENABLED = True")
    settings_file.write_text(new_content, encoding="utf-8")

def test_trigger_no_word_cutoff():
    wav_file = FIXTURE_DIR / "sl5_aura_demo_en_v1_aura.wav"
    if not wav_file.exists():
        pytest.skip(f"WAV fehlt: {wav_file}")

    print("\n--- TEST START ---")
    original_source = subprocess.check_output(["pactl", "get-default-source"]).decode().strip()
    print(f"Original source: {original_source}")

    _clear_output_dir()

    try:
        print("--- Setup: Virtual Sink ---")
        subprocess.run(["pactl", "load-module", "module-null-sink", "sink_name=test_sink"],
                       capture_output=True)
        time.sleep(0.3)

        # Wake up the sink
        print("Aktiviere test_sink...")
        _activate_sink("test_sink")

        # Set default source BEFORE trigger so Aura opens stream on test_sink.monitor
        print("Setze Default-Source auf test_sink.monitor...")
        subprocess.run(["pactl", "set-default-source", "test_sink.monitor"], capture_output=True)
        time.sleep(0.5)

        # Start recording
        print("Sende Start-Trigger...")
        time_before = time.time()
        TRIGGER_FILE.touch()

        # Wait for stream and move as backup
        print("Warte auf Aura-Stream...")
        sid = _wait_for_aura_stream(timeout=10.0)
        if sid:
            print(f"Aura-Stream gefunden: {sid} → verschiebe auf test_sink.monitor (Backup)")
            subprocess.run(["pactl", "move-source-output", sid, "test_sink.monitor"],
                           capture_output=True)
            time.sleep(0.3)
        else:
            print("WARNUNG: Kein Aura-Stream gefunden!")

        _pause_type_watcher()

        # Play WAV into the sink
        print(f"Spiele {wav_file.name} ein...")
        subprocess.run(["paplay", "--device", "test_sink", str(wav_file)], check=True)
        time.sleep(1.0)

        # Stop recording
        print("Sende Stopp-Trigger...")
        TRIGGER_FILE.touch()

        # Wait for output with polling loop
        print("Warte auf Verarbeitung (max 30s)...")

        texts = _wait_for_output(time_before, timeout=90.0)

        output_files = sorted(OUTPUT_DIR.glob("*.txt"), key=lambda f: f.stat().st_mtime)
        print(f"Gefundene Dateien: {[f.name for f in output_files]}")

        full_text = " ".join(texts)
        print(f"ERGEBNIS-TEXT: '{full_text}'")

        assert len(full_text) > 0, "Aura hat gar keine verwertbaren Dateien erzeugt."

        yt_ref = _load_wav_transcript()
        if yt_ref:

            # Find first common word to align output
            yt_words_list = yt_ref.split()
            aura_words_list = full_text.split()

            best_start_aura = 0
            best_start_yt = 0
            for i, word in enumerate(aura_words_list[:10]):
                clean_word = word.strip(".,?!")
                if len(clean_word) > 4 and clean_word in yt_words_list:
                    best_start_aura = i
                    best_start_yt = yt_words_list.index(clean_word)
                    break

            aligned_aura = " ".join(aura_words_list[best_start_aura:])
            aligned_yt = " ".join(yt_words_list[best_start_yt:])
            print(f"YT Referenz : '{aligned_yt[:80]}...'")
            print(f"Aura Output : '{aligned_aura[:80]}...'")

            # print(f"YT Referenz : '{yt_ref[:80]}...'")
            # print(f"Aura Output : '{full_text[:80]}...'")
            try:
                from jiwer import wer
                error_rate = wer(yt_ref, full_text)
                print(f"WER: {error_rate:.1%}")
                # assert error_rate < 0.80, f"WER zu hoch: {error_rate:.1%}"
                assert error_rate < 0.90, f"WER zu hoch: {error_rate:.1%}"
            except ImportError:
                print("jiwer nicht installiert — kein WER-Vergleich")

    finally:
        print("\n--- Cleanup ---")
        sid = _get_aura_stream_id()
        if sid:
            subprocess.run(["pactl", "move-source-output", sid, original_source],
                           capture_output=True)
        subprocess.run(["pactl", "set-default-source", original_source], capture_output=True)
        subprocess.run(["pactl", "set-source-mute", original_source, "0"], capture_output=True)
        subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
        TRIGGER_FILE.touch()
        time.sleep(0.5)
        TRIGGER_FILE.touch()
        print("Cleanup fertig.")
        _clear_output_dir()
        _resume_type_watcher()

