user_name = input("User name:")
sur_name = input("Sur name: ")

#message = f"Hello {user_name} {sur_name}"
message = "Hello %s %s" % (user_name, sur_name)

print(message)