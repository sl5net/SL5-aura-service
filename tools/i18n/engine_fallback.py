
import json
from pathlib import Path
import subprocess
import time

DEFAULT_ENGINES = ["bing", "google", "yandex"]


def load_cooldowns(file_path: Path) -> dict:
    if file_path.exists():
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            now = time.time()
            return {k: v for k, v in data.items() if v > now}
        except Exception:
            return {}
    return {}


def save_cooldowns(file_path: Path, cooldowns: dict) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_file = file_path.with_suffix(".tmp")
    temp_file.write_text(json.dumps(cooldowns, indent=2), encoding="utf-8")
    temp_file.replace(file_path)


def get_active_engines(cooldowns: dict, engines: list | None = None) -> list:
    selected_engines = engines or DEFAULT_ENGINES
    now = time.time()
    return [e for e in selected_engines if cooldowns.get(e, 0) <= now]


def mark_engine_blocked(
    cooldowns: dict, engine: str, file_path: Path, duration_sec: int = 3600
) -> None:
    cooldowns[engine] = time.time() + duration_sec
    save_cooldowns(file_path, cooldowns)
    print(f"      [WARN] Engine '{engine}' marked as blocked for {duration_sec // 60}m.")


def translate_with_engine_fallback(
    text: str,
    source_lang: str,
    target_lang: str,
    cooldowns: dict,
    cooldown_file: Path,
    timeout: int = 40,
    engines: list | None = None,
) -> list[str] | None:
    available_engines = get_active_engines(cooldowns, engines)
    if not available_engines:
        print("      [WARN] No translation engines available (all currently on cooldown).")
        return None

    for engine in available_engines:
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
                mark_engine_blocked(cooldowns, engine, cooldown_file)
                continue
            if len(lines) == 1 and "rate limiting" in lines[0].lower():
                mark_engine_blocked(cooldowns, engine, cooldown_file)
                continue
            if not lines or (len(lines) == 1 and not lines[0].strip()):
                mark_engine_blocked(cooldowns, engine, cooldown_file)
                continue
            return lines
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ) as e:
            print(f"      [WARN] Engine '{engine}' failed: {e}")
            mark_engine_blocked(cooldowns, engine, cooldown_file)
            continue

    return None
