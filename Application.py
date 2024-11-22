# Import Libraries
import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

# Import Pages
from app.pages.root import App
import app.pages.gloveSetting
import app.pages.setup
import app.pages.filepathWarning


if not os.path.exists("./Code/MotorEase.py"):
    app.pages.filepathWarning.display()
else:
    app.pages.setup.display()

App().run()
