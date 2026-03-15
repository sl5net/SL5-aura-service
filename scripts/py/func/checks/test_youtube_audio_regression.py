"""
Audio Regression Tests for SL5 Aura – YouTube Transcript Comparison
=====================================================================

HOW IT WORKS
------------
1. Each test fixture defines a YouTube video + a time segment (start/end seconds).
2. The audio clip is downloaded once (cached locally) via yt-dlp.
3. The official YouTube auto-transcript is fetched (cached) via youtube-transcript-api.
4. SL5 Aura's Vosk engine transcribes the local audio clip.
5. Word Error Rate (WER) between the Vosk output and the YouTube transcript is asserted
   to stay below a configurable threshold.

HOW TO ADD NEW TESTS
--------------------
Just append a new entry to YOUTUBE_TEST_CASES at the bottom of this file:

    YoutubeAudioTestCase(
        test_id   = "my_new_test",
        video_id  = "xxxxxxxxxxx",   # YouTube video ID (the part after ?v=)
        start_sec = 30,
        end_sec   = 45,
        language  = "en",            # or "de", "fr", …
        wer_threshold = 0.25,        # allow up to 25 % word errors
        notes     = "optional human-readable description",
    )

DEPENDENCIES (add to requirements-dev.txt)
------------------------------------------
    yt-dlp
    youtube-transcript-api
    vosk
    jiwer           # Word Error Rate calculation
    pytest
    ffmpeg          # system package, not pip

RUNNING
-------
    pytest scripts/py/func/checks/test_youtube_audio_regression.py -v
    pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -k "my_new_test"
"""

from __future__ import annotations

import json
import os
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pytest
import re

from config.settings import LANGUAGETOOL_CHECK_URL


def maybe_clear_cache():
    if not FRESH_RUN:
        return
    for f in FIXTURE_DIR.glob("*.wav"):
        f.unlink()
    for f in FIXTURE_DIR.glob("*.transcript.json"):
        f.unlink()
    print("FRESH_RUN: cache cleared")




active_lt_url =LANGUAGETOOL_CHECK_URL = f"{LANGUAGETOOL_CHECK_URL}"

# ---------------------------------------------------------------------------
# Optional-import helpers – give clear error messages when deps are missing
# ---------------------------------------------------------------------------

def _require(module_name: str, pip_name: Optional[str] = None):
    """Import a module and raise a readable error if it is missing."""
    import importlib
    try:
        return importlib.import_module(module_name)
    except ImportError:
        pkg = pip_name or module_name
        pytest.skip(
            f"Missing dependency '{pkg}'. Install it with:  pip install {pkg}"
        )


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[4]   # …/SL5-aura-service/
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "youtube_clips"
FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

FRESH_RUN = os.environ.get("AURA_TEST_FRESH", "0") == "1"

maybe_clear_cache()


# Where Vosk models live in this repo
DEFAULT_MODEL_PATHS = {
    "en": REPO_ROOT / "models" / "vosk-model-en-us-0.22",
    "de": REPO_ROOT / "models" / "vosk-model-de-0.21",
}


# ---------------------------------------------------------------------------
# Data class for a single test case
# ---------------------------------------------------------------------------

@dataclass
class YoutubeAudioTestCase:


    test_id: str                  # unique slug used for cache file names
    video_id: str                 # YouTube video ID (no URL prefix needed)
    start_sec: float              # clip start in seconds
    end_sec: float                # clip end   in seconds
    language: str = "de-DE"       # BCP-47 language code for Vosk model + YT transcript
    transcript_language: str = ""  # für YouTube-Transcript, leer = language verwenden
    wer_threshold: float = 0.30   # acceptable Word Error Rate (0.0 – 1.0)
    notes: str = ""               # free-text description shown in test output


    # --- Aura pipeline mode ---
    test_aura_pipeline: bool = False
    # If set: assert Aura's final output equals this string exactly (after strip/lower).
    # If None: just assert WER of Aura output vs YT transcript, same as Vosk mode.
    expected_output: Optional[str] = None

    @property
    def duration(self) -> float:
        return self.end_sec - self.start_sec

    @property
    def audio_cache_path(self) -> Path:
        return FIXTURE_DIR / f"{self.test_id}.wav"

    @property
    def transcript_cache_path(self) -> Path:
        return FIXTURE_DIR / f"{self.test_id}.transcript.json"

    @property
    def youtube_url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"


