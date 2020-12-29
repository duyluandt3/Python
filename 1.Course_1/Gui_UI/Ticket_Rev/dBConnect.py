import sqlite3

class DBConnect:
    def __init__(self):
        self._db = sqlite3.connect("Reservation.db")
        # Create table
        self._db.row_factory = sqlite3.Row
        # Add state in db
        self._db.execute("create table if not exists Ticket("
                   "ID integer primary key autoincrement, Name text, Gender text, Comment text)")
        self._db.commit()

    # Add data into database
    def AddData(self, Name, Gender, Comments):
        try:
            self._db.row_factory = sqlite3.Row
            #Add record data
            self._db.execute("insert into Ticket(Name, Gender, Comment) values(?, ?, ?)",
                             (Name, Gender, Comments))
        except IOError:
            return "Cannot add data"
        else:
            self._db.commit()
            return "Data Recorded"

    # Delete record data of database
    def DeleteData(self, ID):
        try:
            self._db.row_factory = sqlite3.Row
            self._db.execute("delete from Ticket where Name = '{}'".format(ID))
            self._db.commit()
        except IOError:
            return "Cannot delete data"
        else:
            return "Deleted data"

    # List data
    def ListData(self):
        try:
            cusor = self._cusor = self._db.execute("select * from Ticket")
            return cusor

            '''
            for row in self._cusor:
                print("ID:{}, Name:{}, Gender:{}, Comment:{}".
                      format(row["ID"],row["Name"], row["Gender"], row["Comment"]))
            '''
        except IOError:
            return "Cannot list data"
        else:
            return "\n*** Data Listed ***"

    # Update Data
    def UpdateData(self, ID, Comments):
        try:
            self._db.row_factory = sqlite3.Row
            self._db.execute("update Admin set Comment = ? where ID = ?",(Comments, ID))
            self._db.commit()
        except IOError:
            return "Cannot update data"
        else:
            return "Updated Data"
