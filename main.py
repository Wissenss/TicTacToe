import tkinter as tk

import game
import menu

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #main window config
        self.geometry("500x500")
        self.configure(bg="#000000")
        self.resizable(False, False)
        self.iconbitmap("./assets/icon.ico")
        self.title("TicTacToe")

        self.container = tk.Frame(self, bg="#000000")
        self.container.pack(expand=True)

        frames = {
            game.MainFrame : None,
            menu.MainFrame : None
        }
        self.frames = frames

        for frame in frames:
            frames[frame] = frame(self, self.container)
            frames[frame].grid(column=0, row=0, sticky="nswe")

        self.changeFrame(menu.MainFrame)

    def changeFrame(self, frame):
        self.frames[frame].tkraise()

if __name__ == "__main__":
    App().mainloop()