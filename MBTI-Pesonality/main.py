import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.personality-database.com/profile?pid=1&sort=top"

response = requests.get(url)

htmlContent = response.content

soup = BeautifulSoup(htmlContent,"lxml")

print(soup)

card = soup.find("div",attrs = {
    "class" : "profile-card"
})
# print(card)