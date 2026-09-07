import io
import json
import logging
import os
import platform
import shutil
import socket
import subprocess
import tempfile
import threading
import wave
from pathlib import Path
from scripts.py.func.config.dynamic_settings import settings

_LOG_FILE = Path(__file__).resolve().parents[4] / "log" / "wyoming_speak.log"
_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

_file_logger = logging.getLogger("wyoming_speak")
if not _file_logger.handlers:
    _file_logger.setLevel(logging.DEBUG)
    _handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    _handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    _file_logger.addHandler(_handler)


def _is_server_reachable(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, socket.timeout):
        return False


def _synthesize_and_play(
    text: str, host: str, port: int, logger: logging.Logger = None
) -> None:
    try:
        _file_logger.info(f"Connecting to Wyoming server at {host}:{port}")
        with socket.create_connection((host, port), timeout=10.0) as sock:
            req = json.dumps({"type": "synthesize", "data": {"text": text}}) + "\n"
            sock.sendall(req.encode("utf-8"))

            rate = 22050
            width = 2
            channels = 1
            audio_buffer = bytearray()
            sock_file = sock.makefile("rb")

            while True:
                line = sock_file.readline()
                if not line:
                    break
                event = json.loads(line.decode("utf-8"))
                event_type = event.get("type")

                if event_type == "audio-start":
                    data = event.get("data", {})
                    rate = data.get("rate", rate)
                    width = data.get("width", width)
                    channels = data.get("channels", channels)
                elif event_type == "audio-chunk":
                    payload_len = event.get("payload_length", 0)
                    if payload_len > 0:
                        chunk = sock_file.read(payload_len)
                        audio_buffer.extend(chunk)
                elif event_type == "audio-stop":
                    break

        if not audio_buffer:
            _file_logger.warning("No audio data received from Wyoming server")
            return

        _file_logger.info(f"Received {len(audio_buffer)} bytes. Assembling WAV…")
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, "wb") as wav_file:
                wav_file.setnchannels(channels)
                wav_file.setsampwidth(width)
                wav_file.setframerate(rate)
                wav_file.writeframes(audio_buffer)
            wav_bytes = wav_io.getvalue()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(wav_bytes)
            tmp_path = tmp.name

        try:
            if platform.system() == "Darwin":
                cmd = ["afplay", tmp_path]
            else:
                player = "paplay" if shutil.which("paplay") else "aplay"
                cmd = [player, tmp_path]

            _file_logger.info(f"Playing audio via: {' '.join(cmd)}")
            subprocess.run(cmd, check=False)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        _file_logger.error(f"Wyoming synthesis error: {e}", exc_info=True)
        if logger:
            logger.error(f"Wyoming synthesis error: {e}")


def wyoming_speak(text: str, logger: logging.Logger = None) -> bool:
    if not text:
        return False
    host = getattr(settings, "WYOMING_PIPER_HOST", "127.0.0.1")
    port = int(getattr(settings, "WYOMING_PIPER_PORT", 10200))

    if not _is_server_reachable(host, port):
        _file_logger.debug(f"Wyoming server at {host}:{port} is unreachable")
        return False

    _file_logger.info(f"Wyoming server at {host}:{port} reachable. Starting synthesis…")
    thread = threading.Thread(
        target=_synthesize_and_play, args=(text, host, port, logger), daemon=True
    )
    thread.start()
    return True
