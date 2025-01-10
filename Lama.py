import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd
import csv
import json
import time
from selenium import webdriver
import random
import requests
info = {  # uninitialized dictionary to use for later
        'Name': [],
        'Price': [],
        'Image': [],
        'Link':[]
    }
url = 'https://lamaretail.com/collections/woman-studio-collection'
# Getting the navbar of the website
soup = bsp(req.get(url).content, 'html.parser')
# getting the ul tag with the class name "site-nav site-navigation small--hide"
ol = soup.find('ul', class_='site-nav site-navigation small--hide')
# getting the li tags inside the ul tag
lis = ol.find_all('li')
# within each li tag there is an ul tag with the class name "site-nav__dropdown text-left" and within that there are li tags
# we are extracting the href attribute of the a tag within the li tag
links = []
for li in lis:
    ul = li.find('ul', class_='site-nav__dropdown text-left')
    if ul is not None:
        for li in ul.find_all('li'):
            a = li.find('a')
            links.append(a['href'])
for i in range(len(links)):
    links[i] = 'https://lamaretail.com' + links[i]
    
print(links)

def get_valid_proxies():
    proxy_list_url = 'https://free-proxy-list.net/'
    response = requests.get(proxy_list_url)
    soup = bsp(response.text, 'html.parser')
    proxy_data = []
    rows = soup.find_all('tr')[1:]
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 8:
            ip_address = columns[0].text.strip()
            google_enabled = columns[5].text.strip().lower() == 'yes'
            https_enabled = columns[6].text.strip().lower() == 'yes'
            last_checked = columns[7].text.strip()
            if (last_checked.endswith('mins ago') and int(last_checked.split(' ')[0]) < 15) or last_checked.endswith('hours ago'):
                if google_enabled or https_enabled:
                    proxy_data.append({'ip_address': ip_address, 'google_enabled': google_enabled, 'https_enabled': https_enabled})

    return proxy_data

def rotate_user_agent(proxy):
    if proxy:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    return headers
# Scrapping the links one by one
for link in links:
    # Getting the navbar of the website
    response = req.get(link)
    if not response.ok:
        print("Server responded with exit code:", response.status_code) # if scrapping is not allowed
    else:
        soup = bsp(response.content, 'html.parser')
        # scrolling the page to the bottom above the footer then back up to load all the items until the end
        driver = webdriver.Chrome()
        driver.get(link)
        Previous_Height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # It will scroll to right above the footer of the page then scoll to the top then back to the bottom untill there is no new items being loaded
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
            time.sleep(5)
            New_Height = driver.execute_script("return document.body.scrollHeight")
            if New_Height == Previous_Height:
                break
            Previous_Height = New_Height
            # if there is a popup press the close button
            try:
                driver.find_element_by_class_name('modal-close').click()
            except:
                pass
            
        
        # getting the html content of the page
        html = driver.page_source
        driver.quit()
        # parsing the html content
        soup = bsp(html, 'html.parser')
        pretty = soup.prettify() # increasing readability
        with open('scrapped.html', 'w', encoding='utf-8') as htmlFile:  # specify encoding method
            htmlFile.write(pretty)

        
        lists = soup.find('div', class_ = 'grid grid--uniform')
        dresses = lists.find_all('div', class_ = 'grid__item-image-wrapper')

        for dress in dresses:
            # getting the name
            try:
                dressName = dress.find('div', class_='grid-product__title grid-product__title--body')
                name = dressName.text.strip()
                print(name)
                info['Name'].append(name)
            except:
                info['Name'].append(' ')
            
            # getting the price
            try:
                dressPrice = soup.find('div', class_='grid-product__meta').find('div', class_='grid-product__price').find('span', class_='money')
                price = dressPrice.string.strip()  # Use .strip() to clean up any surrounding whitespace
                print(price)
                info['Price'].append(price)
            except:
                info['Price'].append(' ')


            # getting the image
            try:
                dressImage = dress.find('div', class_= 'grid-product__image-mask').find('div', class_ = 'image-wrap loaded').find('img')
                image = 'https:' + dressImage['src']
                print(image)
                info['Image'].append(image)
            except:
                info['Image'].append(' ')

            # getting the link
            try:
                dressLink = dress.find('a', class_ = 'grid-product__link')
                link = 'https://lamaretail.com' + dressLink['href']
                print(link)
                info['Link'].append(link)
            except:
                print("kuch nhi")
                info['Link'].append(' ')



# Write dictionary to CSV file
csvFile = 'lama.csv' # writing the headings of the columns
with open(csvFile, mode='w', newline='', encoding='utf-8') as file: # using an encoder for special characters
    fieldnames = list(info.keys()) # typecasting the keys into a list
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    
    for i in range(len(info['Name'])): # according to number of items, we are copying every value of every key into it's respective heading
        row = {
            'Name': info['Name'][i],
            'Price': info['Price'][i],
            'Link': info['Link'][i],
            'Image': info['Image'][i]
        }
        writer.writerow(row)


 # Write dictionary to JSON file
json_file = 'lama.json'
with open(json_file, mode='w', encoding='utf-8') as file:
    # Prepare list of dictionaries for JSON serialization
    json_data = []
    for i in range(len(info['Name'])): # according to number of items, we are copying every value of every key into it's respective heading
        row = {
            'Name': info['Name'][i],
            'Price': info['Price'][i],
            'Link': info['Link'][i],
            'Image': info['Image'][i]
        }
        json_data.append(row)
    
    # Write JSON data to file
    json.dump(json_data, file, indent=4, ensure_ascii=False)
        
            

