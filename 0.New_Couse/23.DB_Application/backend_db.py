import sqlite3

def connect():
    try:
        # Create BD
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
        conn.commit()
        conn.close()
    except IOError:
        print("Cannot connect database")

def insert(title, author, year, isbn):
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO book VALUES(NULL,?,?,?,?)",(title, author, year, isbn))
        conn.commit()
        conn.close()
    except IndexError:
        print("Cannot insert data")

def view():
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM book")
        rows = cur.fetchall()
        conn.close()
        return rows
    except IOError:
        print("Cannot view data")

def search(title="", author="", year="", isbn=""):
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",(title, author, year, isbn))
        rows = cur.fetchall()
        conn.close()
        return rows
    except IndexError:
        print("Input error")

def delete(id):
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM book WHERE id=?",(id,))
        conn.commit()
        conn.close()
    except IndexError:
        print("Delete error")


def updateData(id, title, author, year, isbn):
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",(title, author, year, isbn, id))
        conn.commit()
        conn.close()
    except IndexError:
        print("Cannot update data")

connect()
#insert("What","Luan", 2019, 1327)
#print(search(author="Luan"))
#updateData(4,"How long","Luan",2019,2230)
#print(view())
#delete(3)