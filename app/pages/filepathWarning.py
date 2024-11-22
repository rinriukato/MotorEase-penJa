# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

# Import Modules
from app.pages.root import App
APP = App()

def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text="MotorEase.py not found.\nMake sure this app is run\nfrom the root directory.")
    glove_label.pack(pady=10)