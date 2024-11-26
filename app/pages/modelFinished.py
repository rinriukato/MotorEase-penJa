# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Import Modules
from app.pages.root import App
import app.pages.home
import app.ResultsPopup
APP = App()


def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text="Finished!")
    glove_label.pack(pady=10)

    # Results Popup Button
    results_button = ttk.Button(APP.root, text="View Results", command=app.ResultsPopup.popup_report, width=20)
    results_button.place(relx=0.5, rely=0.60, anchor="center")

    # Done Button
    home_button = ttk.Button(APP.root, text="Done", command=app.pages.home.display, width=20)
    home_button.place(relx=0.5, rely=0.84, anchor="center")