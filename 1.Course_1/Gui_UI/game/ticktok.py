from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint

# UI
root = Tk()
root.title("Player 1")
style = ttk.Style()
style.theme_use("classic")
root.resizable(False,False)

# Global variable
ActivePlayer = 1
p1 = [] # What player 1 selected
p2 = [] # What player 2 selected

# Add button
# row 1
BT_1 = ttk.Button(root, text=' ')
BT_1.grid(row=0, column=0, sticky='snew', ipadx=20, ipady=20)
BT_1.config(command=lambda :ButtonClick(1))

BT_2 = ttk.Button(root, text=' ')
BT_2.grid(row=0, column=1, sticky='snew', ipadx=20, ipady=20)
BT_2.config(command=lambda :ButtonClick(2))

BT_3 = ttk.Button(root, text=' ')
BT_3.grid(row=0, column=2, sticky='snew', ipadx=20, ipady=20)
BT_3.config(command=lambda :ButtonClick(3))

# row 2
BT_4 = ttk.Button(root, text=' ')
BT_4.grid(row=1, column=0, sticky='snew', ipadx=20, ipady=20)
BT_4.config(command=lambda :ButtonClick(4))

BT_5 = ttk.Button(root, text=' ')
BT_5.grid(row=1, column=1, sticky='snew', ipadx=20, ipady=20)
BT_5.config(command=lambda :ButtonClick(5))

BT_6 = ttk.Button(root, text=' ')
BT_6.grid(row=1, column=2, sticky='snew', ipadx=20, ipady=20)
BT_6.config(command=lambda :ButtonClick(6))

# row 4
BT_7 = ttk.Button(root, text=' ')
BT_7.grid(row=2, column=0, sticky='snew', ipadx=20, ipady=20)
BT_7.config(command=lambda :ButtonClick(7))

BT_8 = ttk.Button(root, text=' ')
BT_8.grid(row=2, column=1, sticky='snew', ipadx=20, ipady=20)
BT_8.config(command=lambda :ButtonClick(8))

BT_9 = ttk.Button(root, text=' ')
BT_9.grid(row=2, column=2, sticky='snew', ipadx=20, ipady=20)
BT_9.config(command=lambda :ButtonClick(9))

# Set player turn
def ButtonClick(id):
    #print("ID:{}".format(id))
    global ActivePlayer
    global p1
    global p2
    if ActivePlayer==1:
        SetLayout(id, "X")
        p1.append(id)
        root.title("Player 2")
        ActivePlayer=2
        print("P1:{}".format(p1))
        AutoPlay()
    elif ActivePlayer==2:
        SetLayout(id, "O")
        p2.append(id)
        root.title("Player 1")
        ActivePlayer=1
        print("P2:{}".format(p2))
    # Check winner
    CheckWinner()

def SetLayout(id, PlaySymbol):
    #pass
    if id==1:
        BT_1.config(text=PlaySymbol)
        BT_1.state(['disabled'])
    elif id==2:
        BT_2.config(text=PlaySymbol)
        BT_2.state(['disabled'])
    elif id==3:
        BT_3.config(text=PlaySymbol)
        BT_3.state(['disabled'])
    elif id==4:
        BT_4.config(text=PlaySymbol)
        BT_4.state(['disabled'])
    elif id==5:
        BT_5.config(text=PlaySymbol)
        BT_5.state(['disabled'])
    elif id==6:
        BT_6.config(text=PlaySymbol)
        BT_6.state(['disabled'])
    elif id == 7:
        BT_7.config(text=PlaySymbol)
        BT_7.state(['disabled'])
    elif id==8:
        BT_8.config(text=PlaySymbol)
        BT_8.state(['disabled'])
    elif id==9:
        BT_9.config(text=PlaySymbol)
        BT_9.state(['disabled'])

def CheckWinner():
    Winner = -1
    global p1, p2
    if (1 in p1) and (2 in p1) and (3 in p1):
        Winner = 1
    if (1 in p2) and (2 in p2) and (3 in p2):
        Winner = 2

    if (4 in p1) and (5 in p1) and (6 in p1):
        Winner = 1
    if (4 in p2) and (5 in p2) and (6 in p2):
        Winner = 2

    if (7 in p1) and (8 in p1) and (9 in p1):
        Winner = 1
    if (7 in p2) and (8 in p2) and (9 in p2):
        Winner = 2

    if (1 in p1) and (4 in p1) and (7 in p1):
        Winner = 1
    if (1 in p2) and (4 in p2) and (7 in p2):
        Winner = 2

    if (1 in p1) and (5 in p1) and (9 in p1):
        Winner = 1
    if (1 in p2) and (5 in p2) and (9 in p2):
        Winner = 2

    if (2 in p1) and (5 in p1) and (8 in p1):
        Winner = 1
    if (2 in p2) and (5 in p2) and (8 in p2):
        Winner = 2

    if (3 in p1) and (6 in p1) and (9 in p1):
        Winner = 1
    if (3 in p2) and (6 in p2) and (9 in p2):
        Winner = 2

    if (3 in p1) and (5 in p1) and (7 in p1):
        Winner = 1
    if (3 in p2) and (5 in p2) and (7 in p2):
        Winner = 2

    # Winner message
    if Winner==1:
        messagebox.showinfo(title="Congrat.", message="Player 1 is winner")
        Reset()
    elif Winner==2:
        messagebox.showinfo(title="Congrat.", message="Player 2 is winner")
        Reset()

# Play with computer
def AutoPlay():
    global p1, p2
    EmptyCell = []
    for cell in range(9):
        if not ((cell + 1 in p1) or (cell + 1 in p2)):
            EmptyCell.append(cell+1)

    RandIndex = randint(0, len(EmptyCell)-1)
    ButtonClick(EmptyCell[RandIndex])

def Reset():
    global p1, p2
    BT_1.config(text=' ', state=NORMAL)
    BT_2.config(text=' ', state=NORMAL)
    BT_3.config(text=' ', state=NORMAL)
    BT_4.config(text=' ', state=NORMAL)
    BT_5.config(text=' ', state=NORMAL)
    BT_6.config(text=' ', state=NORMAL)
    BT_7.config(text=' ', state=NORMAL)
    BT_8.config(text=' ', state=NORMAL)
    BT_9.config(text=' ', state=NORMAL)
    p1 = []
    p2 = []

root.mainloop()
