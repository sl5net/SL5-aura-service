# scripts/py/func/ensure_package.py
import sys
import subprocess
import importlib

def ensure_package(pkg_name):
    try:
        return importlib.import_module(pkg_name)
    except ModuleNotFoundError:
        print(f"[ensure_package] Package {pkg_name!r} not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
        return importlib.import_module(pkg_name)
