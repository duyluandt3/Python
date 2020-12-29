import time
from db_creat import DBConnect


def main():
    dbConnet = DBConnect()
    while 1:
        # Select option
        print("***\n0-Exit\n1-Add\n2-Delete Data\n3-List Data\n4-Update Data \n***")
        selectOP = int(input("Your option: "))
        try:
            if(selectOP == 0):
                break
            elif (selectOP == 1):
                print("Add data")
                aName = input("Name: ")
                aAge = int(input("Age: "))
                dbConnet.AddData(aName, aAge)
            # Delete state
            elif (selectOP == 2):
                aID = int(input("ID:"))
                dbConnet.DeleteData(aID)
            elif (selectOP == 3):
                dbConnet.ListData()
            elif (selectOP == 4):
                aID = input("ID:")
                aAge = int(input("Update new Age:"))
                dbConnet.UpdateData(aID, aAge)
            else:
                print("You must input index")
                break

            time.sleep(1)
        except ValueError:
            print("Input number")
            break

if __name__ == '__main__':main()