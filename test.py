# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver  # Install using: pip install selenium-wire

# List of user agents
# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    # Add more user agents
# ]

# Randomly select a user agent
# import random
# user_agent = random.choice(user_agents)

# # Configure Selenium Wire options
# options = {
#     'headers': {
        # 'User-Agent': user_agent,
#         'Accept-Language': 'en-US,en;q=0.9',
#         # Add more headers if needed
#     }
# }

# # Set up Selenium Wire driver
# driver = webdriver.Chrome(seleniumwire_options=options)
# driver.get("www.youtube.com")


# string = "Hello, Wrld!"
# substring = "World"
# result = string.replace(substring, "")
# print(result)  # Output: "Hello, !"

# import pandas as pd

# file_path = "AmazonCategories_Cleaned_Final2.csv"  # Update with your actual path

# # Read the CSV file with semicolon as the delimiter
# df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")

# # Print column names to verify
# print("Column names in CSV:", df.columns)

# # Remove duplicates based on "Subcategory 1"
# df_deduplicated = df.drop_duplicates(subset=["Mai+Category", "Subcategory+1"], keep="first")

# # Save cleaned data
# output_path = "AmazonCategories_Cleaned_Final.csv"
# df_deduplicated.to_csv(output_path, index=False, sep=";")  # Keep semicolon delimiter

# print(f"Duplicates removed. Cleaned data saved to {output_path}.")



# import re
# import time
# from datetime import datetime
# date_pattern = r"\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b"
# reviewTimes = 'Reviewed in the United States on February 7, 2025'
# reviewTimes = re.search(date_pattern, reviewTimes)
# reviewTiming = datetime.strptime(reviewTimes, "%B %d, %Y")
# print("Review Time :", reviewTiming)
# reviewTime = int(reviewTiming.timestamp())



# import pandas as pd
# import re

# file_path = "AmazonCategories_Final.csv"  # Update with your actual path

# # Read the CSV file with semicolon delimiter
# df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")

# # Function to clean text: replace spaces with '+' and remove special characters
# def clean_text(text):
#     text = text.replace(" ", "+")  # Replace spaces with '+'
#     text = re.sub(r"[^a-zA-Z0-9+]", "", text)  # Remove special characters
#     return text

# # Apply cleaning to column names
# df.columns = [clean_text(col) for col in df.columns]

# # Apply cleaning to all column values
# df = df.applymap(lambda x: clean_text(str(x)) if isinstance(x, str) else x)

# # # Remove duplicates based on "Subcategory+1"
# # df_deduplicated = df.drop_duplicates(subset="Mai+Category", keep="first")

# # Save cleaned data
# output_file = "AmazonCategories_Cleaned_Final2.csv"
# df.to_csv(output_file, index=False, sep=";")  # Keep semicolon delimiter

# print(f"Duplicates removed. Cleaned data saved to {output_file}.")




import requests as req
import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup as bsp
from selenium import webdriver
from seleniumwire import webdriver  # blinker == 1.7.0
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from googlesearch import search
from datetime import datetime
from collections import defaultdict

maxDate = "June 1, 2023"
maxDateT = datetime.strptime(maxDate, "%B %d, %Y")

base = 'https://www.amazon.com'
number_pattern = r"\d+"
date_pattern = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b"
options = {
    'headers' : {
        "User-Agent": UserAgent().random
    }
}
link = "https://www.amazon.com/Maybelline-Volumizing-Buildable-Lengthening-Multiplying/dp/B08H3JPH74/?_encoding=UTF8&ref_=pd_hp_d_btf_nta-top-picks"
print(link)

driver = webdriver.Chrome(seleniumwire_options = options)
driver.get(link)
time.sleep(10)
Previous_Height = driver.execute_script("return document.body.scrollHeight")
print(f"Height : {Previous_Height}" )
while True:
    # It will scroll to right above the footer of the page then scoll to the top then back to the bottom untill there is no new items being loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
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
feat = []
img = []
vid = []
det = []
# extracting details
try:
    detailsBoard = soup.find('div', class_ = 'a-expander-content a-expander-section-content a-section-expander-inner').find('table', class_ = 'a-keyvalue prodDetTable').find_all('tr')
