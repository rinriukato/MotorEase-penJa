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
import app.pages.gloveSetting
APP = App()

def display():
    APP.clear()
    
    # Label
    glove_label = tk.Label(APP.root, name="label", text="MotorEase.py not found.\nMake sure this app is run\nfrom the root directory.")
    glove_label.pack(pady=10)