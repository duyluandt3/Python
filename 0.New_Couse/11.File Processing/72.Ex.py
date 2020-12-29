myData = open("bear.txt")
content = myData.read()

myData.close()

print(content[:90])