# ---------------------------------------------------------------------------
# ① Download audio clip (cached)
# ---------------------------------------------------------------------------

def download_audio_clip(case: YoutubeAudioTestCase) -> Path:
    """
    Download the requested time segment from YouTube as a 16 kHz mono WAV.
    Uses yt-dlp + ffmpeg. Result is cached on disk.
    """
    out = case.audio_cache_path
    if out.exists():
        return out

    # yt-dlp downloads the best audio stream, then ffmpeg trims + converts.
    # Using --download-sections to grab only the needed segment (yt-dlp ≥ 2023.03).
    cmd = [
        "yt-dlp",
        "--quiet",
        "--no-playlist",
        "--download-sections", f"*{case.start_sec}-{case.end_sec}",
        "--force-keyframes-at-cuts",
        "-x",                       # extract audio only
        "--audio-format", "wav",
        "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
        "-o", str(out),
        case.youtube_url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not out.exists():
        # Fallback: download full video then trim with ffmpeg
        _download_and_trim(case, out)

    if not out.exists():
        pytest.fail(
            f"[{case.test_id}] Could not download audio from {case.youtube_url}.\n"
            f"yt-dlp stderr: {result.stderr[:500]}"
        )
    return out


def _download_and_trim(case: YoutubeAudioTestCase, out: Path):
    """Fallback: full download then ffmpeg trim."""
    raw = FIXTURE_DIR / f"{case.test_id}_raw"
    dl_cmd = [
        "yt-dlp", "--quiet", "--no-playlist",
        "-x", "--audio-format", "best",
        "-o", str(raw) + ".%(ext)s",
        case.youtube_url,
    ]
    subprocess.run(dl_cmd, check=True)
    raw_file = next(FIXTURE_DIR.glob(f"{case.test_id}_raw.*"), None)
    if raw_file is None:
        return
    trim_cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(raw_file),
        "-ss", str(case.start_sec),
        "-t",  str(case.duration),
        "-ar", "16000", "-ac", "1",
        str(out),
    ]
    subprocess.run(trim_cmd, check=True)
    raw_file.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# ② Fetch YouTube transcript (cached)
# ---------------------------------------------------------------------------

