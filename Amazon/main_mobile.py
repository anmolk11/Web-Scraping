# class="a-section a-spacing-base a-text-center"
import requests 
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from urllib.parse import urljoin

header = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

data = {
        "brand" : [], # string
        "description" : [], # string 
        "stars" : [], # float
        "num_of_reviews" : [], # int
        "disc_price" : [], # float
        "act_price" : [], # float
    }


def get_brand(card):
    brand = card.find("span",attrs={
        "class" : "a-size-medium a-color-base a-text-normal"
    }).text

    return brand

def get_description(card):
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
        review_count = int(''.join(filter(str.isdigit, review_count)))
    except:
        review_count = 0

    return review_count


def get_price(card):
    try:
        price = card.find("div",attrs={
            "class" : "a-row a-size-base a-color-base"
        }).find_all("span",attrs={
            "class" : "a-offscreen"
        })
        disc_price = price[0].text
        act_price = disc_price if len(price) == 1 else price[1].text

        disc_price = float(''.join(filter(str.isdigit, disc_price)))
        act_price = float(''.join(filter(str.isdigit, act_price)))
    except:
        disc_price = -1
        act_price = -1
    
    

    return (disc_price,act_price)



def getSoup(url):
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.content,'lxml')

    return soup

def saveCSV(name,data):
    df = pd.DataFrame(data)
    df.to_csv(name)

def getAllLinks(url):
    links = []

    while True:
        links.append(url)
        soup = getSoup(url)
        footer = soup.select_one("div.a-section.a-text-center.s-pagination-container") 
        next_button = footer.find("a",attrs={
        "class" : "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"
        })
        if next_button:
            next_page_url = next_button.get("href")
            url = urljoin(url,next_page_url)
        else:
            break

    return links

def extractData(url):
    soup = getSoup(url)
    cards = soup.find_all("div",attrs={
         "class" : "s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis s-latency-cf-section s-card-border"
    })
    for card in cards:
        # brand
        brand = get_brand(card)
        brand, description = brand.split(maxsplit=1)
        
        # stars
        stars = get_stars(card)
        
        # review count
        review_count = get_review_count(card)
        
        # disc price and actual price
        disc_price ,act_price = get_price(card)  
        
        # adding data
        data["brand"].append(brand)
        data["description"].append(description)
        data["stars"].append(stars)
        data["num_of_reviews"].append(review_count)
        data["disc_price"].append(disc_price)
        data["act_price"].append(act_price)



if __name__ == "__main__":

    home_url = "https://www.amazon.in/s?k=mobile&rh=p_72%3A1318479031&dc&ds=v1%3AvBZjy7Wn23a8h51gCOf7OFvIqg5PvkRo4jowXa9Y%2BS8&crid=1RJIT475MY9BF&qid=1677492325&rnid=1318475031&sprefix=mobil%2Caps%2C259&ref=sr_nr_p_72_4"
    
    links = getAllLinks(home_url)

    for url in links:
        extractData(url)

    saveCSV("mobile_data.csv",data)