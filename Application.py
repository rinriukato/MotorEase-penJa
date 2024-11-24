# Import Libraries
import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

# Import Pages
import app.pages.criticalError
from app.pages.root import App
import app.pages.gloveSetting
import app.pages.setup
import app.pages.criticalError


if not os.path.exists("./Code/MotorEase.py"):
    app.pages.criticalError.display("MotorEase.py not found.\nMake sure this app is run\nfrom the root directory.")
else:
    app.pages.setup.display()

App().run()