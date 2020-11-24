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

    ###Visit NASA Mars News website
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

    # news_data = {
    #     "news_title":news_title,
    #     "news_p":news_p
    # }

    ###Featured Image
    url_two = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_two)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')

    #Get the link to featured image [image=new soup]
    image = soup1.select_one('figure.lede a img').get('src')
    image
    featured_image_url = f'https://www.jpl.nasa.gov/{image}'
    featured_image_url

    # featured_image_data = {
    #     "featured_image_url":featured_image_url
    # }

    ###Mars Facts
    url_three = 'https://space-facts.com/mars/'

    #Get tables using pandas
    tables = pd.read_html(url_three)
    #tables

    df = tables[0]
    #df.head(10)

    facts_df = df.rename(columns={0: "Description", 1: "Mars"})
    #facts_df

    html_table = facts_df.to_html()
    #html_table

    html_table_string = html_table.replace('\n', '')
    #html_table_string

    ###Mars Hemispheres  - unfinished part
    # hemisphere_image_urls = [
    # {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    # {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    # {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    # {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    # ]

    final_data = [ 
        {"news_title":news_title, "news_p":news_p},
        {"featured_image_url":featured_image_url},
        {"html_table_string":html_table_string},
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}

    ]

    # Close the browser after scraping
    browser.quit()

    # Return results
    # return news_data, featured_image_data, html_table_string, hemisphere_image_urls
    return final_data