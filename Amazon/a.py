# class="a-section a-spacing-base a-text-center"
import requests 
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

header = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

def get_brand(card):
    brand = card.find("div",attrs={
        "class" : "a-row a-size-base a-color-secondary"
    }).text

    return brand

def get_category(card):
    category = card.find("h2",attrs={
        "class" : "a-size-mini a-spacing-none a-color-base s-line-clamp-2"
    }).text

    return category

def get_stars(card):
    stars = 0.0
    try:
        stars = card.find("div",attrs={
            "class" : "a-section a-spacing-none a-spacing-top-micro"
        }).find("span",attrs={
            "class" : "a-size-base"
        }).text
    except:
        stars = 0.0
        
    return stars


def get_review_count(card):
    review_count = 0
    try:
        review_count = card.find("div",attrs={
            "class" : "a-section a-spacing-none a-spacing-top-micro"
        }).find("span",attrs={
            "class" : "a-size-base s-underline-text"
        }).text
    except:
        review_count = 0

    return review_count


def get_price(card):
    price = card.find("div",attrs={
        "class" : "a-section a-spacing-none a-spacing-top-small s-price-instructions-style"
    }).find_all("span",attrs={
        "class" : "a-offscreen"
    })
    
    disc_price = price[0].text
    act_price = disc_price if len(price) == 1 else price[1].text

    return (disc_price,act_price)



def getSoup(url):
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.content,'lxml')

    return soup

def saveCSV(name,data):
    df = pd.DataFrame(data)
    df.to_csv(name)

if __name__ == "__main__":

    url = "https://www.amazon.in/s?k=shoes&crid=1I0U9V426YT6J&sprefix=shoe%2Caps%2C405&ref=nb_sb_noss_1"
    
    soup = getSoup(url)

    cards = soup.find_all("div",attrs={
            "class" : "a-section a-spacing-small puis-padding-left-micro puis-padding-right-micro"
        })

    data = {
        "brand" : [], # string
        "category" : [], # string 
        "stars" : [], # float
        "num_of_reviews" : [], # int
        "disc_price" : [], # float
        "act_price" : [], # float
    }

    for card in cards:
        # brand
        brand = get_brand(card)
        
        # category
        category = get_category(card)

        # stars
        stars = get_stars(card)

        # review count
        review_count = get_review_count(card)
        
        # disc price and actual price
        disc_price ,act_price = get_price(card)  


        # adding data
        data["brand"].append(brand)
        data["category"].append(category)
        data["stars"].append(stars)
        data["num_of_reviews"].append(review_count)
        data["disc_price"].append(disc_price)
        data["act_price"].append(act_price)

    
    saveCSV("data.csv",data)


    

    
        

