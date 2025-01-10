from bs4 import BeautifulSoup as bsp
import hashlib
import logging
import pandas as pd
import requests
import time
from selenium import webdriver


def generateMenu(url) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = bsp(response.text, 'lxml')
        
        navbar = soup.find('div', class_='menu-area')
        if navbar:
            links = [a['href'] for a in navbar.find_all('a', class_='open-section', href=True)]
            newLinks = links[2:6] + links[10:12] + links[13:15]
            logging.info(f"Menu links found: {newLinks}")
            return newLinks
        else:
            logging.warning("Navbar not found")
            return []
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []

def generateNews(url) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = bsp(response.text, 'lxml')
        
        board = soup.find('div', class_='row video-list laodMoreCatNews')
        if board:
            news = [a['href'] for a in board.find_all('a', class_='open-section', href=True)]
            return news
        else:
            logging.warning("News board not found")
            return []
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []

def calculate_hash(title, date, link):
    hash_object = hashlib.sha256()
    hash_object.update(f"{title}{date}{link}".encode('utf-8'))
    return hash_object.hexdigest()

def scrapeData(link, info, stored_hashes):
   l = 0
   try:
        # driver = webdriver.Chrome()
        # driver.get(link)
        response = requests.get(link)
        # # driver = webdriver.Chrome()
        # # driver.get(link)
        # driver.quit()
        response.raise_for_status()
        soup = bsp(response.text, 'lxml')

        board = soup.find('div', class_='column-right')
        receipt = board.find('div', class_='content-area')


        try:
            title = board.find('div', class_='heading_H').find('h1').text.strip() if board.find('div', class_='heading_H') else 'No Title'
            print(title)
        except:
            title = " "
            l +=1

        try:
            summary = board.find('div', class_='except').text.strip() if board.find('div', class_='except') else 'No Summary'
            # print(summary)
        except:
            summary = " "
            l +=1


        try:
            category = board.find('div', class_='breadcrumb').text.strip() if board.find('div', class_='breadcrumb') else 'No Category'
            # print(category)
        except:
            category = " "
            l +=1
 
        try:    
            date = board.find('p', class_='post-date-time').text.strip() if board.find('p', class_='post-date-time') else 'No Date'
            # print(date)
        except:
            date = " "
            l +=1
 
        try:
            image = receipt.find('img', src=True)['src'] if receipt.find('img', src=True) else 'No Image'
            # print(image)
        except:
            image = " "  
            l +=1      
 
        try:
            paragraphs = [p.text.strip() for p in receipt.find_all('p')] if receipt else []
            # print(paragraphs)
        except:
            paragraphs = " "
            l +=1

        article_hash = calculate_hash(title, date, link)
        if article_hash in stored_hashes:
            logging.info(f"Article already stored: {title}")
            return
        
        info['Header'].append(title)
        info['Summary'].append(summary)
        info['Category'].append(category)
        info['CreationDate'].append(date)
        info['Pic_url'].append(image)
        info['Link'].append(link)
        info['Detail'].append(paragraphs)

        print("\n\n\n\n=======================================================", article_hash ,"=======================================================\n\n\n")
        stored_hashes.add(article_hash)

        if( l== 7):
            with open('junk.csv', 'a') as f:
                f.write(receipt.text)
            l = 0

   except Exception as e:
        logging.error(f"An error occurred while scraping data from {link}: {e}")
        if( l== 7):
            with open('junk.csv', 'a') as f:
                f.write(receipt.text)
            l = 0

def load_existing_hashes(filename):
    hashes = set()
    try:
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            article_hash = calculate_hash(row['Header'], row['CreationDate'], row['Link'])
            # print("\n\n\n||||||||||||||||||||||||||||||||||||||||||||||||||||||", article_hash ,"||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\n\n")
            hashes.add(article_hash)
    except FileNotFoundError:
        logging.info(f"{filename} not found. Starting fresh.")
    except Exception as e:
        logging.error(f"An error occurred while loading existing hashes: {e}")
    return hashes

if __name__ == '__main__':
    info = {
        'Header': [],
        'Summary': [],
        'Detail': [],
        'Link': [],
        'Category': [],
        'CreationDate': [],
        'Pic_url': []
    }
    
    base_url = 'https://www.geo.tv/'
    navs = generateMenu(base_url)
    news_links = []

    for nav in navs:
        news_links.extend(generateNews(nav))

    existing_hashes = load_existing_hashes('GEO.csv')
    print(existing_hashes)

    for link in news_links:
        scrapeData(link, info, existing_hashes)
        # Adding sleep to prevent overloading the server
        time.sleep(1)

    csv_file = 'newGeo.csv'
    # Write dictionary to CSV file
    new_df = pd.DataFrame(info)
    try:
        existing_df = pd.read_csv(csv_file, index_col=0)
        last_index = existing_df.index[-1]
    except FileNotFoundError:
        last_index = -1  # If the file doesn't exist, start from index 0

    # # Create a new DataFrame to append
    # new_data = {
    #     'Column1': [10, 20, 30],
    #     'Column2': [40, 50, 60]
    # }
    # new_df = pd.DataFrame(new_data)

    # Adjust the index of the new DataFrame
    new_df.index += last_index + 1

    # Append the new DataFrame to the CSV
    new_df.to_csv(csv_file, mode='a', header=False)

    print("Data appended successfully with continued index.")
