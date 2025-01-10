import requests
import re
from bs4 import BeautifulSoup as bsp
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

def generateMenu(url) -> list:
    response = requests.get(url, headers=headers)
    soup = bsp(response.text, 'lxml')
    if not response.ok:
        print("Server responded with exit code:", response.status_code)
        return [] 
    else:
        # print(soup)
        navbar = soup.find('ul', id= 'menu-main-menu-2')
        # navbar = navbar.prettify()
        # print(navbar)
        if navbar:
            links = []
            act = navbar.find_all('li')
            for link in act:
                links.append(link.find('a')['href'])
            print(links)
            newLinks = links[1:4] + links[5:6] + links[7:10]
            # print(newLinks)
            return newLinks
        else:
            print("Navbar not found")
            return []


def generateNews(url, info) -> list:
    driver = webdriver.Chrome()
    driver.get(url)
    # Define a WebDriverWait instance to wait for elements
    # wait = WebDriverWait(driver, 10)  # wait up to 10 seconds for elements

    # for _ in range(10):
    #     # It will scroll to right above the footer of the page then scoll to the top then back to the bottom untill there is no new items being loaded

    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 700);")
    #     time.sleep(5)
    #     try:
    #         # Wait for the "Load more" button to be clickable
    #         load_more_button = wait.until(EC.element_to_be_clickable(
    #             (By.CSS_SELECTOR, 'a.td_ajax_load_more.td_ajax_load_more_js')
    #         ))
    #         # Click the "Load more" button
    #         load_more_button.click()
    #         print("Clicked 'Load more' button.")
    #         time.sleep(5)  # Wait for the new content to load
    #     except Exception as e:
    #         # print(f"An error occurred: {e}")
    #         print("Not CLicked")
    #         break

    # # Optional: quit the driver after finishing
    html = driver.page_source
    driver.quit()
                
    news = list()
    # response = requests.get(url, headers=headers)
    # if not response.ok:
    #     print("Server responded with exit code:", response.status_code)
    #     return []
    # else:
    soup = bsp(html, 'lxml')
    board = soup.find('div', class_='td_block_inner tdb-block-inner td-fix-index')
    # print(board)
    if board:
        big = board.find_all('div', class_ = 'td-module-container td-category-pos-above')
        for small in big:
            news.append(small.find('h3').find('a', href = True)['href'])
            category = soup.find('h1', class_ = 'tdb-title-text').text.strip()
            print(category)
            info['Category'].append(category)

        print(news)
        return news
    else:
        print("News board not found")
        return []


def scrapeData(link, info):
    response = requests.get(link, headers = headers)
    if not response.ok:
        print("Server responded with exit code:", response.status_code)
    else:
        soup = bsp(response.text, 'lxml')

    try:
        board = soup.find('div', class_='tdc-row stretch_row_1200 td-stretch-content')
        # receipt = board.find('div', class_='content-area')
        title = soup.find('h1', class_='tdb-title-text').text.strip() if board.find('h1', class_='tdb-title-text') else 'No Title'
        print("Title : ", title)
        # summary = board.find('div', class_='wpb_wrapper').find('p').text.strip() if board.find('div', class_='wpb_wrapper') else 'No Summary'
        # print("Summary : ", summary)
        # category = board.find('div', class_='breadcrumb').text.strip() if board.find('div', class_='breadcrumb') else 'No Category'
        # date = soup.find('div', class_='tdb-block-inner td-fix-index').text.strip() if soup.find('div', class_='tdb-block-inner td-fix-index') else 'No Date'
        # image = board.find('div', class_ = 'td_block_wrap tdb_single_bg_featured_image tdi_67 tdb-content-horiz-left td-pb-border-top td_block_template_1').find('style', url) if board.find('div', class_ = 'td_block_wrap tdb_single_bg_featured_image tdi_67 tdb-content-horiz-left td-pb-border-top td_block_template_1') else 'No Image'
        image = 'No Image'  # Default value if no image is found

        # Find the specific div with the desired class
        div = board.find('div', class_='td_block_wrap tdb_single_bg_featured_image tdi_67 tdb-content-horiz-left td-pb-border-top td_block_template_1')

        if div:
            # Find the <style> tag within that div
            style_tag = div.find('style')

            if style_tag:
                # Use a regular expression to extract the URL from the background property
                match = re.search(r"background:url\('(.*?)'\);", style_tag.string)
                if match:
                    image = match.group(1)

        # Output the image URL or the default message
        print("Image URL:", image)
        date = soup.find('time', class_ = 'entry-date updated td-module-date').text.strip() if soup.find('time', class_ = 'entry-date updated td-module-date') else 'No Date'
        print("Date : ", date)
        receipt = soup.find('div', class_ = 'tdb-block-inner td-fix-index')
        paragraphs = [p.text.strip() for p in receipt.find_all('p')] if receipt else []
        print("Paragraphs : \n", paragraphs)

        info['Header'].append(title)
        info['Summary'].append(summary)
        info['CreationDate'].append(date)
        info['Pic_url'].append(image)
        info['Link'].append(link)
        info['Detail'].append(paragraphs)
    except Exception as e:
        print(f"An error occurred while scraping data: {e}")


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
    url = 'https://arynews.tv/'
    navs = generateMenu(url)
    news = []
    for nav in navs:
        news.extend(generateNews(nav, info))

    for link in news:
        scrapeData(link, info)

    # # Write dictionary to CSV file
    # df = pd.DataFrame(info)
    # df.to_csv('Geo.csv', index=False)