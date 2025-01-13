import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd
import time
from selenium import webdriver
import requests
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

firefox_path = "/usr/bin/firefox"  # Example for Linux
geckodriver_path = "/snap/bin/geckodriver"

options = Options()
options.binary_location = firefox_path

service = Service(executable_path=geckodriver_path)
# from fake_useragent import UserAgent

headers = {"User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'}

base = 'https://www.amazon.com'

def generateMenu():
    # session = requests.Session()
    # session.headers.update({"User-Agent": UserAgent().random})
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox(service = service, options = options)
    driver.get(base)
    #   It will scroll to right above the footer of the page then scoll to the top then back to the bottom untill there is no new items being loaded

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
        link = base + actual
        print(link)
        links.append(link)
        som = box.get('aria-label')
        categ.append(som)
        print(som)
    return links, som

def giveProducts(url):
    print("VISITING : ", url)
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    html = driver.page_source
    # driver.quit()
    response = req.get(url, headers = headers)
    if not response.ok:
        print(f"Server exited with code : {reponse.status_code}")
    soup = bsp(response.text, 'lxml')
    print(soup)
    products = soup.find_all('a', class_ = 'a-link-normal s-line-clamp-2 s-link-style a-text-normal')['href']
    for product in products:
        product = url + product
    
    nextP = soup.find('a', class_ = 's-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator')['href']
    if nextP:
        url = base + nextP
        return products, url
    else:
        return products, NULL

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
    links, cat = generateMenu()
    print(links)
    products = []
    for link in links:
        while(link):
            product, link = giveProducts(link)
            products.extend(product)
