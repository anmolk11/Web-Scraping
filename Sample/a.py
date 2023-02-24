import pandas as pd
from bs4 import BeautifulSoup
import requests


url = "https://webscraper.io/test-sites/e-commerce/allinone"

data = {
    "Name" : [],
    "Price" : [],
    "Description" : [],
    "Review count" : [],
    "Stars" : []
}

respose = requests.get(url)

# print(f"Status code : {respose.status_code}")

html_content = respose.content

soup = BeautifulSoup(html_content,"lxml")

# print(soup.find(class_ = "thumbnail").prettify())

cards = soup.find_all("div",attrs={
    "class" : "thumbnail"
})


for card in cards:
    # About ----------------------------
    about = card.find("div",attrs={
        "class" : "caption"
    })
    price = about.find("h4",attrs={
        "class" : "price"
    }).text
    name = about.find("a",attrs={
        "class" : "title"
    }).get("title")
    
    # Description ----------------------------
    descriptions = card.find("p",attrs={
        "class" : "description"
    }).text

    # Review ----------------------------
    review = card.find("div",attrs={
        "class" : "ratings"
    })
    review_count = review.find("p",attrs={
        "class" : "pull-right"
    }).text
    # stars = review.find("p").get("data-rating")
    
    for p in review.find_all("p"):
         if not p.has_attr('class') and not p.has_attr('id'):
              stars = p.get("data-rating")
              break

    print(f" Name : {name} \n Price : {price} \n Description : {descriptions} \n Review count : {review_count} \n Stars : {stars}")
    print("\n-----------------------------------------------------\n")

    data["Name"].append(name)
    data["Price"].append(price)
    data["Description"].append(descriptions)
    data["Review count"].append(review_count)
    data["Stars"].append(stars)

df = pd.DataFrame(data)
df.to_excel("data.xlsx")