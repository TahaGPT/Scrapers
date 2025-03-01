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

import pandas as pd

file_path = "AmazonCategories_Cleaned_Final2.csv"  # Update with your actual path

# Read the CSV file with semicolon as the delimiter
df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")

# Print column names to verify
print("Column names in CSV:", df.columns)

# Remove duplicates based on "Subcategory 1"
df_deduplicated = df.drop_duplicates(subset=["Mai+Category", "Subcategory+1"], keep="first")

# Save cleaned data
output_path = "AmazonCategories_Cleaned_Final.csv"
df_deduplicated.to_csv(output_path, index=False, sep=";")  # Keep semicolon delimiter

print(f"Duplicates removed. Cleaned data saved to {output_path}.")



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
