import os, platform, subprocess
from app.setup.venv import VENV_DIR

MODEL_FILE = "./Code/MotorEase.py"

def get_venv_python():
    # Get the path to venv
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")
    
def run_script_in_venv(script_name):
    # Get path to venv
    venv_python = get_venv_python()
    if not os.path.exists(venv_python):
        raise FileNotFoundError(f"Virtual environment Python not found: {venv_python}")
    
    # Run script in venv
    try:
        print(f"Running {script_name} using {venv_python}...")
        subprocess.check_call([venv_python, script_name])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e}")
        raise

def run_MotorEase():
    # Run the MotorEase model in venv
    run_script_in_venv(MODEL_FILE)