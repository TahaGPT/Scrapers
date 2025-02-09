# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver  # Install using: pip install selenium-wire

# # List of user agents
# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
#     # Add more user agents
# ]

# # Randomly select a user agent
# import random
# user_agent = random.choice(user_agents)

# # Configure Selenium Wire options
# options = {
#     'headers': {
#         'User-Agent': user_agent,
#         'Accept-Language': 'en-US,en;q=0.9',
#         # Add more headers if needed
#     }
# }

# # Set up Selenium Wire driver
# driver = webdriver.Chrome(seleniumwire_options=options)
# driver.get("www.youtube.com")
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver  # Install using: pip install selenium-wire

# # List of user agents
# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
#     # Add more user agents
# ]

# # Randomly select a user agent
# import random
# user_agent = random.choice(user_agents)

# # Configure Selenium Wire options
# options = {
#     'headers': {
#         'User-Agent': user_agent,
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
# # 2545580
# # Load the CSV file
# file_path = "Amazon.csv"  # Replace with the path to your CSV file
# df = pd.read_csv(file_path)
# # Remove duplicates based on the "Products" column
# df_deduplicated = df.drop_duplicates(subset="Products")

# # Overwrite the original CSV file with the cleaned data
# df_deduplicated.to_csv(file_path, index=False)

# print(f"Duplicates removed and written back to {file_path}.")
import re
import time
from datetime import datetime
date_pattern = r"\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b"
reviewTimes = 'Reviewed in the United States on February 7, 2025'
reviewTimes = re.search(date_pattern, reviewTimes)
reviewTiming = datetime.strptime(reviewTimes, "%B %d, %Y")
print("Review Time :", reviewTiming)
reviewTime = int(reviewTiming.timestamp())
