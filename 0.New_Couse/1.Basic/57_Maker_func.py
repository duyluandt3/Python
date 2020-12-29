def maker_fun(makerValue):
    sentence = ("How", "What", "Why")
    capitalized = makerValue.capitalize()
    if capitalized.startswith(sentence):
        return "{}".format(capitalized)
    else:
        return "{}".format(capitalized)


results = []

while True:
    user_input = input("Say something:")
    if user_input == "/end":
        break
    else:
        results.append(maker_fun(user_input))

print(" ".join(results))
