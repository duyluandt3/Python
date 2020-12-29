from tkinter import *
from tkinter import ttk

def BuClick(ID):
    print("ID: {}".format(ID))


root = Tk()

ttk.Button(root, text ="Click me", command = lambda :BuClick(10)).pack()


root.mainloop()