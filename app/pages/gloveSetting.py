# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Import Modules
from app.pages.root import App
import app.pages.gloveDownload, app.pages.home
import app.setup.glove
APP = App()


def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, text="Select a GloVe model:")
    glove_label.pack(pady=10)

    # Dropdown menu
    glove_models = app.setup.glove.get_possible_glove_models()
    glove_combobox = ttk.Combobox(APP.root, values=glove_models, state="readonly")
    glove_combobox.pack(pady=10)
    glove_combobox.bind("<<ComboboxSelected>>", check_glove)

    APP.update()


def check_glove(value):
    # Get value from combobox
    selected_model = value.widget.get()

    # Split input into tokens and vectors
    selected_model = {
        "tokens": selected_model.split(" ")[0], 
        "vectors": selected_model.split(" ")[2]
    }

    # Get all downloaded GloVe models
    downloaded_models = app.setup.glove.get_downloaded_glove_models()

    # Remove old button
    for widget in APP.root.winfo_children():
        if widget.winfo_name() == "selectBtn":
            widget.destroy()

    # Check if selected model is downloaded
    if selected_model in downloaded_models:

        # Button to set as preferred model
        set_button = ttk.Button(APP.root, name="selectBtn", text="Set as Preferred Model", bootstyle=PRIMARY, command=lambda: save_preference(selected_model))
        set_button.pack(pady=10)
        
    else:
        # Button to install model
        download_button = ttk.Button(APP.root, name="selectBtn", text="Install GloVe Model", bootstyle=PRIMARY, command=lambda: start_download(selected_model))
        download_button.pack(pady=10)
    
def start_download(model):
    app.pages.gloveDownload.display()
    app.pages.gloveDownload.start(model)

def save_preference(model):
    app.setup.glove.set_preferred_glove_model(model['tokens'], model['vectors'])
    app.pages.home.display()

