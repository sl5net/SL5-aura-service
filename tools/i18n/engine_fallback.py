# tools/i18n/engine_fallback.py
import json
import logging
from pathlib import Path
import subprocess
import time

# Determine log path: two folders up, then "log/i18n_engine_fallback.log"
SCRIPT_PATH = Path(__file__).resolve()
LOG_PATH = SCRIPT_PATH.parents[2] / "log"
LOG_FILE = LOG_PATH / "i18n_engine_fallback.log"

# Ensure log dir exists
LOG_PATH.mkdir(parents=True, exist_ok=True)

# Configure module-level logger
logger = logging.getLogger("i18n_engine_fallback")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if module is reloaded
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

logger.info("Logger initialized. Log file: %s", LOG_FILE)

# DEFAULT_ENGINES = ["bing", "google", "yandex"]
DEFAULT_ENGINES = ["bing", "google"]
_engine_index = 0

def load_cooldowns(file_path: Path) -> dict:
    logger.info("Loading cooldowns from: %s", file_path)
    if file_path.exists():
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            now = time.time()
            active = {k: v for k, v in data.items() if v > now}
            logger.info(
                "Loaded %d cooldown entries (%d still active)", len(data), len(active)
            )
            return active
        except Exception as exc:
            logger.exception("Failed to load cooldowns from %s: %s", file_path, exc)
            return {}
    logger.info("Cooldown file does not exist yet (%s), starting fresh", file_path)
    return {}


def save_cooldowns(file_path: Path, cooldowns: dict) -> None:
    logger.info("Saving %d cooldown entries to: %s", len(cooldowns), file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_file = file_path.with_suffix(".tmp")
    temp_file.write_text(json.dumps(cooldowns, indent=2), encoding="utf-8")
    temp_file.replace(file_path)
    logger.info("Cooldowns saved successfully to %s", file_path)


def get_active_engines(cooldowns: dict, engines: list | None = None) -> list:
    global _engine_index
    selected_engines = engines or DEFAULT_ENGINES
    now = time.time()
    active = [e for e in selected_engines if cooldowns.get(e, 0) <= now]
    blocked = [e for e in selected_engines if e not in active]
    logger.info("Active engines: %s | blocked (cooldown): %s", active, blocked)
    if not active:
        logger.warning("No engines available, all currently on cooldown.")
        return []
    start = _engine_index % len(active)
    _engine_index += 1
    rotated = active[start:] + active[:start]
    logger.debug("Engine rotation order: %s (start index=%d)", rotated, start)
    return rotated


# tools/i18n/engine_fallback.py:34 3600=1h 300=5min 600=10min 1600=26min
def mark_engine_blocked(
    cooldowns: dict, engine: str, file_path: Path, duration_sec: int = 600
) -> None:
    cooldowns[engine] = time.time() + duration_sec
    save_cooldowns(file_path, cooldowns)
    logger.warning("Engine '%s' marked as blocked for %dm.", engine, duration_sec // 60)


def translate_with_engine_fallback(
    text: str,
    source_lang: str,
    target_lang: str,
    cooldowns: dict,
    cooldown_file: Path,
    timeout: int = 40,
    engines: list | None = None,
) -> list[str] | None:
    logger.info(
        "Starting translation request: %d chars, %s->%s",
        len(text), source_lang, target_lang,
    )
    available_engines = get_active_engines(cooldowns, engines)
    if not available_engines:
        logger.warning("No translation engines available (all currently on cooldown).")
        return None

    for engine in available_engines:
        logger.info("Trying engine '%s' for %s->%s", engine, source_lang, target_lang)
        try:
            process = subprocess.run(
                ["trans", "-e", engine, "-brief", f"{source_lang}:{target_lang}"],
                input=text,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                timeout=timeout,
            )
            lines = process.stdout.strip().split("\n")
            if any(line.startswith("https://translate.google.com") for line in lines):
                logger.warning("Engine '%s' returned a redirect URL instead of a translation.", engine)
                mark_engine_blocked(cooldowns, engine, cooldown_file)
                continue
            if len(lines) == 1 and "rate limiting" in lines[0].lower():
                logger.warning("Engine '%s' reported rate limiting.", engine)
                mark_engine_blocked(cooldowns, engine, cooldown_file)
                continue
            if not lines or (len(lines) == 1 and not lines[0].strip()):
                logger.warning("Engine '%s' returned empty output.", engine)
                mark_engine_blocked(cooldowns, engine, cooldown_file)
                continue
            logger.info("Engine '%s' succeeded (%d line(s) returned).", engine, len(lines))
            time.sleep(4)
            return lines
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ) as e:

            logger.warning("Engine '%s' failed: %s", engine, e)
            duration = (
                3600
                if isinstance(e, subprocess.CalledProcessError) and e.returncode == 1 and engine == "google"
                else 600
            )
            mark_engine_blocked(cooldowns, engine, cooldown_file, duration_sec=duration)
            continue



    logger.error("All engines exhausted, translation failed for %s->%s.", source_lang, target_lang)
    return None
