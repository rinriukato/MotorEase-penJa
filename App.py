import os
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import shutil
import json
from Setup import check_python_version, create_virtualenv, install_dependencies, download_glove_embeddings, run_script_in_venv  # Import functions

def run_setup():
    # Run the setup process with progress tracking
    progress_label["text"] = "Starting setup..."
    
    def update_progress(msg):
        progress_label["text"] = msg
        root.update_idletasks()  # Update GUI
    
    try:
        # Check python version
        if not check_python_version():
            progress_label["text"] = "Python version check failed. Please use Python 3.6 or higher."
            return
        
        # Run setup steps
        create_virtualenv(progress_callback=update_progress)
        install_dependencies(progress_callback=update_progress)
        download_glove_embeddings(progress_callback=update_progress)

        # Setup completed
        progress_label["text"] = "Setup completed successfully!"

        # Save setup completion status
        save_data["setupComplete"] = True
        with open("./save.json", "w") as file:
            json.dump(save_data, file)

    except Exception as e:
        progress_label["text"] = f"Setup failed: {str(e)}"


def run_model():
    # Disable the buttons while the model is running
    browse_button["state"] = "disabled"
    run_button["state"] = "disabled"

    # Run the model script
    progress_label["text"] = "Running model...\nThis will take some time."
    root.update_idletasks()
    
    try:
        run_script_in_venv("./Code/MotorEase.py")
        progress_label["text"] = "Model finished successfully!\nCheck results in ./predictions2.txt"

    except Exception as e:
        progress_label["text"] = f"Model failed with error: {str(e)}"

    # Re-enable the buttons
    browse_button["state"] = "normal"
    run_button["state"] = "normal"
    root.update_idletasks()

# Browse image files
def browse_file():
    file_path = tk.filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    file_picker.delete(0, tk.END)
    file_picker.insert(0, file_path)
    copy_files()


# Copy selected files to ./Data
def copy_files():
    file_path = file_picker.get()
    if not file_path:
        return
    
    shutil.copy(file_path, "./Data")
    progress_label["text"] = f"File copied to ./Data: {file_path}"


# GUI Setup
root = tk.Tk()

# Get save data
with open("./save.json", "r") as file:
    save_data = json.load(file)


# If setup has not been completed, show the setup GUI
if not save_data["setupComplete"]:

    root.title("App Setup")

    progress_label = tk.Label(root, text="Click 'Run Setup' to begin.")
    progress_label.pack(pady=10)

    run_button = tk.Button(root, text="Run Setup", command=run_setup)
    run_button.pack(pady=10)

# Setup has been completed, show the main app GUI
else:

    root.title("Main App")

    # Set size of window
    root.geometry("600x300")
    root.resizable(False, False)

    progress_label = tk.Label(root, text="Upload your application images \n and click 'Run Model' to begin.")
    progress_label.pack(pady=10)

    # Show file picker
    file_picker = ttk.Entry(root, width=50)
    browse_button = tk.Button(root, text="Browse", command=browse_file)
    browse_button.pack(pady=10)

    # Show button
    run_button = tk.Button(root, text="Run Model", command=run_model)
    run_button.pack(pady=10)    


root.mainloop()