import sqlite3

class Database:
    def __init__(self):
        try:
            # Create BD
            self.conn = sqlite3.connect("books.db")
            self.cur = self.conn.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
            self.conn.commit()
            #self.conn.close()
        except IOError:
            print("Cannot connect database")

    def insert(self,title, author, year, isbn):
        try:
            #self.conn = sqlite3.connect("books.db")
            #self.cur = self.conn.cursor()
            self.cur.execute("INSERT INTO book VALUES(NULL,?,?,?,?)",(title, author, year, isbn))
            self.conn.commit()
            #self.conn.close()
        except IndexError:
            print("Cannot insert data")

    def view(self):
        try:
            #self.conn = sqlite3.connect("books.db")
            #self.cur = self.conn.cursor()
            self.cur.execute("SELECT * FROM book")
            rows = self.cur.fetchall()
            #self.conn.close()
            return rows
        except IOError:
            print("Cannot view data")

    def search(self,title="", author="", year="", isbn=""):
        try:
            #self.conn = sqlite3.connect("books.db")
            #self.cur = self.conn.cursor()
            self.cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",(title, author, year, isbn))
            rows = self.cur.fetchall()
            #self.conn.close()
            return rows
        except IndexError:
            print("Input error")

    def delete(self,id):
        try:
            #self.conn = sqlite3.connect("books.db")
            #self.cur = self.conn.cursor()
            self.cur.execute("DELETE FROM book WHERE id=?",(id,))
            self.conn.commit()
            #self.conn.close()
        except IndexError:
            print("Delete error")


    def updateData(self, id, title, author, year, isbn):
        try:
            #self.conn = sqlite3.connect("books.db")
            #self.cur = self.conn.cursor()
            self.cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",(title, author, year, isbn, id))
            self.conn.commit()
            #self.conn.close()
        except IndexError:
            print("Cannot update data")

    # Destructor
    def __del__(self):
        self.conn.close()

#database = Database()
#database.__init__()
#database.delete(2)
#print(database.view())