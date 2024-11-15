import os
import sys
import subprocess
import platform
import json


PYTHON_VERSION = "3.9"
VENV_DIR = "./Code/.venv"
REQUIREMENTS_FILE = "./Code/requirements.txt"
TARGET_SCRIPT = "./Code/MotorEase.py"
SAVE_PATH = "./save.json"

def check_python_version():
    # Ensure the correct Python version is being used
    if sys.version_info[:2] != tuple(map(int, PYTHON_VERSION.split("."))):
        sys.exit(f"Error: Python {PYTHON_VERSION} is required.")

def create_virtualenv():
    # Create a virtual environment
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    # Install dependencies from requirements.txt
    pip_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    print("Installing dependencies...")
    subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS_FILE])

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

def main():

    # Read save file
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, 'r') as file:
            save = json.load(file)
    
    # Create save file if it doesn't exist
    else:
        save = json.loads('{"venvCreated": false}')
        with open(SAVE_PATH, 'w') as file:
            json.dump(save, file)

    # Check if virtual environment has been created
    if (not save['venvCreated']) or (not os.path.exists(VENV_DIR)):
        print("Creating virtual environment...")

        # To prevent any issues if the program was stopped before finishing venv creation.
        if os.path.exists(VENV_DIR):
            subprocess.check_call(["rm", "-rf", VENV_DIR])

        check_python_version()
        create_virtualenv()
        install_dependencies()

        # Assume venv exists in the future
        save['venvCreated'] = True
        with open(SAVE_PATH, 'w') as file:
            json.dump(save, file)

    else:
        print("Virtual environment already exists.")

    # Check if ./Code/glove.42B.300d.txt exists
    if not os.path.exists("./Code/glove.42B.300d.txt"):
        # Download glove.42B.300d.txt
        print("Downloading GloVe embeddings...")
        subprocess.check_call(["wget", "http://nlp.stanford.edu/data/glove.42B.300d.zip", "-P", "./Code/"])
        subprocess.check_call(["unzip", "./Code/glove.42B.300d.zip", "-d", "./Code/"])
        subprocess.check_call(["rm", "./Code/glove.42B.300d.zip"])
    else:
        print("GloVe embeddings already exist.")

        
    run_script_in_venv(TARGET_SCRIPT)

if __name__ == "__main__":
    main()