temps = [200, 225, 228, 300, -999]

new_temp = [temp /10  if temp != -999 else 0 for temp in temps]

print(new_temp)