from tkinter import *
from tkinter import ttk

def Convert():
    inputKg = float(entryKG.get())
    gram = inputKg*1000
    pound = inputKg*2.20462
    ounces = inputKg*35.274
    txtGram.delete("1.0", END)
    txtGram.insert(END, gram)
    txtPound.delete("1.0", END)
    txtPound.insert(END, pound)
    txtOunces.delete("1.0", END)
    txtOunces.insert(END, ounces)

##################### UI ########################
root = Tk()
root.title("CONVERT")
root.geometry("300x200")
root.configure(background="#e1d8b2")
root.resizable(False, False)

# Style
style = ttk.Style()
style.theme_use("classic")
style.configure("TLabel", background="#e1d8b2")
style.configure("TButton", background="#e1d8b2")
style.configure("TRadiobutton", background="#e1d8b2")

# Label
lbKG = Label(root,text="Input KG")
lbKG.grid(row=1, column=0, padx=5, pady=5)

lbGram = Label(root,text="Gram")
lbGram.grid(row=3, column=0, padx=5, pady=5)

lbPound = Label(root,text="Pound")
lbPound.grid(row=4, column=0, padx=5, pady=5)

lbOunces = Label(root,text="Ounces")
lbOunces.grid(row=5, column=0, padx=5, pady=5)

# Convert button
btConvert = Button(root,text="Convert",command=Convert)
btConvert.grid(row=2, column=2, padx=5, pady=5)

# Entry KG
entryKG = Entry(root)
entryKG.grid(row=1, column=2, padx=5, pady=5)

# Convert Gram
txtGram = Text(root,height=1,width=20,)
txtGram.grid(row=3, column=2)

# Convert Pound
txtPound = Text(root,height=1,width=20)
txtPound.grid(row=4, column=2)

# Convert Ounces
txtOunces = Text(root,height=1,width=20)
txtOunces.grid(row=5, column=2)


root.mainloop()