from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import pandas as pd
from IPython.display import HTML

# Specify the path to Firefox Developer Edition binary
firefox_dev_path = r"C:\\Users\\KW032723\\AppData\\Local\\Firefox Developer Edition\\firefox.exe"  # Adjust this path if necessary

# Set options for Firefox, specifying the binary location
options = webdriver.FirefoxOptions()
options.binary_location = firefox_dev_path

# Set up the GeckoDriver with the correct service
service = Service(GeckoDriverManager().install())

# Initialize the browser with the correct options
browser = Browser('firefox', options=options, service=service, headless=False)

# Visit the Milky Way facts page
facts_url = "https://space-facts.com/galaxies/milky-way/"
browser.visit(facts_url)

# Use Pandas to scrape data
tables = pd.read_html(facts_url)

# Take second table for Milky Way facts
milkyway_df = tables[0]

# Rename columns and set index
milkyway_df.columns = ['description', 'value']
print(milkyway_df)

# Convert table to HTML
milkyway_facts_table = milkyway_df.to_html(classes='data table table-borderless', index=False, header=False, border=0)
print(milkyway_facts_table)

# Close the browser
browser.quit()

def main():
    # Specify the path to Firefox Developer Edition binary
    firefox_dev_path = r"C:\\Users\\KW032723\\AppData\\Local\\Firefox Developer Edition\\firefox.exe"  # Adjust this path if necessary

    # Set options for Firefox, specifying the binary location
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_dev_path

    # Set up the GeckoDriver with the correct service
    service = Service(GeckoDriverManager().install())

    # Initialize the browser with the correct options
    browser = Browser('firefox', options=options, service=service, headless=False)

    # Search for the meta tag with property 'og:description'
    browser.visit('https://space-facts.com/jupiter/')
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for the meta tag with property 'og:description'
    meta_tag = soup.find('meta', property='og:description')

    # Check if the meta tag is found and extract the content
    if meta_tag:
        description = meta_tag.get('content')
        if description:
            print(description.split('.')[0])  # Print the first sentence
        else:
            print("No content found in the meta tag.")
    else:
        print("No meta tag found with the specified property.")

    # Find the paragraph containing the information about Jupiter
    entry_content = soup.find('div', class_='entry-content clearfix')
    if entry_content:
        paragraph = entry_content.find('p')
        if paragraph:
            text = paragraph.text
            
            # Extract the specific information about Jupiter's size
            start = text.find("It is two and a half times")
            end = text.find("combined.") + len("combined.")
            jupiter_info = text[start:end]
            print(jupiter_info)
        else:
            print("No paragraph found in the entry content.")
    else:
        print("No entry content found with the specified class.")

    # Find the meta tag with the name 'twitter:data1'
    meta_tag = soup.find('meta', attrs={'name': 'twitter:data1'})

    # Check if the meta tag is found and extract the content
    if meta_tag:
        reading_time = meta_tag.get('content')
        if reading_time:
            print(f"Estimated reading time: {reading_time}")
        else:
            print("No content found in the meta tag.")
    else:
        print("No meta tag found with the specified name.")

    # Close the browser
    browser.quit()

if __name__ == "__main__":
    main()