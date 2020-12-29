import mysql.connector

con = mysql.connector.connect(
    user = "ardit700_student",
    password = "ardit700_student",
    host = "108.167.140.122",
    database = "ardit700_pm1database"
)

cusor = con.cursor()

#input word
inputWord = input("Input word: ")

query = cusor.execute("SELECT * FROM Dictionary WHERE Expression = '%s'" % inputWord)

results = cusor.fetchall()

if results:
    for result in results:
        print(result[1])
else:
    print("No word found")