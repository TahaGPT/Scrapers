import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd
import time
from selenium import webdriver
import requests
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions




if __name__ == '__main__':
    info = {
        'Title' : [],
        'Category' : [],
        'Average_Rating' : [],
        'Rating_Number' : [],
        'Features' : [[]],
        'Description' : [[]],
        'Price' : [],
        'Images' : [[]],
        'Videos' : [[]],
        'Store' : [],
        'Categories' : [],
        'Details' : [[]],
        'Parent_asin' : [],
        'Bought_Together' : [] 
    }

    