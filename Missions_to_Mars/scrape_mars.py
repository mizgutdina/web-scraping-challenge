# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    #Visit NASA Mars News website
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    #time.sleep(1)

    #Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Extract title text
    new_soup=soup.select_one('ul.item_list li.slide')
    news_title = new_soup.find('div', class_='content_title')
    news_title = news_title.text
    news_title

    #Extract paragraph 
    news_p = new_soup.find('div', class_='article_teaser_body')
    news_p = news_p.text
    news_p

    news_data = {
        "news_title":news_title,
        "news_p":news_p
    }



    # Close the browser after scraping
    browser.quit()

    # Return results
    return news_data