import sqlite3

def CreateTable():
    # Create BD
    conn = sqlite3.connect("DBLite.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS store(item TEXT, quantity INTEGER, price REAL)")
    conn.commit()
    conn.close()

def insertData(item, quantity, price):
    conn = sqlite3.connect("DBLite.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO store VALUES(?,?,?)",(item,quantity,price))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("DBLite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()
    conn.close()
    return rows

def deleteData(item):
    conn = sqlite3.connect("DBLite.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM store WHERE item=?",(item,))
    conn.commit()
    conn.close()

# Update data
def updateData(quantity,price,item):
    conn = sqlite3.connect("DBLite.db")
    cur = conn.cursor()
    cur.execute("UPDATE store SET quantity=?, price=? WHERE item=?",(quantity,price,item))
    conn.commit()
    conn.close()


#insertData("Water", 10, 5.5)
#insertData("Fruit", 10, 5.5)
updateData(11,4,"Fruit")
#deleteData("Water")
print(view())