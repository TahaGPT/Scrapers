from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver  # Install using: pip install selenium-wire

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    # Add more user agents
]

# Randomly select a user agent
import random
user_agent = random.choice(user_agents)

# Configure Selenium Wire options
options = {
    'headers': {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        # Add more headers if needed
    }
}

# Set up Selenium Wire driver
driver = webdriver.Chrome(seleniumwire_options=options)
driver.get("www.youtube.com")
