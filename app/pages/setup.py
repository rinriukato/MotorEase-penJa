# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading

# Import Modules
from app.pages.root import App
import app.ModelRunner
from app.AnimatedGIF import AnimatedGif
import app.setup.venv, app.setup.glove
import app.pages.gloveSetting, app.pages.modelFinished, app.pages.home
APP = App()


def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text="Setting up...")
    glove_label.pack(pady=10)

    # GIF
    settings_gif = AnimatedGif(APP.root, resize=(100, 100))
    settings_gif.pack(fill=BOTH, expand=YES)
    settings_gif.place(relx=0.5, rely=0.6, anchor="center")

    start()

def start():
    # Start download thread
    thread = threading.Thread(target=setup_thread)
    thread.start()

def setup_thread():
    # Create venv and install dependencies
    if not app.setup.venv.has_venv():

        # Setup virtual environment
        APP.root.nametowidget("label").config(text="Creating virtual environment...")
        if not app.setup.venv.create_virtualenv():
            return

        # Install dependencies
        APP.root.nametowidget("label").config(text="Installing dependencies...")
        #app.setup.venv.install_dependencies()

    # Display next page
    preferred_glove = app.setup.glove.get_preferred_glove_model()
    preferred_glove_exists = app.setup.glove.glove_installed(preferred_glove['tokens'], preferred_glove['vectors'])
    
    if not preferred_glove_exists:
        app.pages.gloveSetting.display()
    else:
        app.pages.home.display()