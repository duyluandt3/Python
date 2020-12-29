from tkinter import  *
from tkinter import ttk

root = Tk()

# Create style
style = ttk.Style()
style.configure("Tbutton", background="#e1d8b9", font=("Arial", 20))

# Creat entry
entry = ttk.Entry(root, width=50)
entry.pack()

# Creat button
button = ttk.Button(root, text = "Click me")
button.pack()

# Insert image
logo = PhotoImage(file="google.gif")
button.configure(image=logo, compound=CENTER)
resize_logo = logo.subsample(10,10)
button.configure(image=resize_logo)


# Get data from UI to terminal
def BuClick():
    print(entry.get())
    # delete data in entry when command is geted
    entry.delete(0, END)
    # Insert in entry
    entry.insert(0, "Button is clicked")

# export data to command
button.config(command = BuClick)

root.mainloop()