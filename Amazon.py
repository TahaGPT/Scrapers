import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd
import time
from selenium import webdriver
import requests
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
# from fake_useragent import UserAgent

headers = {"User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'}

def generateMenu(url):
    # session = requests.Session()
    # session.headers.update({"User-Agent": UserAgent().random})
    response = req.get(url, headers  = headers)
    if not response.ok:
        print("Server responded with exit code:", response.status_code) # if scrapping is not allowed
        return None
    else:    
        soup = bsp(response.text, 'lxml')
        links = soup.find_all('div', class_ = 'a-link-normal _fluid-quad-image-label-v2_style_centerImage__30wh- aok-block image-window')
        


if __name__ == '__main__':
    info = {
        'Title' : [],
        'Category' : [],
        'Average_Rating' : [],
        'Rating_Number' : [],
        'Features' : [[]],
        'Description' : [[]],
        'Price' : [],
        'Images' : [[]],
        'Videos' : [[]],
        'Store' : [],
        'Categories' : [],
        'Details' : [[]],
        'Parent_asin' : [],
        'Bought_Together' : [] 
    }
    generateMenu('https://www.amazon.com/')

    