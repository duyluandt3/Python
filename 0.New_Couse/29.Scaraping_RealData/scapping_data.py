import requests
from bs4 import BeautifulSoup

web_data=requests.get("https://www.century21.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")

data_content=web_data.content

make_beauty=BeautifulSoup(data_content,"html.parser")

#Extracting div
all=make_beauty.find_all("div",{"class":"propertyRow"})

print(all)
#print(make_beauty.prettify())