# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Import Modules
from app.pages.root import App
APP = App()

def display(output):
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text=output)
    glove_label.pack(pady=10)

    # Close button
    close_button = ttk.Button(APP.root, text="Close", bootstyle=PRIMARY, command=APP.root.quit)
    close_button.pack(pady=10)

    APP.update()