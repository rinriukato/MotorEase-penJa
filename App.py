import os, shutil, json
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from app.Setup import runSetup
from app.ModelRunner import run_MotorEase
import app.SaveData as SaveData

def find_component(component_type):
    for component in root.winfo_children():
        if isinstance(component, component_type):
            return component
    return None

def find_components(component_type):
    components = []
    for component in root.winfo_children():
        if isinstance(component, component_type):
            components.append(component)
    return components

def update_label(text):
    label = find_component(tk.Label)
    label["text"] = text
    root.update_idletasks()
    return

def disable_buttons():
    buttons = find_components(tk.Button)
    for button in buttons:
        button["state"] = "disabled"
    root.update_idletasks()

def enable_buttons():
    buttons = find_components(tk.Button)
    for button in buttons:
        button["state"] = "normal"
    root.update_idletasks()

def begin_setup():
    disable_buttons()
    runSetup(progress_callback=update_label)
    display_main_app()

def skip_setup():
    save = SaveData.load_data()
    save["setupComplete"] = True
    SaveData.save_data(save)
    display_main_app()

def begin_model():
    disable_buttons()
    update_label("Running model...\nThis will take some time.")
    
    try:
        run_MotorEase()
        update_label("Model finished successfully!\nCheck results in ./predictions2.txt")

    except Exception as e:
        update_label("Model failed with error:\n" + str(e))

    enable_buttons()

# Browse image files
def browse_file():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Image files", "*.png")], multiple=True)
    
    # Split the file paths if multiple files are selected
    if isinstance(file_path, tuple):
        file_path = list(file_path)
    
    # Add the file paths for each image's xml file (should have identical names)
    missing_xml = []
    for i in range(len(file_path)):
        PathXML = file_path[i].replace(".png", ".xml")
        if os.path.exists(PathXML):
            file_path.append(PathXML)
        else:
            missing_xml.append(file_path.pop(i))
    
    if len(missing_xml)> 0:
        update_label("Error: " + str(len(missing_xml)) + " image(s) are missing XML.\nPlease be sure each image\nhas a corresponding XML file.")
        return

    file_picker = find_component(ttk.Entry)
    file_picker.delete(0, tk.END)
    file_picker.insert(0, file_path)
    copy_files(file_path)


# Copy selected files to ./Data
def copy_files(file_paths):
    data_folders = ["./Data", "./Code/detectors/Visual/UIED-master/data/input/"]

    for data_folder in data_folders:
        if os.path.exists(data_folder):
            shutil.rmtree(data_folder)
        
        os.makedirs(data_folder)
        
        for file_path in file_paths:
            shutil.copy(file_path, data_folder)
    
    update_label("Files copied to ./Data")
    root.update_idletasks()

def check_filepath():
    if not os.path.exists("./Code/MotorEase.py"):
        display_filepath_warning()
        return False
    return True

def display_filepath_warning():
    progress_label = tk.Label(root, text="Could not find MotorEase.py.\nPlease ensure the file is run from\nthe root directory of the project.")
    progress_label.pack(pady=10)

def display_setup():
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Show the setup GUI
    progress_label = tk.Label(root, text="Click the button to begin setup.\nRequires about 12GB of storage.")
    progress_label.pack(pady=10)

    setup_button = tk.Button(root, text="Begin Setup", command=begin_setup)
    setup_button.pack(pady=10)

    skip_button = tk.Button(root, text="Skip Setup", command=skip_setup)
    skip_button.pack(pady=10)
    enable_buttons()

def display_main_app():
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Show the main app GUI
    progress_label = tk.Label(root, text="Select image files to begin.")
    progress_label.pack(pady=10)
    
    # File picker
    file_picker = ttk.Entry(root, width=50)

    browse_button = tk.Button(root, text="Browse Files", command=browse_file)
    browse_button.pack(pady=10)

    # Run model button
    run_button = tk.Button(root, text="Run Model", command=begin_model)
    run_button.pack(pady=10)

    enable_buttons()

# GUI Setup
root = tk.Tk()

# Get save data
save_data = SaveData.load_data()

root.title("MotorEase Model")
root.geometry("600x300")
root.resizable(False, False)

if check_filepath():
    
    if not save_data["setupComplete"]:
        display_setup()
    else:
        print("Displaying main app")
        display_main_app()

root.mainloop()