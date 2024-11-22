import sys

from app.setup.glove import *
from app.setup.venv import *
from app.setup.version import *

def runSetup(progress_callback):
    try:
        progress_callback("Starting setup...")
        
        # Check Python version
        progress_callback("Checking Python version...")
        if not check_python_version():
            raise ValueError(f"Invalid Python version: {sys.version_info.major}.{sys.version_info.minor}")
        
        # Create virtual environment
        progress_callback("Creating virtual environment...")
        #create_virtualenv()

        # Check for GloVe file
        progress_callback("Checking GloVe file...")
        #glove_file = check_glove_exists()

        # Check how much RAM is available
        progress_callback("Checking available RAM...")
        
        

        # Download GloVe file if not found
        #if glove_file is None:
            #progress_callback("Downloading GloVe file...")
            #download_glove()
        #else:
            #progress_callback("GloVe file found!")
        


        # Setup completed
        progress_callback("Setup complete!")

    except Exception as e:
        progress_callback(f"Setup failed: {str(e)}")