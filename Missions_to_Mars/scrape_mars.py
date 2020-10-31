# Import All Dependencies:
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
# Setup Executable Path:
executable_path = {'executable_path': './chromedriver'}
browser = Browser('chrome', **executable_path)

def mars_news(browser):
    # Establish the Visit to the NASA MARS URL:
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional Delay: 
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Parsing the results with html and beautiful soup:
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_element = news_soup.select_one('ul.item_list li.slide')
        slide_element.find("div", class_='content_title')
        news_title=slide_element.find("div",class_="content_title").get_text()
        news_paragraph=slide_element.find("div",class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    return news_title, news_paragraph

def jpl_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()
    html = browser.htmlhtml = browser.html
    image_soup = soup(html, "html.parser")
    img_url = image_soup.select_one("figure.lede a img")
    img_url

    try:
        img_url=img_url.get("src")
    except AttributeError:
        return None, None
        img_url_base=f"https://www.jpl.nasa.gov{img_url}"
        return img_url_base

def mars_facts(): 
    try:
        facts_df=pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    facts_df.columns=["Description","Value"]
    facts_df.set_index("Description",inplace=True)
    return facts_df.to_html(classes="table table striped")

def hemisphere(browser):
   url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(url)
   hemisphere_img_url=[]
   Url_links=browser.find_by_css("a.product-item h3")
   for L in range(len(Url_links)):
        hemisphere={}
        browser.find_by_css("a.product-item h3")[L].click()
        slide_element=browser.find_link_by_text("Sample").first
        hemisphere["img_url"]=slide_element["href"]
        hemisphere["title"]=browser.find_by_css("h2.title").text
        hemisphere_img_url.append(hemisphere)
        browser.back()
   return hemisphere_img_url

def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        slide_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        slide_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": slide_element
    }
    return hemisphere

def scrape_all():
    news_title, news_paragraph = mars_news(browser)
    img_url = jpl_image(browser)
    facts = mars_facts()
    hemisphere_image_url = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_url,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())