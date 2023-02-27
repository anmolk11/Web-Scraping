import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://www.amazon.in/s?k=keyboard&rh=n%3A1389401031&ref=nb_sb_noss"

header = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

response = requests.get(url,headers=header)

soup = BeautifulSoup(response.content,"lxml")

images = soup.find_all("img",attrs={
    "class" : "s-image"
})

for link in images:
    
