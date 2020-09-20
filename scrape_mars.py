#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver_win32/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#create dictionary that can be imported to Mongo
#this will hold all our scraped info
mars_info = {}

def scrape_news():
    try:

        #init browser
        browser = init_browser()

        #visit nasa site via splinter
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        #make into an HTML object and be able to parse with BeautifulSoup
        html = browser.html
        soup = bs(html, "html.parser")

        #reterive lastest news title and sample paragraph
        news_title = soup.find_all('div', class_='content_title')
        news_p = soup.find('div', class_='article_teaser_body').text

        #put news into global dictionary
        mars_info['news_title'] = news_title
        mars_info["news_p"] = news_p
        return mars_info
    
    finally:
        browser.quit()

# Featured image
def featured_image():
    try:
        #init browser
        browser = init_browser()

        #visit image page
        browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
        #find full image
        browser.find_by_id('full_image').first.click()

        #click on more info to get to image page
        browser.is_element_present_by_text("more info")
        more_info = browser.find_link_by_partial_text("more info")
        more_info.click()

        #parse with Beautiful soup
        html = browser.html
        image = bs(html, "html.parser")

        #featured image url
        feat_img = image.select_one("figure a img.main_image").get("src")

        #full url
        full_url = f"https://www.jpl.nasa.gov/{feat_img}"

        #put into dictionary
        mars_info['full_url'] = full_url

        return mars_info
    finally:
        browser.quit()

#Mars facts
def scrape_mars_facts():
    try:

        #visit facts website and pull facts
        facts = pd.read_html("https://space-facts.com/mars/")[0]

        #assign columns
        facts.columns=["Description", "Value"]
        #set index to descruption
        facts.set_index("Desc", inplace=True)

        #convert to html
        table_string = facts.to_html()
        #remove \n
        table_string = table_string.replace("\n", "")

        #place into dictionary
        mars_info['facts'] = data

        return mars_info
    finally:
        browser.quit()

#Hemispheres
def hemispheres():
    try:
        #init browser
        browser = init_browser()

        #vist hemi url via splinter
        browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

        #HTML object & parse with BS
        html = browser.html
        soup = bs(html, 'html.parser')

        #retreive hemisphere info
        info = soup.find_all('div', class_='item')

        #make a list for the hemisphere urls to live in and append to list
        hemi_urls = []

        #main website url
        main_url = 'https://astrogeology.usgs.gov'

        #list of hemisphere links
        for items in info:
            #grab hemisphere title
            title = items.find('h3').text
    
            #find element that leads to full image
            full_image = items.find('a', class_='itemLink product-item')['href']
    
            #go to link that has image
            browser.visit(main_url + full_image)
    
            #html object
            full_image = browser.html
    
            #parse
            soup = bs(full_image, 'html.parser')
    
            #retrieve full image
            img_url = main_url + soup.find('img', class_='wide-image')["src"]
    
            #append title and picture urls to list
            hemi_urls.append({"title": title, "img_url": img_url})
        
        #place into global dictionary
        mars_info['hemi_url'] = hemi_urls
        
        return mars_info
    finally:
        browser.quit()


