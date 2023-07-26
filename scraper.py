#scrape, then push to a database for data manipulation
from requests import get, post
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy as np
import re

"""
DB object:
listing title
year
make
model
date listed
source (craigslist, fb marketplace, dealer etc)
URL
############### stretch goal: some sort of way to save the pictures from the listing?? might cause performance issues though
"""

#base 
url = 'https://seattle.craigslist.org/search/mca#search=1~gallery~0~100'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

time.sleep(5)

html = driver.page_source

driver.get_screenshot_as_file("screenshot.png")
driver.quit()

html_soup = BeautifulSoup(html, 'html5lib')

num_results = html_soup.find('div', class_="cl-search-paginator").find('span', class_='cl-page-number').text

results = html_soup.find('div', class_="cl-search-results").find('div', class_='results').find_all('li', class_='cl-search-result')

titles = []
years = []
links = []
prices = []
locations = []
list_dates = []
miles = []
sources = []

for post in results:

    title = post.get('title')
    titles.append(title)

    year = "-1"
    match = re.search(r'\b\d{4}\b', title)
    if match:
        year = match.group()

    years.append(year)

    price = post.find('span', class_='priceinfo')
    if price:
        price = price.text
    else:
        price = "-1"
    prices.append(price)

    link = post.find('a', class_='cl-app-anchor').get('href')
    links.append(link)

    location = "-1"
    match = re.search(r"/d/(.*?)(?=-)", link)
    if match:
        location = match.group(1)
    
    locations.append(location)

    #meta info (timestamp,  mileage, locatiopn) all '.' seperated

    meta_data = post.find('div', class_='meta').text.split('·')

    list_dates.append(meta_data[0]) #if includes 'ago', replace with current date
    
    if re.search(r"(\d+|k)\s*mi", meta_data[1]):
        miles.append(meta_data[1])
    else:
        miles.append("-1")

    sources.append("Craigslist")

titles = titles[:120] #pull only the first 120 results at a time
prices = prices[:120]
locations = locations[:120]
years = years[:120]
links = links[:120]
sources = sources[:120]
list_dates = list_dates[:120]
miles = miles[:120]

import pandas as pd
df = pd.DataFrame({'title': titles,
                   'price': prices,
                   'location': locations,
                   'year': years,
                   'mileage': miles,
                   'list_date': list_dates,
                   'URL': links,
                   'source': sources
                   })

print(df.info())


print(df)
### Data Cleaning ###
#Drop duplicates
#update year to float
#update price to float
