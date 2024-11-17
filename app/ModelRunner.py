import os, platform, subprocess
from app.Config import VENV_DIR, MODEL_FILE

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

def run_MotorEase():
    # Run the MotorEase model script on a separate thread
    run_script_in_venv(MODEL_FILE)