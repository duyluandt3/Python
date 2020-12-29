import os

def Read():
    try:
        ReadFile = open("text.txt", "r")
        for line in ReadFile:
            print(line)
        ReadFile.close()
    except IOError:
        print("File is not found")

def InputValule():
    try:
        x = int(input("Number: "))
        print(x)
    except ValueError:
        print("You must input number type")

# Write file
def WriteFile():
    try:
        wFile = open("test.txt", "w")
        for i in range(5):
            InputToFile = input("Enter your string: ")
            wFile.write("\n{}".format(InputToFile))
            if InputToFile == "END":
                break
    except IOError:
        print("Cannot write in this file")

def main():
#    InputValule()
    WriteFile()

if __name__ == '__main__':main()
