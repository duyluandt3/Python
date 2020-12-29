import sqlite3

class Connect:
    def __init__(self):
        self._db = sqlite3.connect("infomation.db")
        # Create table
        self._db.row_factory = sqlite3.Row
        # Add state in db
        self._db.execute("create table if not exists Admin("
                   "ID integer primary key autoincrement, Name text, age int)")
        self._db.commit()

    # Add data into database
    def AddData(self, Name, age):
        try:
            self._db.row_factory = sqlite3.Row
            #Add record data
            self._db.execute("insert into Admin(Name, age) values(?, ?)",(Name, age))
        except IOError:
            print("Cannot add data")
        else:
            self._db.commit()
            print("Data Recorded")

    # Delete record data of database
    def DeleteData(self, ID):
        try:
            self._db.row_factory = sqlite3.Row
            self._db.execute("delete from Admin where ID = '{}'".format(ID))
            self._db.commit()
        except IOError:
            print("Cannot delete data")
        else:
            print("Deleted data")

    # List data
    def ListData(self):
        try:
            self._cusor = self._db.execute("select * from Admin")
            for row in self._cusor:
                print("ID:{}, Name:{}, Age:{}".format(row["ID"],row["Name"], row["age"]))
        except IOError:
            print("Cannot list data")
        else:
            print("\n*** Data Listed ***")

    # Update Data
    def UpdateData(self, ID, Age):
        try:
            self._db.row_factory = sqlite3.Row
            self._db.execute("update Admin set Age = ? where ID = ?",(Age, ID))
            self._db.commit()
        except IOError:
            print("Cannot update data")
        else:
            print("Updated Data")

