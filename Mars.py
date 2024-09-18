from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import pandas as pd

# Specify the path to Firefox Developer Edition binary
firefox_dev_path = r"C:\Users\KW032723\AppData\Local\Firefox Developer Edition\firefox.exe"  # Adjust this path if necessary

# Set options for Firefox, specifying the binary location
options = webdriver.FirefoxOptions()
options.binary_location = firefox_dev_path

# Set up the GeckoDriver with the correct service
service = Service(GeckoDriverManager().install())

# Initialize the browser with the correct options
driver = webdriver.Firefox(service=service, options=options)

# Use splinter's Browser class correctly
browser = Browser('firefox', headless=False, options=options)

facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)

# Use Pandas to scrape data
tables = pd.read_html('https://space-facts.com/mars/')

# Take second table for Mars facts
mars_df = tables[0]

# Rename columns and set index
mars_df.columns = ['description', 'value']

# Convert table to html
mars_facts_table = [mars_df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]

# Display the HTML table
from IPython.display import HTML
HTML(mars_facts_table[0])

# Open browser to USGS Astrogeology site
browser.visit('https://astrogeology.usgs.gov/search/?target=&system=&p=1&accscope=&geoform=&mapprojn=&missikey=&searchBar=hemisphere')

html = browser.html
soup = bs(html, 'html.parser')

hemi_names = []

# Search for the names of all planets
results = soup.find_all('div', class_="planet-button")

# Check if results is not empty
if results:
    for result in results:
        span = result.find('span')
        if span:
            hemi_names.append(span.text)
else:
    print("No results found with the specified class name.")

hemi_names

# Initialize an empty list to store the links
thumbnail_links = []

html = browser.html
soup = bs(html, 'html.parser')

# Search for the divs containing the links
results = soup.find_all('div', class_="item")

# Check if results is not empty
if results:
    # Loop through the results and extract the links
    for result in results:
        a_tag = result.find('a', class_='itemLink product-item')
        if a_tag:
            href = a_tag['href']
            # Check if href is a relative path
            if href.startswith('/'):
                link = 'https://astrogeology.usgs.gov' + href
            else:
                link = href
            thumbnail_links.append(link)
else:
    print("No results found with the specified class name.")

thumbnail_links

full_imgs = []

for url in thumbnail_links:
    
    # Print the URL to debug
    print(f"Visiting URL: {url}")
    
    # Click through each thumbnail link
    browser.visit(url)
    
    # Wait for the page to load
    browser.is_element_present_by_css('img.wide-image', wait_time=10)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Scrape each page for the relative image path
    results = soup.find_all('img', class_='wide-image')
    
    # Check if results is not empty
    if results:
        relative_img_path = results[0]['src']
        
        # Combine the relative image path to get the full URL
        img_link = 'https://astrogeology.usgs.gov' + relative_img_path
        
        # Print the image link to debug
        print(f"Found image link: {img_link}")
        
        # Add full image links to a list
        full_imgs.append(img_link)
    else:
        print(f"No image found for URL: {url}")

full_imgs
