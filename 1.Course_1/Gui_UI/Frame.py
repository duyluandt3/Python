from tkinter import *
from tkinter import ttk

root = Tk()

frame = ttk.Frame(root)
frame.pack()

# Config frame size
frame.config(height=200, width=200)
# Set button in frame 1
ttk.Button(frame, text="Click me (#1)").grid(row=0, column=0)
ttk.Button(frame, text="Click me (#1)").grid(row=0, column=3)

# Set frame 2
frame2 = ttk.Frame(root)
frame2.pack()

frame2.config(height=200, width=200)
# Set button in frame 2
ttk.Button(frame2, text="Click me (#2)").grid(row=0, column=0)
ttk.Button(frame2, text="Click me (#2)").grid(row=0, column=3)
root.mainloop()