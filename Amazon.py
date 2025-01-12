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
    driver = webdriver.Chrome()
    driver.get(url)
    #   It will scroll to right above the footer of the page then scoll to the top then back to the bottom untill there is no new items being loaded

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 700);")
    time.sleep(10) 
    html = driver.page_source
    driver.quit()          
    soup = bsp(html, 'lxml')
    boxes = soup.find_all('a', class_ = 'a-link-normal _fluid-quad-image-label-v2_style_centerImage__30wh- aok-block image-window')
    print(boxes)
    links = []
    categ = []
    for box in boxes:
        actual = box.get('href')
        print(actual)
        links.extend(url + actual)
        som = box.get('aria-label')
        categ.extend(som)
        print(som)
    return links, som


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
    links, cat = generateMenu('https://www.amazon.com')

    