from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Add Database
from dBConnect import DBConnect
from ListTicket import ListTicket

dbConnect = DBConnect()

#Frame
root = Tk()
root.configure(background="#e1d8b2")
root.title("Ticket Reservation")


# Style
style = ttk.Style()
style.theme_use("classic")
style.configure("TLabel", background="#e1d8b2")
style.configure("TButton", background="#e1d8b2")
style.configure("TRadiobutton", background="#e1d8b2")

# Design UI
# Name
ttk.Label(root, text="Full name").grid(row=0, column=0, pady=10)
entryName = ttk.Entry(root, width=30, font=('Arial', 10))
entryName.grid(row=0, column=1, columnspan=2)

# Gender
ttk.Label(root, text="Gender").grid(row=1, column=0, pady=10)
spanGender = StringVar()
spanGender.set("Male")
ttk.Radiobutton(root, text="Male", variable=spanGender, value="Male").grid(
                row=1, column=1)
ttk.Radiobutton(root, text="Female", variable=spanGender, value="Female").grid(
                row=1, column=2)

# Comment
textComment = Text(root, width=30, height=10, font=('Arial', 10))
textComment.grid(row=3, column=1, columnspan=2)
ttk.Label(root, text="Comment").grid(row=2, column=0)

# Button
commitButton = ttk.Button(root, text="Submit")
commitButton.grid(row=4, column=3, pady=5, padx=5)

listButton = ttk.Button(root, text="List Rev.")
listButton.grid(row=4, column=2, pady=5, padx=5)

def ButtonClick():
    print("Name:{}".format(entryName.get()))
    print("Gender:{}".format(spanGender.get()))
    print("Comment:{}".format(textComment.get(1.0, 'end')))
    # Add data to database
    msg = dbConnect.AddData(entryName.get(),spanGender.get(), textComment.get(1.0, 'end'))
    messagebox.showinfo(title="Add info", message=msg)
    # Clear data in form when data was added
    entryName.delete(0, 'end')
    textComment.delete(1.0, 'end')

# List all data in DB
def ButtonList():
    listTicket = ListTicket()

commitButton.config(command=ButtonClick)
listButton.config(command=ButtonList)


root.mainloop()

