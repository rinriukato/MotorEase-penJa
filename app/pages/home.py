# Import Libraries
import os, shutil
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.filedialog

# Import Modules
from app.pages.root import App
import app.setup.glove
import app.pages.gloveDownload, app.pages.modelRunning
APP = App()

def display():
    APP.clear()

    # Label
    progress_label = tk.Label(APP.root, text="Select image files to begin.", name="progress_label")
    progress_label.place(relx=0.50, rely=0.15, anchor="center")
    
    # File picker
    file_picker = ttk.Entry(APP.root, name="file_picker", width=50)

    # Image Icon next to button
    image_icon = tk.PhotoImage(file="./app/img/image.png")
    image_icon_label = tk.Label(APP.root, image=image_icon)
    image_icon_label.image = image_icon
    image_icon_label.place(relx=0.55, rely=0.40, anchor="center")

    # Number of selected files
    num_selected_label = tk.Label(APP.root, text="0", name="num_selected_label")
    num_selected_label.place(relx=0.45, rely=0.39, anchor="center")
    get_num_files()

    # Browse Button
    browse_button = ttk.Button(APP.root, text="Browse Files", command=browse_file, width=20)
    browse_button.place(relx=0.5, rely=0.60, anchor="center")

    # Run Model button
    run_button = ttk.Button(APP.root, text="Run Model", command=begin_model, width=20)
    run_button.place(relx=0.5, rely=0.84, anchor="center")

def update_label(text):
    progress_label = APP.root.nametowidget("progress_label")
    progress_label["text"] = text
    APP.update()

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

    file_picker = APP.root.nametowidget("file_picker")
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
    APP.update()

def get_num_files():
    data_folder = "./Data"
    if not os.path.exists(data_folder):
        print("Data folder not found.")
        return 0
    
    # Count the number of .png files in the Data folder
    num_files = 0
    for file in os.listdir(data_folder):
        if file.endswith(".png"):
            num_files += 1
    
    num_files_label = APP.root.nametowidget("num_selected_label")
    num_files_label["text"] = str(num_files)
    return num_files

def begin_model():
    if get_num_files() == 0:
        update_label("Error: No image files selected.")
        return

    app.pages.modelRunning.display()
    app.pages.modelRunning.start()