except:
    try:
        detailsBoard = soup.find('div', id = 'detailBullets_feature_div').find_all('li')
    except:
        try:
            detailsBoard = soup.find('table', id = 'productDetails_detailBullets_sections1').find_all('tr')
        except:   
            try:
                detailsBoard = soup.find('ul', class_ = 'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list').find_all('tr')
            except:
                detailsBoard = []
details = {}
if detailsBoard:
    for detailBoard in detailsBoard:
        detailingH = detailBoard.find('th').text.strip() if detailBoard.find('th') else None
        detailingA = detailBoard.find('td').text.strip() if detailBoard.find('td') else None
        if detailingH and detailingA:
            detailed = {detailingH: detailingA} 
            details |= detailed  
else:
    details = {}
print("Details :", details)
date = ""
try:
    for value in reversed(list(details.values())):
        if isinstance(value, str):
            date = re.search(date_pattern, value)
            print("Date Found", date)
            if date:
                date = date.group(0)
                dateT = datetime.strptime(date, "%B %d, %Y")
                if dateT > maxDateT:
                    print(f"{date} is after {maxDateT}")
                elif dateT < maxDateT:
                    print(f"{date} is before {maxDateT}")
                else:
                    print(f"{date} is the same as {maxDateT}")
                break
except:
    print("Date not found")
    date = ""
print("Date :", date)
# # extracting Category
# category = row['Categories']
# print("Category :", category)
# agent["main_category"] = category
# extracting Title
try:
    titleBoard = soup.find('span', id = 'productTitle')
    title = titleBoard.text.strip()
except:
    title = ""
print("Title :", title)
# agent["title"] = title
# extracting ratings
try:
    ratingBoard = soup.find('div', id = 'averageCustomerReviews')
    # extracting average rating
    avgRatingBoard = ratingBoard.find('span', class_ = 'a-size-base a-color-base')
    avgRating = avgRatingBoard.text.strip()
    # extracting rating number
    ratingNoBoard = ratingBoard.find('span', id = 'acrCustomerReviewText')
    ratingNo = ratingNoBoard.text.strip()
    junk = " ratings"
    ratingNo = ratingNo.replace(junk, "")
except:
    avgRating = ""
    ratingNo = ""
print("Average Rating :", avgRating)
# agent["average_rating"] = avgRating
print("Rating :", ratingNo)
# agent["rating_number"] = ratingNo
# extracting price
try:
    priceBoard = soup.find('div', class_ = 'a-section a-spacing-none aok-align-center aok-relative').find('span', class_ = 'aok-offscreen')
    price = priceBoard.text.strip()[0:5]
except:
    price = ""
