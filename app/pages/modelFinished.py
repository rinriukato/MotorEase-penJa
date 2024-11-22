# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading

# Import Modules
from app.pages.root import App
from app.AnimatedGIF import AnimatedGif
import app.pages.home
APP = App()


def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text="Finished!")
    glove_label.pack(pady=10)

    # Home Button
    home_button = ttk.Button(APP.root, text="Home", command=app.pages.home.display, width=20)
    home_button.place(relx=0.5, rely=0.84, anchor="center")