import os, shutil
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.Setup import runSetup
from app.ModelRunner import run_MotorEase
import app.SaveData as SaveData
from app.AnimatedGIF import AnimatedGif
import threading

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
    label = root.nametowidget("progress_label")
    label["text"] = text
    root.update_idletasks()
    return

def begin_setup():
    setup_thread = threading.Thread(target=begin_setup_thread)
    setup_thread.start()

def begin_setup_thread():
    display_setup()
    runSetup(progress_callback=update_label)
    display_main_app()

def skip_setup():
    save = SaveData.load_data()
    save["setupComplete"] = True
    SaveData.save_data(save)
    display_main_app()

def begin_model():
    model_thread = threading.Thread(target=begin_model_thread)
    model_thread.start()

def begin_model_thread():
    display_running_model()
    update_label("Running model...\nThis will take some time.")
    
    try:
        run_MotorEase()
        update_label("Model finished successfully!\nCheck results in ./predictions2.txt")

    except Exception as e:
        update_label("Model failed with error:\n" + str(e))
    display_finished_model()

# Browse image files
def browse_file():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Image files", "*.png")], multiple=True)
    
    # Split the file paths if multiple files are selected
    if isinstance(file_path, tuple):
        file_path = list(file_path)

    # Check if any files were selected
    if len(file_path) == 0:
        return
    
    # Add the file paths for each image's xml file (should have identical names)
    missing_xml = []
    for i in range(len(file_path)):
        PathXML = file_path[i].replace(".png", ".xml")
        if os.path.exists(PathXML):
            file_path.append(PathXML)
        else:
            missing_xml.append(file_path.pop(i))
    
    if len(missing_xml) > 0:
        update_label("Error: " + str(len(missing_xml)) + " image(s) are missing\ncorresponding XML files.")
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
    get_num_files()
    root.update_idletasks()

def get_num_files():
    data_folder = "./Data"
    if not os.path.exists(data_folder):
        return 0
    
    # Count the number of .png files in the Data folder
    num_files = 0
    for file in os.listdir(data_folder):
        if file.endswith(".png"):
            num_files += 1
    
    num_files_label = root.nametowidget("num_selected_label")
    num_files_label["text"] = str(num_files)
    return num_files

def check_filepath():
    if not os.path.exists("./Code/MotorEase.py"):
        display_filepath_warning()
        return False
    return True

def clear_root():
    for widget in root.winfo_children():
        widget.destroy()

def display_filepath_warning():
    clear_root()
    progress_label = tk.Label(root, text="Could not find MotorEase.py.\nPlease ensure the file is run from\nthe root directory of the project.", name="progress_label")
    progress_label.place(relx=0.5, rely=0.5, anchor="center")

def display_intro():
    clear_root()
    
    # Show the setup GUI
    progress_label = tk.Label(root, text="Click the button to begin setup.\nRequires about 12GB of storage.")
    progress_label.pack(pady=10)

    setup_button = ttk.Button(root, text="Begin Setup", bootstyle=PRIMARY, command=begin_setup, width=20)
    setup_button.pack(pady=10)

    skip_button = ttk.Button(root, text="Skip Setup", bootstyle=SECONDARY , command=skip_setup, width=20)
    skip_button.pack(pady=10)

def display_setup():
    clear_root()
    
    # Show the setup GUI
    progress_label = tk.Label(root, text="Beginning Setup...", name="progress_label")
    progress_label.pack(pady=10)

    # Show Settings GIF
    settings_gif = AnimatedGif(root)
    settings_gif.pack(fill=BOTH, expand=YES)

    # Center the GIF
    settings_gif.place(relx=0.5, rely=0.7, anchor="center")

def display_main_app():
    clear_root()
    
    # Show the main app GUI
    progress_label = tk.Label(root, text="Select image files to begin.", name="progress_label")
    progress_label.place(relx=0.50, rely=0.15, anchor="center")
    
    # File picker
    file_picker = ttk.Entry(root, width=50)

    # Image Icon next to button
    image_icon = tk.PhotoImage(file="./app/img/image.png")
    image_icon_label = tk.Label(root, image=image_icon)
    image_icon_label.image = image_icon
    image_icon_label.place(relx=0.55, rely=0.40, anchor="center")

    # Number of selected files
    num_selected_label = tk.Label(root, text="0", name="num_selected_label")
    num_selected_label.place(relx=0.45, rely=0.39, anchor="center")

    # Browse Button
    browse_button = ttk.Button(root, text="Browse Files", command=browse_file, width=20)
    browse_button.place(relx=0.5, rely=0.60, anchor="center")

    # Run model button
    run_button = ttk.Button(root, text="Run Model", command=begin_model, width=20)
    run_button.place(relx=0.5, rely=0.84, anchor="center")

    get_num_files()

def display_running_model():
    clear_root()
    
    # Show the running model GUI
    progress_label = tk.Label(root, text="Running model...\nThis will take some time.", name="progress_label")
    progress_label.pack(pady=10)

    # Show Settings GIF
    settings_gif = AnimatedGif(root)
    settings_gif.pack(fill=BOTH, expand=YES)

    # Center the GIF
    settings_gif.place(relx=0.5, rely=0.7, anchor="center")

def display_finished_model():
    clear_root()
    
    # Show the finished model GUI
    progress_label = tk.Label(root, text="Model finished successfully!\nCheck results in ./predictions2.txt", name="progress_label")
    progress_label.pack(pady=10)

    # Close button
    close_button = ttk.Button(root, text="Done", command=display_main_app, width=20)
    close_button.pack(pady=10)

# GUI Setup
root = ttk.Window()

# Get save data
save_data = SaveData.load_data()

root.title("MotorEase Model")
root.geometry("600x300")
root.resizable(False, False)

if check_filepath():
    
    if not save_data["setupComplete"]:
        display_intro()
    else:
        print("Displaying main app")
        display_main_app()

root.mainloop()