def WeatherConditon(temperature):
    if temperature > 7:
        return "Warm"
    else:
        return "Cold"

x = int(input("Teperature: "))
print(WeatherConditon(x))

input_user = input("Message: ")
#message = "Hello %s" % input_user
message = f"Hello {input_user}"
print(message)