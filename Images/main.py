import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import io
from PIL import Image


url = "https://www.amazon.in/s?k=keyboard&rh=n%3A1389401031&ref=nb_sb_noss"

header = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

response = requests.get(url,headers=header)

soup = BeautifulSoup(response.content,"lxml")

images = soup.find_all("img",attrs={
    "class" : "s-image"
})

img = 1

for link in images:
    img_link = link.get("src")
    image_content = requests.get(img_link).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')
    file_path = "C:\\Users\hp\Desktop\X\Web-Scraping\Images\output\img" + str(img) + ".png" 
    image.save(file_path, "PNG", quality=80)
    img += 1
    
    
