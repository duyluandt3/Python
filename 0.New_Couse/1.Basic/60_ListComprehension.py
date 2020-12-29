temps = [200, 225, 228, 300]

new_temp = []

for temp in temps:
    new_temp.append(temp /10)

print(new_temp)

# List Conprehension
new_temp2 = [temp /10 for temp in temps]
print(new_temp2)