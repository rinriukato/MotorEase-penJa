# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Import Modules
from app.pages.root import App
ROOT = App()

def display():
    App.clear()
    
    # Label
    progress_label = tk.Label(ROOT, text="Click the button to begin setup.\nRequires about 12GB of storage.")
    progress_label.pack(pady=10)

    # Begin Setup Button
    setup_button = ttk.Button(ROOT, text="Begin Setup", bootstyle=PRIMARY, command=begin_setup, width=20)
    setup_button.pack(pady=10)

    # Skip Setup Button
    skip_button = ttk.Button(ROOT, text="Skip Setup", bootstyle=SECONDARY , command=skip_setup, width=20)
    skip_button.pack(pady=10)