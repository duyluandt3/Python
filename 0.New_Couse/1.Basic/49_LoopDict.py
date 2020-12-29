student_grade = {"Heya":9.1, "Murano": 7.8, "Satata": 5.9}

for val in student_grade.items():
    print(val)

for val_key in student_grade.keys():
    print(val_key)

for val_val in student_grade.values():
    print(val_val)

phone_numbers = {"John Smith": "+37682929928", "Marry Simpons": "+423998200919"}

for key, value in phone_numbers.items():
    print("{}:{}".format(key, value))
