import tkinter as tk
import game
from components import FrameButton

class MainFrame(tk.Frame):
    def __init__(self, owner, container):
        super().__init__(container)
        self.configure(bg="#000000")
        self.owner = owner

        self.container = tk.Frame(self, bg="#101010")
        self.container.pack(expand=1, ipadx=20, ipady=20)

        self.title = tk.Label(self.container, fg="white", bg="#101010", text="TicTacToe", font=("Helvetica bold", 20))
        self.title.pack(side=tk.TOP, pady=20)

        self.bOnePlayer = FrameButton(self.container, "One Player", self.onePlayerCallBack)
        self.bOnePlayer.pack(side=tk.TOP, pady=(0, 10))
        # self.bOnePlayer = tk.Button(self.container, text="One Player", command=lambda:owner.changeFrame(game.MainFrame))
        
        self.bTwoPlayer = FrameButton(self.container, "Two Players", self.twoPlayerCallBack)
        # self.bTwoPlayer = tk.Button(self.container, text="Two Players")
        self.bTwoPlayer.pack(side=tk.TOP, pady=(0, 10))

    def onePlayerCallBack(self, event):
        print("Not implemented yet")

    def twoPlayerCallBack(self, event):
        self.owner.changeFrame(game.MainFrame)

