from tkinter import *
from tkinter import ttk

root = Tk()

# Key press event
def key_press(event):
    print("Copy")
    print("Type:{}".format(event.type))

# Button press event
def button_press(event):
    print("Button press")
    print("Type:{}".format(event.type))

# Call key_press event
root.bind("<Control-c>",key_press)

# Call button press event 
bu = ttk.Button(root, text = "Button")
bu.pack()
bu.bind("<ButtonPress>",button_press)


root.mainloop()