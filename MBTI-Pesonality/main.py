import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome 
from selenium.webdriver import ChromeOptions
import time

options = ChromeOptions()
options.headless = True
driver = Chrome(executable_path='chromedriver.exe', options=options)

data = {
    "Name" : [],
    "Category" : [],
    "MBTI" : [],
    "Subtype" : [],
    "Votes" : []
}


def getName(card):
    name =  card.find("h2",attrs={
        "class" : "info-name"
    }).text

    return name

def getCategory(card):
    category = card.find("label").text
    return category

def getMBTI(card):
    mbti_type = card.find("div",attrs={
        "class" : "personality"
    }).text
    return mbti_type

def getSubtype(card):
    subtype = card.find("div",attrs={
        "class" : "subtype"
    }).text
    return subtype

def getVote(card):
    vote = card.find("div",attrs={
        "class" : "vote-count"
    }).find("label").text
    return vote


def fetchData(content):
    cards = content.find_all("div",attrs={
        "class" : "profile-card"
    })

    for card in cards:
        name = getName(card)
        category = getCategory(card)
        mbti_type = getMBTI(card)
        subtype = getSubtype(card)
        vote = getVote(card)

        print(f"Name : {name}\nCategort : {category}\nMBTI : {mbti_type}\nSubtype : {subtype}\nVotes : {vote}",end="\n------------------\n")

        # data["Name"].append(name)
        # data["Category"].append(category)
        # data["MBTI"].append(mbti_type)
        # data["Subtype"].append(subtype)
        # data["Votes"].append(vote)


if __name__  == "__main__":
    url = "https://www.personality-database.com/profile?pid=1"
    driver.get(url)

    time.sleep(5)

    html = driver.execute_script("return document.documentElement.outerHTML")

    soup = BeautifulSoup(html,'lxml')

    content = soup.find("div",attrs={
        "id" : "root"
    })

    fetchData(content)    