print("Price :", price)
# agent["price"] = price
# exracting media
try:
    mediaBoard = soup.find('ul', class_ = 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro regularAltImageViewLayout')
    if not mediaBoard:
        mediaBoard = soup.find('ul', class_ = 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro gridAltImageViewLayoutIn1x7')
        if not mediaBoard:
            mediaBoard = soup.find('ul', class_ = 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-extra-large regularAltImageViewLayout')
            if not mediaBoard:
                mediaBoard = soup.find('ul', class_ = 'a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-vertical a-spacing-top-extra-large regularAltImageViewLayout')
    media = mediaBoard.find_all('img')
    images = [img['src'] for img in media]
    vids = images[-1]
    images = images[0:-1]
except:
    images = []
    vids = []
print("Images :", images)
# agent["images"] = images   
print("Videos :", vids)
# agent["videos"] = vids
# extracting the store
try:
    storeBoard = soup.find('tr', class_ = 'a-spacing-small po-brand').find('td', class_ = 'a-span9')
    store = storeBoard.text.strip()
except:
    try:
        storeBoard = soup.find('a', id = 'bylineInfo').text.strip()
        junk = "Visit the "
        store = storeBoard.replace(junk, "")
    except:
        store = ""
print("Store :", store)
# agent["store"] = store
# extracting features
try:
    featuresBoard = soup.find('ul', class_ = 'a-unordered-list a-vertical a-spacing-mini').find_all('li')
    features = [feature.text.strip() for feature in featuresBoard]
except:
    features = []
print("Features :", features)
# agent["features"] = features
    
                
# extracting asin
try:
    asin = details['ASIN']
except:
    asin = ""
print("ASIN :", asin)
# agent["parent_asin"] = asin

# agent["date"] = date

# extracting description
try:
    descriptionBoard = soup.find('table', class_ = 'a-normal a-spacing-micro')
    if not descriptionBoard:
        descriptionBoard = soup.find('ul', id = 'a-nostyle').find_all('div', class_ = 'a-fixed-left-grid-col a-col-right')
    descriptions = descriptionBoard.find_all('td', class_ = 'a-span9')
    description = [dec.text.strip() for dec in descriptions]
except:
    description = []
print("Description :", description)
# agent["description"] = description
# extracting bought together
try:
    boughtTogetherBoard = soup.find('div', id = 'a-cardui _c3AtZ_new-thumbnail-box_1W9Ku _c3AtZ_two-item-thumbnail-box_7kF95')
    if not boughtTogetherBoard:
        boughtTogetherBoard = soup.find('div', class_ = 'a-cardui _p13n-desktop-sims-fbt_fbt-desktop_new-thumbnail-box__36bD3 _p13n-desktop-sims-fbt_fbt-desktop_two-item-thumbnail-box__jV2am')
    if not boughtTogetherBoard:
        boughtTogetherBoard = soup.find('div', class_ = 'a-cardui _p13n-desktop-sims-fbt_fbt-desktop_new-thumbnail-box__36bD3')
    boughtTogetherS = boughtTogetherBoard.find_all('a', class_ = 'a-link-normal a-text-normal', href = True)
    if not boughtTogetherS:
        boughtTogetherS = boughtTogetherBoard.find_all('a', class_ = 'a-link-normal', href = True)        
    boughtTogether = [base + link['href'] for link in boughtTogetherS]
except:
    boughtTogether = []
print("Bought Together :", boughtTogether)
# agent["bought_together"] = boughtTogether
# extracting further categories
try:
    categoriesBoard = soup.find_all('div', id= 'tp-inline-twister-dim-values-container')
    categoriesBoardAh = categoriesBoard[-1].find_all('li')
    categories = [categoriesBoardh.text.strip() for categoriesBoardh in categoriesBoardAh]
except:
    categories = []
print("Categories :", categories)
# agent["categories"] = categories
############################################################################################################################################################
# print("\n\n\n-------------------------------------------------------------------Comments-------------------------------------------------------------------")
# extracting reviews
try:
    reviewsUS = soup.find('ul', id = 'cm-cr-dp-review-list').find_all('li')
except:
    reviewUS = []

try:
    reviewsGlobal = soup.find('ul', id = 'cm-cr-global-review-list').find_all('li')
except:
    reviewsGlobal = []
reviews = reviewsUS + reviewsGlobal
for review in reviews:
    
    try:
        # extracting rating
        reviewRatingBoard = review.find('a', {'data-hook': 'review-star-rating'})
        reviewRatingBoard = reviewRatingBoard.find_all('span')
        try:
            reviewRating = reviewRatingBoard[0].text.strip()
            reviewRating = reviewRating[0:3]
        except:
            reviewRating = ""

        try:
            reviewTitle = reviewRatingBoard[-1].text.strip()
        except:
            reviewTitle = ""
    except:
        reviewRating = ""
        reviewTitle = ""
    print("Rating :", reviewRating)
    # comment["rating"].append(reviewRating)
    # extracting title
    print("Title :", reviewTitle)
    # comment["title"].append(reviewTitle)
    # extracting Text
    try:
        reviewTextBoard = review.find('div', class_ = 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content')
        reviewText = reviewTextBoard.text.strip()
    except:
        reviewText = ""
    print("Review :", reviewText)
    # comment["text"].append(reviewText)
    # extracting images
    try:
        reviewImages = review.find('div', class_ = 'review-image-tile-section').find_all('img')
        Images = [img['src'] for img in reviewImages]
    except:
        Images = []
    print("Images :", Images)
    # comment["images"].append(Images)
    # extracting ASIN
    try:
        reviewAsin = review.get('id')
    except:
        reviewAsin = ""
    print("ASIN :", reviewAsin)
    # comment["asin"].append(reviewAsin)
    # extracting parent ASIN
    reviewParentAsin = asin
    print("Parent ASIN :", reviewParentAsin)
    # comment["parent_asin"].append(review)
    # eaxtracting username
    try:
        username = review.find('span', class_ = 'a-profile-name').text.strip()
    except:
        username = ""
    print("Username :", username)
    # comment["user_id"].append(username)
    # extracting date
    try:
        reviewTimeBoard = review.find('span', class_ = 'a-size-base a-color-secondary review-date')
        reviewTimes = reviewTimeBoard.text
        reviewTime = re.search(date_pattern, reviewTimes)
        reviewTime = reviewTime.group(0)
        print("Date Found")
    except:
        reviewTime = ""
    print("Date :", reviewTime)
    # comment["timestamp"].append(reviewTime)
    verified = False
    if review.find('span', class_ = 'a-size-mini a-color-state a-text-bold'):
        verified = True
    print("Verified :", verified)
    # comment["verified_purchase"].append(verified)
    # extracting helpfulness
    try:
        reviewHelpful = review.find('span', class_ = 'a-size-base a-color-tertiary cr-vote-text')
        reviewHelpful = reviewHelpful.text
        haha = "One"
        helpful = 0
        Helpfulness = re.search(number_pattern, reviewHelpful)
        if Helpfulness:
            helpful = int(Helpfulness.group())
        elif haha in reviewHelpful:
            helpful = 1
    except:
        helpful = 0
    print("Helpful :", helpful)
    # comment["helpful_vote"].append(helpful)
    # myMeta = pd.DataFrame(agent)
    # myRev = pd.DataFrame(comment)
# if not me:
#     # myMeta.to_csv(meta, mode='a', index = False)
#     myRev.to_csv(rev, mode='a', index = False)
#     me = True
# else:
#     # myMeta.to_csv(meta, mode='a', header=False, index = False)
#     myRev.to_csv(rev, mode='a', header=False, index = False)

print("|||||||||||||||||||||||||||| Data appended successfully with continued index. |||||||||||||||||||||||||||")
    




# print("\n\n\n\n\n\n-------------------------------------------------------------------Product-------------------------------------------------------------------")
# options = {
#         'headers' :{
            # "User-Agent":UserAgent().random
#         }
#     }
# link = "https://www.amazon.com/HEX-BOTS-Crawler-Rechargeable-Control/dp/B0CSFPL6JN/ref=sr_1_2?_encoding=UTF8&sr=8-2"
# print(link)
# driver = webdriver.Chrome(seleniumwire_options = options)
# driver.get(link)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# driver.execute_script("window.scrollTo(0, 0);")
# time.sleep(10)
# html = driver.page_source
# driver.quit()
# soup = bsp(html, 'lxml')
# feat = []
# img = []
# vid = []
# det = []
# # extracting details
# try:
#     detailsBoard = soup.find('div', class_ = 'a-expander-content a-expander-section-content a-section-expander-inner').find('table', class_ = 'a-keyvalue prodDetTable').find_all('tr')
# except:
#     try:
#         detailsBoard = soup.find('div', id = 'detailBullets_feature_div').find_all('li')
#     except:
#         try:
#             detailsBoard = soup.find('table', id = 'productDetails_detailBullets_sections1').find_all('tr')
#         except:   
#             try:
#                 detailsBoard = soup.find('ul', class_ = 'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list').find_all('tr')
#             except:
#                 detailsBoard = []
# # find th for the dictionary subject and td for the disctionary details
# details = {}
# if detailsBoard:
#     for detailBoard in detailsBoard:
#         detailingH = detailBoard.find('th').text.strip() if detailBoard.find('th') else None
#         detailingA = detailBoard.find('td').text.strip() if detailBoard.find('td') else None
#         if detailingH and detailingA:
#             detailed = {detailingH: detailingA} 
#             details |= detailed  
# else:
#     details = {}
# print("Details :", details)
# date_pattern = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b"


# try:
#     for value in details.values():
#         if isinstance(value, str):
#             date = re.findall(date_pattern, value)
#             if date:
#                 break
# except:
#     date = ""
# print("Date :", date)
