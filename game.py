import tkinter as tk
from components import FrameButton
import menu

class Cell(tk.Frame):
    Images = {
        "X" : "./assets/X.png", 
        "O" : "./assets/O.png",
        "E" : "./assets/E.png", 
    }

    def __init__(self, owner, bordercolor=None, borders=(1, 1, 1, 1), **kwargs):
        super().__init__(owner, background=bordercolor, bd=0, highlightthickness=0)

        self.owner = owner
        self.content = tk.Frame(self, background="black", **kwargs)
        self.content.pack(padx=(borders[0], borders[1]), pady=(borders[2], borders[3]), expand=1, fill="both")
        
        self.labelImage = tk.Label(self.content, bd=0)
        self.labelImage.pack(expand=True)

        self.enable = True
        self.value = "E"
        self.set_value(self.value)

        self.content.bind("<Button-1>", self.click)
        self.labelImage.bind("<Button-1>", self.click)

    def set_value(self, value):
        self.value = value
        self.image = tk.PhotoImage(file=Cell.Images[value])
        self.labelImage.configure(image=self.image)

    def get_value(self):
        return self.value

    def click(self, event):
        if self.enable:
            self.set_value(self.owner.turn)
            self.enable = False
            self.owner.nextTurn()

class Menu(tk.Canvas):
    def __init__(self, owner):
        super().__init__(owner, bg="#ffffff", width=444, height=444) #, bg=None, bd=0
        self.owner = owner
        self.container = tk.Frame(self, bg="#101010", bd=0, highlightbackground="white", highlightthickness=0)
        self.container.pack(expand=True, fill="both")
        # self.attributes('alpha', 0.5)
        self.background = tk.PhotoImage(file="./assets/Opacity.png")
        self.create_image(0,0, anchor="nw", image=self.background)

        self.lResult = tk.Label(self.container, text="", fg="white", bg="#101010", font=("Helvetica bold", 20))
        self.lResult.pack(expand=1, pady=(20, 0)) 
        
        self.controlers = tk.Frame(self.container)
        self.controlers.pack(side="bottom", pady=(0, 4))

        # self.bNewGame = tk.Button(self.container, text="New Game", relief="flat", bg="#101010", fg="white", command=self.NewGame)
        self.bNewGame = FrameButton(self.controlers, "New Game", self.NewGame)
        self.bNewGame.pack(side="left", padx=2) #anchor="se"
        
        self.bBackToMain = FrameButton(self.controlers, "Back To Main", self.BackToMain)
        self.bBackToMain.pack(side="right", padx=0)

    def Show(self, message):
        self.lResult.configure(text=message)
        self.tk.call("raise", self._w)

    def NewGame(self, event):
        self.owner.startGame()

    def BackToMain(self, event):
        self.owner.owner.owner.changeFrame(menu.MainFrame)


class Game(tk.Frame): 
    def __init__(self, owner):
        self.turn = "X"
        self.owner = owner
        self.matrix = [ [None, None, None],
                        [None, None, None],
                        [None, None, None]]

        super().__init__(owner)

        self.menu = Menu(self)
        self.menu.grid(column=0, row=0, columnspan=3, rowspan=3, sticky="nswe", padx=120, pady=180)
        self.createCells()

    def createCells(self):
        borders = (
            #(left, right, top, bottom)
            (0, 1, 0, 1),
            (1, 1, 0, 1),
            (1, 0, 0, 1),

            (0, 1, 1, 1),
            (1, 1, 1, 1),
            (1, 0, 1, 1),

            (0, 1, 1, 0),
            (1, 1, 1, 0),
            (1, 0, 1, 0),
        )

        for i in range(3):
            for j in range(3):
                self.matrix[i][j] = Cell(self, "white", borders[j*3+i])
                self.matrix[i][j].grid(column=i, row=j, ipadx=10, ipady=10)

    def nextTurn(self):
        self.turn = "X" if self.turn != "X" else "O"

        check = self.checkWin()
        if check != "Continue":
            self.endGame(check)

        self.owner.turnDisplay.configure(text=f"Turno de {self.turn}")

    def startGame(self):
        self.turn="X"
        for row in self.matrix:
            for cell in row:
                cell.set_value("E")
                cell.enable = True
                cell.tkraise()
        self.owner.turnDisplay.configure(text=f"Turno de {self.turn}")

    def endGame(self, result):
        if result != "Tie":
            result = f"{result} won!"       
        else:
            result = "It's a tie"

        for row in self.matrix:
            for cell in row:
                cell.enable = False

        self.owner.turnDisplay.configure(text="")
        self.menu.Show(result)
        self.menu.tkraise()

    def checkWin(self):
        #return values
        #"Continue"
        #"X"
        #"O"
        #"Tie"
        matrix = self.matrix

        mainDiagonal = 0
        altDiagonal = 0
        occupied = 0
        for i in range(3):
            if matrix[i][i].get_value() == "X":
                altDiagonal+=1
            elif matrix[i][i].get_value() == "O":
                altDiagonal-=1
            if matrix[2-i][i].get_value() == "X":
                mainDiagonal+=1
            elif matrix[2-i][i].get_value() == "O":
                mainDiagonal-=1
            
            horizontal = 0
            vertical = 0

            for j in range(3):
                if matrix[i][j].get_value() == "X":
                    horizontal += 1
                elif matrix[i][j].get_value() == "O":
                    horizontal -= 1
                if matrix[j][i].get_value() == "X":
                    vertical += 1
                elif matrix[j][i].get_value() == "O":
                    vertical -= 1
            
                if matrix[i][j].get_value() != "E":
                    occupied += 1

            winConditions = [horizontal, vertical]
            if -3 in winConditions:
                return "O"
            if 3 in winConditions:
                return "X"

        winConditions = [mainDiagonal, altDiagonal]
        if -3 in winConditions:
            return "O"
        if 3 in winConditions:
            return "X"
        if occupied == 9:
            return "Tie"

        return "Continue"

class MainFrame(tk.Frame):
    def __init__(self, owner, container):
        super().__init__(container)
        self.configure(bg="#000000")
        self.owner = owner

        self.game = Game(self)
        self.game.pack(expand=1, pady=(20, 0))

        self.turnDisplay = tk.Label(self, text="Turno de X", bd=0, fg="white", bg="#000000")
        self.turnDisplay.pack(anchor="se", pady=(0, 20), padx=20)


if __name__ == "__main__":
    pass