def fetch_youtube_transcript(case: YoutubeAudioTestCase) -> str:
    """
    Fetch the auto-generated YouTube transcript for the relevant time window.
    Returns plain text. Result is cached as JSON.
    """
    cache = case.transcript_cache_path
    if cache.exists():
        data = json.loads(cache.read_text(encoding="utf-8"))
        return data["text"]

    YouTubeTranscriptApi = _require(
        "youtube_transcript_api", "youtube-transcript-api"
    ).YouTubeTranscriptApi

    try:
        yt_lang = case.transcript_language or case.language.split("-")[0]
        api = YouTubeTranscriptApi()
        transcript_list = list(api.fetch(
            case.video_id,
            languages=[yt_lang, "en"],
        ))
    except Exception as exc:
        pytest.skip(f"[{case.test_id}] Could not fetch YouTube transcript: {exc}")

    # Filter to the requested time window and join
    words = []
    for entry in transcript_list:
        entry_start = entry.start
        entry_end = entry_start + getattr(entry, "duration", 0)
        if entry_end >= case.start_sec and entry_start <= case.end_sec:
            words.append(entry.text.strip())



    text = " ".join(words)
    cache.write_text(
        json.dumps({"text": text, "video_id": case.video_id,
                    "start_sec": case.start_sec, "end_sec": case.end_sec},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # remove >> speaker markers and their associated text
    text = re.sub(r'>>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# ---------------------------------------------------------------------------
# ③ Transcribe with Vosk (SL5 Aura's engine)
# ---------------------------------------------------------------------------

def transcribe_with_vosk(audio_path: Path, language: str) -> str:
    """
    Run the audio WAV file through Vosk and return the full transcript string.
    Uses the same model paths as the rest of the SL5-aura-service project.
    """
    vosk = _require("vosk")
    vosk.SetLogLevel(-1)   # suppress Vosk's verbose output in test runs

    model_path = DEFAULT_MODEL_PATHS.get(language) or DEFAULT_MODEL_PATHS.get(language.split("-")[0])

    if model_path is None or not model_path.exists():
        # Try to find any model directory matching the language
        candidates = list((REPO_ROOT / "models").glob(f"vosk-model-{language}*"))
        if candidates:
            model_path = candidates[0]
        else:
            pytest.skip(
                f"Vosk model for language '{language}' not found. "
                f"Expected at: {model_path or REPO_ROOT / 'models' / f'vosk-model-{language}-*'}\n"
                f"Download it from https://alphacephei.com/vosk/models"
            )

    model = vosk.Model(str(model_path))

    with wave.open(str(audio_path), "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            pytest.fail(
                f"WAV file {audio_path} must be 16-bit mono. "
                f"Got channels={wf.getnchannels()}, sampwidth={wf.getsampwidth()}"
            )
        sample_rate = wf.getframerate()
        recognizer = vosk.KaldiRecognizer(model, sample_rate)
        recognizer.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if not data:
                break
            if recognizer.AcceptWaveform(data):
                part = json.loads(recognizer.Result())
                results.append(part.get("text", ""))
        # Final partial
        final = json.loads(recognizer.FinalResult())
        results.append(final.get("text", ""))

    return " ".join(r for r in results if r).strip()




def run_through_aura_pipeline(vosk_text: str, language: str) -> str:
    """
    Pass the Vosk transcript through Aura's full post-processing pipeline,
    the same way self_tester.py does it.

    Writes to a temp dir, then reads back tts_output_*.txt.
    Requires LanguageTool to be running (same as normal Aura usage).
    Set active_lt_url = None to skip LanguageTool (faster, less complete).
    """
    import logging
    import tempfile
    import time

    # print(f'LANGUAGETOOL_CHECK_URL:{LANGUAGETOOL_CHECK_URL}')

    # --- import Aura internals ---
    # in run_through_aura_pipeline(), before calling process_text_in_background:


    try:
        from scripts.py.func.process_text_in_background import process_text_in_background
    except ImportError:
        pytest.skip(
            "Could not import process_text_in_background. "
            "Run pytest from the repo root with the venv active."
        )

    # --- null logger (same pattern as self_tester.py) ---
    null_logger = logging.getLogger("aura_test_null")
    null_logger.addHandler(logging.NullHandler())

    # --- LanguageTool URL ---
    # None = LT disabled (Aura handles this gracefully, just skips LT step).
    # Override by setting env var AURA_LT_URL, e.g. "http://localhost:8010/v2"

    # --- temp output dir (one per call, no cross-test pollution) ---
    with tempfile.TemporaryDirectory(prefix="sl5_aura_pytest_") as tmp:
        worker_dir = Path(tmp)
        recording_time = time.time()

        # print(f'LANGUAGETOOL_CHECK_URL:{LANGUAGETOOL_CHECK_URL}')
        # print(f'DEBUG LT URL: {LANGUAGETOOL_CHECK_URL}')

        process_text_in_background(
            null_logger,
            language,           # LT_LANGUAGE  e.g. "en" or "de"
            vosk_text,          # raw_text
            None,               # output_dir  (ignored when override is set)
            recording_time,
            LANGUAGETOOL_CHECK_URL,
            output_dir_override=worker_dir,
        )

        # print(f"DEBUG output files: {list(worker_dir.glob('tts_output_*.txt'))}")


        # Read back the result — glob because timestamp is in the filename
        matches = sorted(worker_dir.glob("tts_output_*.txt"))
        # print(f"DEBUG file content: {matches[-1].read_text(encoding='utf-8-sig')[:100]}")

        if not matches:
            pytest.fail(
                f"Aura pipeline produced no tts_output_*.txt in {worker_dir}.\n"
                f"Input was: {vosk_text!r}"
            )

        return matches[-1].read_text(encoding="utf-8-sig").strip()


# ---------------------------------------------------------------------------
# ④ Word Error Rate helper
# ---------------------------------------------------------------------------

def compute_wer(reference: str, hypothesis: str) -> float:
    # print(f'LANGUAGETOOL_CHECK_URL:{LANGUAGETOOL_CHECK_URL}')

    """
    Compute Word Error Rate using jiwer.
    Falls back to a simple token-based WER if jiwer is not installed.
    """
    try:
        import jiwer
        return jiwer.wer(reference, hypothesis)
    except ImportError:
        # Minimal WER without jiwer
        ref_words = reference.lower().split()
        hyp_words = hypothesis.lower().split()
        if not ref_words:
            return 0.0 if not hyp_words else 1.0
        # Levenshtein distance on word lists
        d = _levenshtein(ref_words, hyp_words)
        return d / len(ref_words)


def _levenshtein(a: list, b: list) -> int:
    """Simple Levenshtein distance for lists."""
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            prev, dp[j] = dp[j], prev if a[i-1] == b[j-1] else 1 + min(prev, dp[j], dp[j-1])
    return dp[n]


# ---------------------------------------------------------------------------
# ⑤ The reusable test body
# ---------------------------------------------------------------------------

def run_audio_regression_test(case: YoutubeAudioTestCase):
    # print(f'LANGUAGETOOL_CHECK_URL:{LANGUAGETOOL_CHECK_URL}')

    """
    Core test logic. Call this from individual test functions.
    Designed to be reused for every YoutubeAudioTestCase.
    """
    print(f"\n{'='*60}")
    print(f"Test   : {case.test_id}")
    if case.notes:
        print(f"Notes  : {case.notes}")
    print(f"Video  : {case.youtube_url}  [{case.start_sec}s – {case.end_sec}s]")

    # Step 1 – audio
    audio_path = download_audio_clip(case)
    print(f"Audio  : {audio_path}")

    # Step 2 – reference transcript from YouTube
    yt_transcript = fetch_youtube_transcript(case)
    print(f"YT ref : {yt_transcript[:120]}{'…' if len(yt_transcript) > 120 else ''}")

    # Step 3 – Vosk transcription
    vosk_text = transcribe_with_vosk(audio_path, case.language)
    print(f"Vosk   : {vosk_text[:120]}{'…' if len(vosk_text) > 120 else ''}")

    # Step 4 – optionally run full Aura pipeline
    if case.test_aura_pipeline:
        aura_text = run_through_aura_pipeline(vosk_text, case.language)
        print(f"Aura   : {aura_text[:120]}{'…' if len(aura_text) > 120 else ''}")
    else:
        aura_text = None

    final_text = aura_text if aura_text is not None else vosk_text

    # Step 5 – evaluate
    if case.test_aura_pipeline and case.expected_output is not None:
        # Exact match mode: you know exactly what Aura should produce
        expected = case.expected_output.strip().lower()
        actual = final_text.lower()
        print(f"Expect : {expected}")
        print(f"Got    : {actual}")
        print('=' * 60)
        assert actual == expected, (
            f"[{case.test_id}] Aura output mismatch.\n"
            f"  Expected : {expected}\n"
            f"  Got      : {actual}\n"
            f"  Vosk raw : {vosk_text}"
        )
    else:
        # WER mode: compare against YouTube transcript
        wer = compute_wer(reference=yt_transcript, hypothesis=final_text)
        mode = "Aura" if case.test_aura_pipeline else "Vosk"
        print(f"WER ({mode}): {wer:.1%}  (threshold: {case.wer_threshold:.0%})")
        print('=' * 60)
        assert final_text, (
            f"[{case.test_id}] {'Aura' if case.test_aura_pipeline else 'Vosk'} "
            f"returned empty transcription."
        )
        assert wer <= case.wer_threshold, (
            f"[{case.test_id}] WER {wer:.1%} exceeds threshold {case.wer_threshold:.0%}.\n"
            f"  Reference : {yt_transcript}\n"
            f"  Output    : {final_text}"
        )





    assert vosk_text, (
        f"[{case.test_id}] Vosk returned empty transcription for {audio_path}"
    )
    assert wer <= case.wer_threshold, (
        f"[{case.test_id}] WER {wer:.1%} exceeds threshold {case.wer_threshold:.0%}.\n"
        f"  Reference : {yt_transcript}\n"
        f"  Vosk      : {vosk_text}"
    )


# ===========================================================================
#  TEST CASES – add your YouTube clips here
# ===========================================================================

YOUTUBE_TEST_CASES: list[YoutubeAudioTestCase] = [

    # ------------------------------------------------------------------
    # TEMPLATE – copy & rename this block to add a new test
    # ------------------------------------------------------------------
    # YoutubeAudioTestCase(
    #     test_id       = "my_video_intro",
    #     video_id      = "XXXXXXXXXXX",    # e.g. "d98ml86u68g"
    #     start_sec     = 10,
    #     end_sec       = 25,
    #     language      = "en",
    #     wer_threshold = 0.25,
    #     notes         = "First 15s of my tutorial video",
    # ),

    # ------------------------------------------------------------------
    # Example: SL5 Aura demo video (from the README)
    # Replace start_sec/end_sec with the segment you want to test.
    # ------------------------------------------------------------------
    # Mode A – Vosk only (existing behaviour, unchanged)
    # YoutubeAudioTestCase(
    #     test_id="sl5_aura_demo_en_v1",
    #     video_id="BZCHonTqwUw",
    #     start_sec=5,
    #     end_sec=20,
    #     language="en",
    #     wer_threshold=0.30,
    # ),

    # Mode B – full Aura pipeline, WER vs YouTube transcript
    # Use this to catch FuzzyMap/LanguageTool regressions
    # YoutubeAudioTestCase(
    #     test_id="sl5_aura_demo_en_v1_aura",
    #     video_id="BZCHonTqwUw",
    #     start_sec=5,
    #     end_sec=20,
    #     language="en",
    #     wer_threshold=0.55,  # tighter — Aura should improve on raw Vosk
    #     test_aura_pipeline=True,
    # ),

    # Mode B2 – full Aura pipeline, WER vs YouTube transcript
    # Use this to catch FuzzyMap/LanguageTool regressions
    # german
    YoutubeAudioTestCase(
        test_id="sl5_aura_demo_en_v1_aura",
        video_id="sOjRNICiZ7Q",
        start_sec=60,
        end_sec=70, # 120
        language = "de-DE",
        wer_threshold=0.55,  # tighter — Aura should improve on raw Vosk
        test_aura_pipeline=True,
        notes="Deutsches SL5 Aura Demo-Video",
    ),

    # Mode C – full Aura pipeline, exact expected output
    # Use this once you know a specific segment should produce a known command/text
    # YoutubeAudioTestCase(
    #     test_id="command_open_terminal",
    #     video_id="XXXXXXXXXXX",
    #     start_sec=42,
    #     end_sec=45,
    #     language="en",
    #     test_aura_pipeline=True,
    #     expected_output="open terminal",  # Aura must produce exactly this
    # ),

]


# ===========================================================================
#  PYTEST PARAMETRIZE – one test per case, named by test_id
# ===========================================================================

@pytest.mark.parametrize(
    "case",
    YOUTUBE_TEST_CASES,
    ids=[c.test_id for c in YOUTUBE_TEST_CASES],
)
def test_vosk_wer_against_youtube_transcript(case: YoutubeAudioTestCase):
    # print(f'LANGUAGETOOL_CHECK_URL:{LANGUAGETOOL_CHECK_URL}')

    """
    For each YoutubeAudioTestCase: download audio, fetch YT transcript,
    run Vosk, assert Word Error Rate stays below threshold.
    """
    run_audio_regression_test(case)
