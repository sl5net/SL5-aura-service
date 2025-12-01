# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# generate_docs.py for Sphinx

# Automatisch generierte Übersicht der Hilfsskripte.

import os

# Configuration: Directories to scan for scripts
DIRS_TO_SCAN = ['setup', 'config', 'githooks', 'update','scripts']
FILES_IN_ROOT = [
    'start_dictation_v2.0.bat', 'update.bat', 'install_hooks.sh',
    'type_watcher.ahk', 'type_watcher_keep_alive.sh'
]
OUTPUT_FILENAME = 'utility_scripts.rst'

# Language mapping for syntax highlighting in Sphinx
LANGUAGE_MAP = {
    '.sh': 'bash',
    'Dockerfile': 'docker',
    '.ahk': 'ahk',
    '.py': 'python',
    '.bat': 'batch',
}

def generate_rst_file():

    print(f"Generating {OUTPUT_FILENAME}...")
    with open(OUTPUT_FILENAME, 'w') as f:

        f.write("Utility-Skripte\n")
        f.write("===============\n\n")
        f.write("Automatisch generierte Übersicht der Hilfsskripte.\n\n")

        for directory in DIRS_TO_SCAN:
            if not os.path.isdir(directory):
                continue

            f.write(f"{directory.capitalize()}-Skripte\n")
            f.write("-" * (len(directory) + 8) + "\n\n")

            for filename in sorted(os.listdir(directory)):
                filepath = os.path.join(directory, filename)

                # Prüfe, ob es eine Datei ist (und kein Ordner)
                if os.path.isfile(filepath):
                    # Determine language for highlighting
                    name, ext = os.path.splitext(filename)
                    lang = LANGUAGE_MAP.get(ext, 'text')
                    if name == 'Dockerfile':
                        lang = 'docker'

                    f.write(f".. literalinclude:: {filepath}\n")
                    f.write(f"   :language: {lang}\n")
                    f.write(f"   :caption: {filepath}\n\n")

        # Add specific files from the root directory
        f.write("Root-Verzeichnis Skripte\n")
        f.write("------------------------\n\n")

        f.write("Folgende Skripte sind hier dokumentiert:\n\n")
        for filename in FILES_IN_ROOT:
            if os.path.exists(filename):
                f.write(f"* ``{filename}``\n")
        f.write("\n") # Wichtig: Leerzeile für korrekte Formatierung


        for filename in FILES_IN_ROOT:
            if os.path.exists(filename):
                # ... (rest of the code for language mapping etc. goes here)
                name, ext = os.path.splitext(filename)
                lang = LANGUAGE_MAP.get(ext, 'text')
                f.write(f".. literalinclude:: {filename}\n")
                f.write(f"   :language: {lang}\n")
                f.write(f"   :caption: {filename}\n\n")


    print(f"Successfully wrote {OUTPUT_FILENAME}")

if __name__ == "__main__":
    generate_rst_file()
