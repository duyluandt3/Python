listItem = [1, 2, 4, 6, 8]
tempList = []

print(listItem)
# without map
for item in listItem:
    tempList.append(item*2)
print(tempList)

# with map
# listItem mul by 2
tempList2 = list(map(lambda x:x*2, listItem))
print(tempList2)

# listItem add by 10
tempList3 = list(map(lambda x:x+10, listItem))
print(tempList3)