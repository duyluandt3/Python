class Account:

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, "r") as file:
            self.balance=int(file.read())

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def commit(self):
        with open(self.filepath, "w") as file:
            file.write(str(self.balance))


class Checking(Account):
    def __init__(self, filepath):
        Account.__init__(self, filepath)

    def tranfer(self, amout):
        self.balance -= amout


#account = Account("balance.txt")
#print(account.balance)
#account.withdraw(200)
#account.deposit(100)
#print(account.balance)
#account.commit()

checking = Checking("balance.txt")
checking.tranfer(500)
checking.commit()
print(checking.balance)