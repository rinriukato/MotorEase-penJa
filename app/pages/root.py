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
        size = self.size(320, 180)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.root.resizable(False, False)

    def run(self):
        self.root.mainloop()

    def clear(self):    
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def update(self):
        self.root.update()

    def size(self, w, h):
        return (self.width(w), self.height(h))

    def width(self, input):
        return int(self.root.winfo_screenheight() * input / 1080)
    
    def height(self, input):
        return int(self.root.winfo_screenheight() * input / 1080)
