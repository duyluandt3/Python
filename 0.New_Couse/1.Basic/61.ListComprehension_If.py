temps = [200, 225, 228, 300, -999]

new_temp = [temp /10 for temp in temps if temp != -999]

print(new_temp)