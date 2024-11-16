import os, sys, subprocess, platform
import time
from app.Config import PYTHON_VERSION, VENV_DIR, REQUIREMENTS_FILE, GLOVE_FILE
from app.SaveData import save_data, load_data

BREAK_TIME = 0.25

def check_python_version():
    majorVersionMatch = (sys.version_info.major == PYTHON_VERSION[0])
    minorVersionMatch = (sys.version_info.minor == PYTHON_VERSION[1])
    return majorVersionMatch and minorVersionMatch

def create_virtualenv(callback=None):
    # Update progress
    callback("Creating virtual environment...")
    time.sleep(BREAK_TIME)

    # Create the virtual environment
    if not os.path.exists(VENV_DIR):
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

def install_dependencies(callback=None):
    # Update progress
    callback("Installing dependencies...\nThis may take some time.")
    time.sleep(BREAK_TIME)

    # Get pip path
    pip_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    
    # Install dependencies
    subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS_FILE])

def download_glove_embeddings(callback=None):
    # Update progress
    callback("Downloading GloVe embeddings...\nThis may take some time.")
    time.sleep(BREAK_TIME)

    # Download the GloVe embeddings file
    if not os.path.exists(GLOVE_FILE):
        subprocess.check_call(["wget", "http://nlp.stanford.edu/data/glove.42B.300d.zip", "-P", "./Code/"])
        subprocess.check_call(["unzip", "./Code/glove.42B.300d.zip", "-d", "./Code/"])
        subprocess.check_call(["rm", "./Code/glove.42B.300d.zip"])

def runSetup(progress_callback):
    try:
        progress_callback("Starting setup...")
        time.sleep(BREAK_TIME)
        
        # Run setup steps
        create_virtualenv(progress_callback)
        install_dependencies(progress_callback)
        download_glove_embeddings(progress_callback)

        # Save setup completion status
        save = load_data()
        save["setupComplete"] = True
        save_data(save)

        # Setup completed
        progress_callback("Setup completed successfully!\nPlease restart the app.")

    except Exception as e:
        progress_callback(f"Setup failed: {str(e)}")