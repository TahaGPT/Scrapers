import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Function to scrape data from a single URL
def scrapeUrl(website, driver):
    result = {
        "Name": [],
        "Price" : [],
        "Type" : [],
        "Image" : [],
        "Link" : []
    }
    
    driver.get(website)
    print(f"Visitng : {website}")
    try:
        driver.get(website)
        Previous_Height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
            time.sleep(3)
            New_Height = driver.execute_script("return document.body.scrollHeight")
            if New_Height == Previous_Height:
                break
            Previous_Height = New_Height
        time.sleep(3)
    except:
        pass
    
    response = requests.get(website)
    if not response.ok:
        print("Server responded with exit code:", response.status_code)
        return []
    
    soup = BeautifulSoup(response.text, 'lxml')

    products = soup.find('div', class_ = 'product-grid__items css-hvew4t').find_all('div', class_ = 'product-card__body')

    for product in products:
        try:
            name = product.find('div', class_ = 'product-card__titles').find('div', class_ = 'product-card__title').text
            print(name)
            result["Name"].append(name)
        except:
            result['Name'].append(' ')

        
        
        try:
            price = product.find('div', class_ = 'product-card__price').text
            print(price)
            result["Price"].append(price)
        except:
            result['Price'].append(' ')
        




        try:
            type = product.find('div', class_ = 'product-card__titles').find('div', class_ = 'product-card__subtitle').text
            print(type)
            result["Type"].append(type)
        except:
            result['Type'].append(' ')



        
        try:
            image = product.find('img')['src']
            print(image)
            result["Image"].append(image)
        except:
            result['Image'].append(' ')







        try:
            info = product.find('a')['href']
            print(info)
            result['Link'].append(info) 
        except:
            result['Link'].append(' ')
    


    


def generateUrl(link):
    try:
        response = requests.get(link)
        if not response.ok:
            print("Server responded with exit code:", response.status_code)
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        navs = soup.find('div', class_='categories__content')
        if navs:
           links = [a['href'] for a in navs.find_all('a', href = True)]
           print(links)
           return links
        else:
            print("No navigation div found.")
            return []
    
    except Exception as e:
        print(f"Error while fetching URL {link}: {str(e)}")
        return []



# Parallelized scraping using multiprocessing
def scrapeParallel(url):
    result = {
        "Name": [],
        "Price" : [],
        "Type" : [],
        "Image" : []
    }
    name = []
    price = []
    type = []
    image = []
    driver = webdriver.Chrome()
    result = scrapeUrl(url, driver)
    driver.quit()
    return result

if __name__ == '__main__':

    link = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'
    links = generateUrl(link)
    # Number of parallel processes
    processes = len(links)

    # Using Pool for parallel execution
    with Pool(processes) as pool:
        results = pool.map(scrapeParallel, links)

    # Displaying results
    for result in results:
        if result:
            print(result)