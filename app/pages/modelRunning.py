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
import app.setup.glove
import app.pages.gloveSetting, app.pages.modelFinished
APP = App()


def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text="Running MotorEase...")
    glove_label.pack(pady=10)

    # GIF
    settings_gif = AnimatedGif(APP.root)
    settings_gif.pack(fill=BOTH, expand=YES)
    settings_gif.place(relx=0.5, rely=0.7, anchor="center")
    
def start():
    # Start download thread
    thread = threading.Thread(target=model_thread)
    thread.start()

def model_thread():  
    app.ModelRunner.run_MotorEase()
    app.pages.modelFinished.display()


