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

from UI import *

WD = Tk()

user_WD = UI_Create(WD)

# Frame design
WD.title("BOOK INFORMATION")
WD.geometry("450x300")
WD.configure(background="#e1d8b2")
WD.resizable(False, False)

# Style
style = ttk.Style()
style.theme_use("classic")
style.configure("TLabel", background="#e1d8b2")
style.configure("TButton", background="#e1d8b2")
style.configure("TRadiobutton", background="#e1d8b2")

WD.mainloop()