listItem = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tempItem = []

# without filter
item: int
for item in listItem:
    if 0 == item %2:
        tempItem.append(item)
print(tempItem)

# with filter
tempItem2 = list(filter(lambda x:x%2==0, listItem))
print(tempItem2)
