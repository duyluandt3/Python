from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from backend_db import Database
database = Database()

class UI_Create:
    def __init__(self, window):
        # Label Design
        self.lbTitle = Label(window, text="Title")
        self.lbTitle.grid(row=0, column=0, padx=1, pady=5)

        self.lbYear = Label(window, text="Year")
        self.lbYear.grid(row=1, column=0, padx=1, pady=5)

        self.lbAuthor = Label(window, text="Author")
        self.lbAuthor.grid(row=0, column=2, padx=5, pady=5)

        self.lbISBN = Label(window, text="ISBN")
        self.lbISBN.grid(row=1, column=2, padx=5, pady=5)

        # Entry Design
        self.txtTitle = StringVar()
        self.entryTitle = Entry(window, textvariable=self.txtTitle)
        self.entryTitle.grid(row=0, column=1,padx=1, pady=5)

        self.txtYear = StringVar()
        self.entryYear = Entry(window, textvariable=self.txtYear)
        self.entryYear.grid(row=1, column=1, padx=1, pady=5)

        self.txtAuthor = StringVar()
        self.entryAuthor = Entry(window, textvariable=self.txtAuthor)
        self.entryAuthor.grid(row=0, column=3, padx=20, pady=5)

        self.txtISBN = StringVar()
        self.entryISBN = Entry(window, textvariable=self.txtISBN)
        self.entryISBN.grid(row=1, column=3, padx=20, pady=5)

        # Listbox Design
        self.lstBox = Listbox(window, height=12, width=35)
        self.lstBox.grid(row=2, column=0, padx=5, pady=5, rowspan=6, columnspan=2)

        # Get selected event
        self.lstBox.bind('<<ListboxSelect>>', self.get_select_row)

        self.scr = Scrollbar(window, orient=VERTICAL)
        self.scr.grid(row=2, column=2, rowspan=6)

        # Set scroll
        self.lstBox.configure(yscrollcommand=self.scr.set)
        self.scr.configure(command=self.lstBox.yview())

        # Button Design
        self.btView = Button(window, text="View all", width=12, command=self.view_command)
        self.btView.grid(row=2, column=3, padx=5, pady=2)

        self.btSearch = Button(window, text="Search Entry", width=12, command=self.search_command)
        self.btSearch.grid(row=3, column=3, padx=5, pady=2)

        self.btAdd = Button(window, text="Add Entry", width=12, command=self.add_command)
        self.btAdd.grid(row=4, column=3, padx=5, pady=2)

        self.btUpdate = Button(window, text="Update Entry", width=12, command=self.update_command)
        self.btUpdate.grid(row=5, column=3, padx=5, pady=2)

        self.btDelete = Button(window, text="Delete Entry", width=12, command=self.delete_command)
        self.btDelete.grid(row=6, column=3, padx=5, pady=2)

        self.btClose = Button(window, text="Close", width=12, command=self.ExitApplication)
        self.btClose.grid(row=7, column=3, padx=5, pady=2)

    def get_select_row(self, event):
        try:
            global selected_tuple
            index = self.lstBox.curselection()[0]
            selected_tuple = self.lstBox.get(index)
            #return selected_tuple
            # Display selected data in entry
            self.entryTitle.delete(0, END)
            self.entryTitle.insert(END, selected_tuple[1])
            self.entryAuthor.delete(0, END)
            self.entryAuthor.insert(END, selected_tuple[2])
            self.entryYear.delete(0, END)
            self.entryYear.insert(END, selected_tuple[3])
            self.entryISBN.delete(0, END)
            self.entryISBN.insert(END, selected_tuple[4])
        except IndexError:
            pass

    # Show list of db
    def view_command(self):
        # delete old data
        self.lstBox.delete(0, END)
        for row in database.view():
            self.lstBox.insert(END, row)

    # Search
    def search_command(self):
        self.lstBox.delete(0, END)
        for row in database.search(self.txtTitle.get(), self.txtAuthor.get(), self.txtYear.get(), self.txtISBN.get()):
            self.lstBox.insert(END, row)

    # Add entry to database
    def add_command(self):
        database.insert(self.txtTitle.get(), self.txtAuthor.get(), self.txtYear.get(), self.txtISBN.get())
        self.lstBox.delete(0, END)
        self.lstBox.insert(END, (self.txtTitle.get(), self.txtAuthor.get(), self.txtYear.get(), self.txtISBN.get()))

    # Delete selected data
    def delete_command(self):
        database.delete(selected_tuple[0])
        self.view_command()

    # Update data
    def update_command(self):
        database.updateData(selected_tuple[0], self.txtTitle.get(), self.txtAuthor.get(), self.txtYear.get(), self.txtISBN.get())
        self.view_command()

    # Close window application
    def ExitApplication(self):
        MsgBox = messagebox.askquestion('Exit Application','Are you sure you want to exit the application',icon = 'warning')
        if MsgBox == 'yes':
           self.window.destroy()
        else:
            messagebox.showinfo('Return','You will now return to the application screen')