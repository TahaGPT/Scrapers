from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time
import random

# Function to get a random user agent
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Function to get a random proxy from a list
def get_random_proxy():
    proxies = [
        'http://123.123.123.123:8080',
        'http://124.124.124.124:8080',
        # Add more proxies
    ]
    return random.choice(proxies)

def set_up_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
    options.add_argument(f"user-agent={get_random_user_agent()}")  # Use a random user agent
    
    # Set the path to the ChromeDriver
    # service = Service('/path/to/chromedriver')
    
    # Initialize the WebDriver with the service object
    driver = webdriver.Chrome(options=options)
    return driver

# Function to log into LinkedIn
def login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    username_input = driver.find_element_by_id("username")
    password_input = driver.find_element_by_id("password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(2)

# Function to perform a search in Sales Navigator
def search_sales_navigator(driver, keyword):
    driver.get("https://www.linkedin.com/sales/search/people")
    time.sleep(2)
    search_input = driver.find_element_by_css_selector("input.search-global-typeahead__input")
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)

# Function to scrape the search results
def scrape_results(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    profiles = soup.find_all('div', {'class': 'result-lockup__wrapper'})
    for profile in profiles:
        name = profile.find('span', {'class': 'name actor-name'}).text.strip()
        title = profile.find('div', {'class': 'search-result__snippets-black'}).text.strip()
        results.append({'name': name, 'title': title})
    return results

# Main function
def main():
    # Credentials
    username = ""
    password = ""

    # Keywords
    keyword = ""

    driver = set_up_driver()
    login(driver, username, password)
    search_sales_navigator(driver, keyword)
    results = scrape_results(driver)
    for result in results:
        print(result)
    driver.quit()

if __name__ == "__main__":
    main()
