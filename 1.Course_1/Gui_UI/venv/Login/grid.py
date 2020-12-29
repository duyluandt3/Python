from tkinter import *
from tkinter import ttk
from tkinter import messagebox


root = Tk()
root.title("Login page")
root.geometry("300x200")
root.resizable(False, False)


# User Name
uNameLabel = ttk.Label(root, text="User Name")
uNameLabel.grid(row=0, column=0)
uNameEntry = ttk.Entry(root, width=20)
uNameEntry.grid(row=0, column=1)
# Password
pwLabel = ttk.Label(root, text="Password")
pwLabel.grid(row=1, column=0)
pwEntry = ttk.Entry(root, width=20)
pwEntry.grid(row=1, column=1)
pwEntry.config(show="*")

# Login Button
loginButton = ttk.Button(root, text="Login", width=20)
loginButton.grid(row=2, column=1)

# Get input data
def BtClick():
    print("User Name:", uNameEntry.get())
    print("Password:", pwEntry.get())
    if(uNameEntry.get()=="admin" and uNameEntry.get()=="admin"):
        messagebox.showinfo(title="Login info:", message="User Name:{}, Password:{}"
                            .format(uNameEntry.get(), uNameEntry.get()))
    else:
        messagebox.showinfo(title="Login info", message="LOGIN")

loginButton.config(command = BtClick)

root.mainloop()