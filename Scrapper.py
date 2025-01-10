import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd

def getPage(url): # function to get the html of the scrapped page for readability
    response = req.get(url)
    if not response.ok:
        print("Server responded with exit code:", response.status_code) # if scrapping is not allowed
        return None
    else:
        soup = bsp(response.text, "lxml") # converting to html
        pretty = soup.prettify() # increasing readability
        with open('scrapped.html', 'w', encoding='utf-8') as htmlFile:  # specify encoding method
            htmlFile.write(pretty)
        return soup

        def findContent(soup, info):
            if soup is None: # if previous function returned none
                return
            
            # going from basic to specific
            ol = soup.find('ol', class_='row') 
            articles = ol.find_all('article', class_='product_pod')

            for article in articles:
                # extracting the title
                try:
                    image = article.find('h3').find('a')
                    title = image.attrs['title']
                    print(title)
                    info['Title'].append(title)
                except:
                    info['Title'].append(' ')

                    
                # extracting the ratings
                try:
                    stars = article.find('p', class_='star-rating')
                    star = stars['class'][1] if len(stars['class']) > 1 else "No rating"
                    print(star)
                    info['Star-Rating'].append(star)
                except:
                    info['Star-Rating'].append(' ')


                # extracting the prices
                try:
                    prices = article.find('p', class_='price_color')
                    price = prices.text.strip() #if price_text.startswith('£') else 0.0
                    print(price)
                    info['Price'].append(price)
                except:
                    info['Price'].append(' ')


                # extracting the availabilities
                try:
                    avail = article.find('p', class_='instock availability')
                    availability = avail.text.strip()
                    print(availability)
                    info['Availability'].append(availability)
                except:
                    info['Availability'].append(' ')



def main():  # the function in which all the functionality takes place
    info = { # uninitialized dictionary to use for later 
        'Title': [],
        'Price': [],
        'Star-Rating': [],
        'Availability': []
    }

    for i in range(1, 50): # for all the fifty pages of the site
        url = f'https://books.toscrape.com/catalogue/page-{i}.html'
        soup = getPage(url) # receiving the html element of the page
        findContent(soup, info) # finding and extracting required stuff
    
    myFile = pd.DataFrame(info, columns=['Title', 'Price', 'Star-Rating', 'Availability']) # using pandas to specify the Database
    myFile.to_csv('infoFile.csv', index=False) # copying into the .csv file

if __name__ == '__main__':
    main()
