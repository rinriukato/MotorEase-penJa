# Import Libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

import tkinter as tk

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

class App(Singleton):
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super().__init__()
        self._initialized = True

        self.root = tk.Tk()
        self.root.title("MotorEase")
        self.root.geometry("600x300")

    def run(self):
        self.root.mainloop()

    def clear(self):    
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def update(self):
        self.root.update()
