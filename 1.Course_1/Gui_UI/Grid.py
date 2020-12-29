from tkinter import *
from tkinter import ttk

root = Tk()

style = ttk.Style()
style.theme_use("classic")

ttk.Label(root, text="Green", background="green").grid(row=0, column=0, padx=5, pady=5, sticky="snew")
ttk.Label(root, text="Yellow", background="yellow").grid(row=0, column=1, padx=5, pady=5, sticky="snew")
ttk.Label(root, text="Blue", background="blue").grid(row=0, column=2, rowspan=2, sticky="sn")  #sticky: phuong huong, span: do rong
ttk.Label(root, text="Orange", background="orange").grid(row=1, column=0, columnspan=2, sticky="ew")

root.rowconfigure(0, weight=2)  # Can chinh theo hang
root.rowconfigure(1, weight=1)  # Can chinh theo hang
root.columnconfigure(1, weight=1)  # Can chinh size cot
root.columnconfigure(2, weight=2)


root.mainloop()