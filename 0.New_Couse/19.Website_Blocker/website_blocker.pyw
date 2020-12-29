import time
from datetime import datetime as dt

host_temp = "hosts"
host_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"
website_list = ["www.dantri.com", "dantri.com"]

# Setup infinite loop
while True:
    if dt(dt.now().year,dt.now().month, dt.now().day,1) < dt.now() < dt(dt.now().year,dt.now().month, dt.now().day,2):
        print("Working times")
        with open(host_temp, "r+") as file:
            content = file.read()
            #print(content)
            for website in website_list:
                if website in content:
                    pass
                else:
                    file.write("\n"+redirect + " " + website)
    else:
        with open(host_temp, "r+") as file:
            content = file.readlines()
            # Start with first of pointer
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
            file.truncate()

        print("Fun times")

    time.sleep(5)