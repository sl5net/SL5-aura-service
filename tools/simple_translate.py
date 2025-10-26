# Speichern unter dem neuen Namen, z.B. in Ihrem 'tools'-Verzeichnis
# als: .../tools/simple_translate.py

import subprocess
import sys

TRANSLATION_COMMAND = "trans"

def translate_text(text: str, target_lang: str) -> (str | None, str | None):
    """
    Übersetzt Text mit 'translate-shell' (trans).
    Gibt ein Tupel zurück: (ergebnis, fehler).
    Im Erfolgsfall ist fehler=None, im Fehlerfall ist ergebnis=None.
    """
    if not text.strip():
        return "", None # Leerer Input, kein Fehler

    # '-b' für "brief mode" (nur die Übersetzung)
    # '--no-ansi' entfernt Farbcodes
    cmd_args = [TRANSLATION_COMMAND, "-b", "--no-ansi", "-t", target_lang, text]

    try:
        result = subprocess.run(
            cmd_args,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        # Erfolgreiche Übersetzung zurückgeben
        return result.stdout.strip(), None

    except subprocess.CalledProcessError as e:
        # Fehler von 'trans' selbst (z.B. ungültige Sprache)
        error_message = f"Fehler von 'trans': {e.stderr.strip()}"
        return None, error_message
    except FileNotFoundError:
        # 'trans' ist nicht installiert oder nicht im PATH
        error_message = f"Fehler: '{TRANSLATION_COMMAND}' nicht gefunden. Ist translate-shell installiert?"
        return None, error_message

def main():
    """
    Hauptfunktion: Nimmt Argumente von der Kommandozeile,
    führt die Übersetzung durch und gibt das Ergebnis aus.
    """
    # Erwartet 3 Argumente: skript.py "text zum übersetzen" ziel-sprache
    if len(sys.argv) != 3:
        # Fehlermeldung auf stderr ausgeben, damit sie nicht als Ergebnis interpretiert wird
        print(f"Usage: python {sys.argv[0]} \"<text_to_translate>\" <target_language>", file=sys.stderr)
        sys.exit(1)

    text_to_translate = sys.argv[1]
    target_language = sys.argv[2]

    # Übersetzung durchführen
    translated_text, error = translate_text(text_to_translate, target_language)

    if error:
        # Fehlerfall: Fehlermeldung auf stderr und mit Fehlercode beenden
        print(error, file=sys.stderr)
        sys.exit(1)
    else:
        # Erfolgsfall: Ergebnis auf stdout ausgeben
        print(translated_text)
        return translated_text
        sys.exit(0)

if __name__ == "__main__":
    main()
























