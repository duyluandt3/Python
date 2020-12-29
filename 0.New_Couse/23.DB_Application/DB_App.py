"""
Book infomation
Title, Author
Year, ISBN

User can:
View all record
Search an entry
Add entry
Update Entry
Delete
Close
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import backend_db

# Get selected event from list box
def get_select_row(event):
    try:
        global selected_tuple
        index = lstBox.curselection()[0]
        selected_tuple = lstBox.get(index)
        #return selected_tuple
        # Display selected data in entry
        entryTitle.delete(0, END)
        entryTitle.insert(END, selected_tuple[1])
        entryAuthor.delete(0, END)
        entryAuthor.insert(END, selected_tuple[2])
        entryYear.delete(0, END)
        entryYear.insert(END, selected_tuple[3])
        entryISBN.delete(0, END)
        entryISBN.insert(END, selected_tuple[4])
    except IndexError:
        pass

# Show list of db
def view_command():
    # delete old data
    lstBox.delete(0, END)
    for row in backend_db.view():
        lstBox.insert(END, row)

# Search
def search_command():
    lstBox.delete(0, END)
    for row in backend_db.search(txtTitle.get(), txtAuthor.get(),txtYear.get(),txtISBN.get()):
        lstBox.insert(END, row)

def add_command():
    backend_db.insert(txtTitle.get(), txtAuthor.get(),txtYear.get(),txtISBN.get())
    lstBox.delete(0, END)
    lstBox.insert(END, (txtTitle.get(), txtAuthor.get(),txtYear.get(),txtISBN.get()))

# Delete selected data
def delete_command():
    backend_db.delete(selected_tuple[0])
    view_command()

# Update data
def update_command():
    backend_db.updateData(selected_tuple[0],txtTitle.get(), txtAuthor.get(),txtYear.get(),txtISBN.get())
    view_command()

# Close window application
def ExitApplication():
    MsgBox = messagebox.askquestion('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       window.destroy()
    else:
        messagebox.showinfo('Return','You will now return to the application screen')

# Frame design
window = Tk()
window.title("BOOK INFORMATION")
window.geometry("450x300")
window.configure(background="#e1d8b2")
window.resizable(False, False)

# Style
style = ttk.Style()
style.theme_use("classic")
style.configure("TLabel", background="#e1d8b2")
style.configure("TButton", background="#e1d8b2")
style.configure("TRadiobutton", background="#e1d8b2")

# Label Design
lbTitle = Label(window, text="Title")
lbTitle.grid(row=0, column=0, padx=1, pady=5)

lbYear = Label(window, text="Year")
lbYear.grid(row=1, column=0, padx=1, pady=5)

lbAuthor = Label(window, text="Author")
lbAuthor.grid(row=0, column=2, padx=5, pady=5)

lbISBN = Label(window, text="ISBN")
lbISBN.grid(row=1, column=2, padx=5, pady=5)

# Entry Design
txtTitle = StringVar()
entryTitle = Entry(window, textvariable=txtTitle)
entryTitle.grid(row=0, column=1,padx=1, pady=5)

txtYear = StringVar()
entryYear = Entry(window, textvariable=txtYear)
entryYear.grid(row=1, column=1, padx=1, pady=5)

txtAuthor = StringVar()
entryAuthor = Entry(window, textvariable=txtAuthor)
entryAuthor.grid(row=0, column=3, padx=20, pady=5)

txtISBN = StringVar()
entryISBN = Entry(window, textvariable=txtISBN)
entryISBN.grid(row=1, column=3, padx=20, pady=5)

# Listbox Design
lstBox = Listbox(window, height=12, width=35)
lstBox.grid(row=2, column=0, padx=5, pady=5, rowspan=6, columnspan=2)

# Get selected event
lstBox.bind('<<ListboxSelect>>', get_select_row)

scr = Scrollbar(window, orient=VERTICAL)
scr.grid(row=2, column=2, rowspan=6)

# Set scroll
lstBox.configure(yscrollcommand=scr.set)
scr.configure(command=lstBox.yview())

# Button Design
btView = Button(window, text="View all", width=12, command=view_command)
btView.grid(row=2, column=3, padx=5, pady=2)

btSearch = Button(window, text="Search Entry", width=12, command=search_command)
btSearch.grid(row=3, column=3, padx=5, pady=2)

btAdd = Button(window, text="Add Entry", width=12, command=add_command)
btAdd.grid(row=4, column=3, padx=5, pady=2)

btUpdate = Button(window, text="Update Entry", width=12, command=update_command)
btUpdate.grid(row=5, column=3, padx=5, pady=2)

btDelete = Button(window, text="Delete Entry", width=12, command=delete_command)
btDelete.grid(row=6, column=3, padx=5, pady=2)

btClose = Button(window, text="Close", width=12, command=ExitApplication)
btClose.grid(row=7, column=3, padx=5, pady=2)

window.mainloop()