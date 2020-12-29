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