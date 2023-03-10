import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome 
from selenium.webdriver import ChromeOptions
import time

data = {
    "Name" : [],
    "Category" : [],
    "MBTI" : [],
    "Subtype" : [],
    "Votes" : []
}

url = "https://www.personality-database.com/profile?pid=1"

options = ChromeOptions()
options.headless = True

driver = Chrome(executable_path='chromedriver.exe', options=options)
driver.get(url)

time.sleep(5)

html = driver.execute_script("return document.documentElement.outerHTML")

soup = BeautifulSoup(html,'lxml')

content = soup.find("div",attrs={
    "id" : "root"
})

cards = content.find_all("div",attrs={
    "class" : "profile-card"
})

for card in cards:
    name =  card.find("h2",attrs={
        "class" : "info-name"
    }).text

    category = card.find("label").text

    mbti_type = card.find("div",attrs={
        "class" : "personality"
    }).text
    
    subtype = card.find("div",attrs={
        "class" : "subtype"
    }).text

    vote = card.find("div",attrs={
        "class" : "vote-count"
    }).find("label").text

    print(f"Name : {name}\nCategort : {1}\nMBTI : {mbti_type}\nSubtype : {subtype}\nVotes : {vote}",end="\n------------------\n")
    
    # data["Name"].append(name)
    # data["Category"].append(category)
    # data["MBTI"].append(mbti_type)
    # data["Subtype"].append(subtype)
    # data["Votes"].append(vote)

