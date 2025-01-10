import requests
from bs4 import BeautifulSoup as bsp
import pandas as pd
import time
from selenium import webdriver
import logging


def generateSubs(url) ->list:
    subs = []
    subs.append(url + '/r/AskReddit')
    subs.append(url + '/r/pakistan')
    subs.append(url + '/r/mildlyinfuriating')
    return subs

def generatePosts(link, url, info):
    response = requests.get(link)
    if not response.ok:
        print("Server responded with exit code:", response.status_code) # if scrapping is not allowed
        return []
    else:
        # scrolling the page to the bottom above the footer then back up to load all the items until the end
        try:
            receipt = []
            driver = webdriver.Chrome()
            driver.get(link)
            Previous_Height = driver.execute_script("return document.body.scrollHeight")
            i = 0
            while i < 50:
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
            
            html = driver.page_source
            driver.quit()
            soup = bsp(html, 'lxml')
            try:
                posts = soup.find_all('article', class_ = 'w-full m-0')
                for post in posts:
                        temp = post.find('a', href = True)
                        try:
                            title = temp.text
                            print(title)
                        except:
                            title = ""
                            print("No Title")
                        info['Title'].append(title)
                        receipt.append(url + temp['href'])
                        print(receipt)

            except:
                receipt = []

        except Exception as e:
            logging.error(f"An error occurred while fetching from {link}: {e}")
        return receipt
        


def scrapeData(info, link):
    response = requests.get(link)
    if not response.ok:
        print("Server responded with exit code:", response.status_code) # if scrapping is not allowed
        return []
    else:
        # scrolling the page to the bottom above the footer then back up to load all the items until the end
        try:
            
            # print(board.prettify())
            driver = webdriver.Chrome()
            driver.get(link)
            Previous_Height = driver.execute_script("return document.body.scrollHeight")
            i = 0
            while i < 2:
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
            
            html = driver.page_source
            driver.quit()
            soup = bsp(html, 'lxml')
            board = soup.find('main', class_ ='main w-full flex-grid--main-container-card right-sidebar-xs')

            user = board.find('div', class_ ='flex gap-0 flex-col truncate')
            try:
                subReddit = user.find('span', class_ = 'flex flex-none subreddit-name neutral-content font-bold text-12 whitespace-nowrap').find('a', href = True)['href']
                print("SubReddit :",subReddit)
            except:
                subReddit = ""
                print("No SubReddit")
            
            try:
                username = user.find('div', class_ = 'inline-flex items-center max-w-full').text.strip()
                print("Username :",username)
            except:
                username = ""
                print("No Username")

            try:
                description = board.find('div', class_ = 'md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14').text.strip()
                print("Description :",description)
            except:
                description = ""
                print("No Description")
            
            try:
                reviews = []
                comments = soup.find_all('div', class_ = 'py-0 xs:mx-xs mx-2xs inline-block max-w-full')
                for comment in comments:
                    reviews.append(comment.text.strip())
                print(reviews)
                
            except:
                reviews = []
                print("No Reviews")

            try:
                image = board.find('img', class_ = 'i18n-post-media-img preview-img media-lightbox-img max-h-[100vw] h-full w-full object-contain relative', src = True)['src']
                print(image)
            except:
                image = ""
                print("No Image")
            

            print("Link :",link)

            

            try:
                video = board.find('shreddit-player', class_ = 'block h-full w-full max-h-full max-w-full nd:visible', src = True)['src']
                print("Video :",video)
            
                
            except:
                try:
                    video = ""
                    embed_tag = board.find('shreddit-embed')
                    if embed_tag and 'html' in embed_tag.attrs:
                        iframe_html = embed_tag['html']

                        iframe_soup = bsp(iframe_html, 'html.parser')
                        iframe_tag = iframe_soup.find('iframe')
                        if iframe_tag and 'src' in iframe_tag.attrs:
                            video = iframe_tag['src']
                            print(f"YouTube URL: {video}")
                except:
                    print("No Video")
            

            print("\n\n\n\n")
            info['User'].append(username)
            info['SubReddit'].append(subReddit)
            info['Description'].append(description)
            info['Comments'].append(reviews)
            info['Picture'].append(image)
            info['Video'].append(video)
            info['Url'].append(link)


        except Exception as e:
            logging.error(f"An error occurred while scrapping data from {link}: {e}")   

        



if __name__ == "__main__":
    info = {
        'User': [],
        'SubReddit': [],
        'Title': [],
        'Description': [],
        'Comments': [],
        'Picture': [],
        'Video': [],
        'Url': []
    }
    url = 'https://www.reddit.com'
    links = generateSubs(url)
    print(links)
    posts = []
    for link in links:
        posts.extend(generatePosts(link, url, info))
    
    for post in posts:
        scrapeData(info, post)
    
   
    # Write dictionary to CSV file
    df = pd.DataFrame(info)
    # df.reset_index(drop = True, inplace= True) 
    try:
        df.to_csv('Reddit.csv', mode='a')
        logging.info("Data has been written to GEO.csv")
    except Exception as e:
        logging.error(f"Failed to write to CSV: {e}")
