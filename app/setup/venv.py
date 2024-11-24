import os, subprocess, sys, platform
import app.pages.criticalError

VENV_DIR = "./Code/.venv"
REQUIREMENTS_FILE = "./Code/requirements.txt"

def has_venv():
    return os.path.exists(VENV_DIR)

def python3_9_installed():
    try:
        subprocess.check_call(["python3.9", "--version"])
        return True
    except FileNotFoundError:
        return False


def create_virtualenv():
    if has_venv():
        return True
    
    if not python3_9_installed():
        app.pages.criticalError.display("Python 3.9 not found.\nPlease install Python 3.9 and try again.")
        return False
    
    subprocess.check_call(["python3.9", "-m", "venv", VENV_DIR])
    return True

def install_dependencies():
    pip = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    subprocess.check_call([pip, "install", "-r", REQUIREMENTS_FILE])