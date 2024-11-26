# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading

# Import Modules
from app.pages.root import App
from app.AnimatedGIF import AnimatedGif
import app.setup.glove
import app.pages.gloveSetting
APP = App()


def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text="Downloading GloVe Model...")
    glove_label.pack(pady=10)

    # GIF
    settings_gif = AnimatedGif(APP.root, resize=(100, 100))
    settings_gif.pack(fill=BOTH, expand=YES)
    settings_gif.place(relx=0.5, rely=0.6, anchor="center")
    
def start(model):
    # Start download thread
    thread = threading.Thread(target=download_thread, args=(model,))
    thread.start()

def download_thread(model):
    
    # Check if model's zip file exists
    if not app.setup.glove.check_zip_exists(model['tokens']):

        # Download GloVe model
        APP.root.nametowidget("label").config(text="Downloading GloVe Models:\n" + app.setup.glove.GLOVE_ZIPS[model['tokens']])
        app.setup.glove.download_glove_model(model['tokens'])

    # Extract GloVe model
    APP.root.nametowidget("label").config(text="Extracting GloVe Models...")
    app.setup.glove.extract_glove_model(model['tokens'])

    # Set as preferred model
    app.setup.glove.set_preferred_glove_model(model['tokens'], model['vectors'])

    # Return to GloVe setting page
    app.pages.gloveSetting.display()
