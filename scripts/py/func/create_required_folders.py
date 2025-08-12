# file: scripts/py/func/create_required_folders.py
import sys
from pathlib import Path

def setup_project_structure(project_root_str: str):
    """
    Creates all necessary directories and placeholder files within the project,
    using the provided project root path. This script is the single source of
    truth for the project's internal directory structure.
    """
    project_root = Path(project_root_str).resolve()
    print(f"--> Using project root for setup: {project_root}")

    # Define all required project-relative directories and their initial files
    project_dirs = {
        project_root / "log": ["__init__.py"],
        project_root / "config": ["__init__.py", "model_name_lastused.txt"],
        project_root / "config" / "maps": ["__init__.py"],
        project_root / "models": None,  # For Vosk models
    }

    # Define absolute paths required by the application (independent of project location)
    absolute_dirs = {
        Path("/tmp/sl5_dictation"): None,
    }

    # Combine both dictionaries
    all_dirs_to_create = {**project_dirs, **absolute_dirs}

    for dir_path, initial_files in all_dirs_to_create.items():
        try:
            # 1. Create the directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"    -> OK (DIR): {dir_path}")

            # 2. Create initial placeholder files if any are specified
            if initial_files:
                for filename in initial_files:
                    file_path = dir_path / filename
                    if not file_path.exists():
                        file_path.touch()
                        print(f"    -> OK (TOUCH): {file_path}")

                        # Special handling for dummy content
                        if filename == "model_name_lastused.txt":
                            file_path.write_text("dummy\n")
                            print(f"    -> OK (WRITE): Wrote 'dummy' to {file_path}")
        except Exception as e:
            print(f"    -> FATAL ERROR setting up {dir_path}: {e}")
            sys.exit(1) # Exit with an error code to fail the CI/CD job

if __name__ == "__main__":
    # This script expects the project root path as its first argument.
    # The setup.sh script will provide it.
    if len(sys.argv) < 2:
        print("FATAL ERROR: Project root path argument is missing.")
        sys.exit(1)

    # The first argument (sys.argv[0]) is the script name itself.
    # The project root is the second (sys.argv[1]).
    setup_project_structure(sys.argv[1])
