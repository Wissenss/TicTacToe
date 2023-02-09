import tkinter as tk
import game

class FrameButton(tk.Frame):
    def __init__(self, owner, text, action):
        super().__init__(owner)

        label = tk.Label(self, text=text)
        label.pack(expand=1)

        label.bind("<Button-1>", action)
        self.bind("<Button-1>", action)