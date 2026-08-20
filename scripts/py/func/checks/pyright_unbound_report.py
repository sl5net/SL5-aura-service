# scripts/py/func/checks/pyright_unbound_report.py
"""Parse pyright --outputjson stdin and report possibly-unbound variable errors."""
import json
import sys


def main() -> int:
    data = json.load(sys.stdin)
    errors = [
        d for d in data.get("generalDiagnostics", [])
        if d.get("rule") == "reportPossiblyUnboundVariable"
    ]
    for err in errors:
        file_path = err["file"]
        line = err["range"]["start"]["line"] + 1
        message = err["message"]
        print(f"{file_path}:{line} - {message}")
    print(len(errors))
    return 0


if __name__ == "__main__":
    sys.exit(main())
