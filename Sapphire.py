import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd
import time
from selenium import webdriver
import requests
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
info = {  # uninitialized dictionary to use for later
        'Name': [],
        'Price': [],
        'Image': [],
        'Link':[]
    }
url = 'https://pk.sapphireonline.pk/'
# Getting the navbar of the website
soup = bsp(req.get(url).content, 'html.parser')
# getting the navbar of the website which has a ul tag with class 't4s-nav__ul t4s-d-inline-flex t4s-flex-wrap t4s-align-items-center'
navbar = soup.find('ul', class_='t4s-nav__ul t4s-d-inline-flex t4s-flex-wrap t4s-align-items-center')
# In the ul there are li tag each tag has a href in the a tag
links = [link.find('a')['href'] for link in navbar.find_all('li')]
# adding the url to the links
links = [url + link for link in links]

for link in links:
    print(link)
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


        # getting the div with class 't4s-section-inner t4s_nt_se_template--16016591585354__main t4s_se_template--16016591585354__main t4s-container-fluid'
        try:
            products = soup.find_all('div', class_='t4s-product-wrapper')
            # print(products)
            for product in products:
                try:
                    # getting name in h3 tag of class 't4s-product-title'
                    name = product.find('h3', class_='t4s-product-title').text.strip()
                    print(name)
                    info['Name'].append(name)
                except:
                    info['Name'].append(' ')

                try:
                    # getting price from div with class 't4s-product-price'
                    price = product.find('div', class_='t4s-product-price').text.strip()
                    print(price)
                    info['Price'].append(price)
                except:
                    info['Price'].append(' ')

                try:
                    # getting the href from div with class 't4s-product-btns t4s-col-2 t4s-col-lg-5'
                    link = product.find('div', class_='t4s-product-btns t4s-col-2 t4s-col-lg-5').find('a')['href']
                    print(url + link)
                    info['Link'].append(url+link)
                except:
                    info['Link'].append(' ')

                try:
                    # getting image from div with class 't4s-product-img t4s_ratio is-show-img2'
                    image = product.find('div', class_='t4s-product-img t4s_ratio is-show-img2').find('img')['src']
                    print(image)
                    info['Image'].append(image)
                except:
                    info['Image'].append(' ')
        except:
            pass
# print(info)
# Write dictionary to CSV file
df = pd.DataFrame(info)
df.to_csv('Sapphire.csv')
