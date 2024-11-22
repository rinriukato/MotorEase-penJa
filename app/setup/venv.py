import os, subprocess, sys, platform

VENV_DIR = "./Code/.venv"
REQUIREMENTS_FILE = "./Code/requirements.txt"

def has_venv():
    return os.path.exists(VENV_DIR)

def create_virtualenv():
    if not os.path.exists(VENV_DIR):
       subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
       install_dependencies()

def install_dependencies():
    pip = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    subprocess.check_call([pip, "install", "-r", REQUIREMENTS_FILE])