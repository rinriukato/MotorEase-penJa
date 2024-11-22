# Script from https://ttkbootstrap.readthedocs.io/en/latest/cookbook/gif-animation/
# Animated GIF from https://icons8.com/preloaders/
from pathlib import Path
from itertools import cycle
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageSequence

class AnimatedGif(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=300)

        # open the GIF and create a cycle iterator
        file_path = "./app/img/Settings.gif"
        with Image.open(file_path) as im:
            # create a sequence
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # length of each frame
            self.framerate = im.info["duration"]

        self.img_container = ttk.Label(self, image=next(self.image_cycle))
        self.img_container.pack(fill="both", expand="yes")
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)