import os
import sys
import subprocess
import platform
import json

PYTHON_VERSION = "3.9"
VENV_DIR = "./Code/.venv"
REQUIREMENTS_FILE = "./Code/requirements.txt"
GLOVE_FILE = "./Code/glove.42B.300d.txt"
TARGET_SCRIPT = "./Code/MotorEase.py"
SAVE_PATH = "./save.json"

def check_python_version():
    # Ensure the correct Python version is being used
    if sys.version_info[:2] != tuple(map(int, PYTHON_VERSION.split("."))):
        return False
    return True

def create_virtualenv(progress_callback=None):
    # Update progress
    if progress_callback:
            progress_callback("Creating virtual environment...")
    
    # Create the virtual environment
    if not os.path.exists(VENV_DIR):
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

def install_dependencies(progress_callback=None):
    # Update progress
    if progress_callback:
        progress_callback("Installing dependencies...\nThis may take some time.")
    
    # Get pip path
    pip_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    
    # Install dependencies
    subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS_FILE])
    if progress_callback:
        progress_callback("Dependencies installed.")

def download_glove_embeddings(progress_callback=None):
    # Update progress
    if progress_callback:
        progress_callback("Downloading GloVe embeddings...\nThis may take some time.")
    
    # Download the GloVe embeddings file
    if not os.path.exists(GLOVE_FILE):
        subprocess.check_call(["wget", "http://nlp.stanford.edu/data/glove.42B.300d.zip", "-P", "./Code/"])
        subprocess.check_call(["unzip", "./Code/glove.42B.300d.zip", "-d", "./Code/"])
        subprocess.check_call(["rm", "./Code/glove.42B.300d.zip"])

def get_venv_python():
    # Get the path to the virtual environment's Python executable
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def run_script_in_venv(script_name):
    # Run a Python script using the virtual environment's Python
    venv_python = get_venv_python()
    if not os.path.exists(venv_python):
        raise FileNotFoundError(f"Virtual environment Python not found: {venv_python}")
    
    try:
        print(f"Running {script_name} using {venv_python}...")
        subprocess.check_call([venv_python, script_name])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e}")
        raise