from tkinter import  *
from tkinter import  ttk

root = Tk()

# Create button
button1 = Button(root, text="Button_1")
button1.place(x= 100, y=30)
#button1.pack()

button2 = Button(root, text="Button_2")
button2.place(x= 100, y=60)
#button2.pack()


button3 = Button(root, text="Button_3")
button3.place(x= 100, y=90)
#button3.pack()


# Theme style
style = ttk.Style()
style.theme_use("classic")
style.configure("TButton", foreground='red', font=("Arial", 20))

# Frame config
root.title("Theme")
root.geometry("300x200")



root.mainloop()