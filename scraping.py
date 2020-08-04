# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)
    title, img_url, thumbnail_src = challenge_image(browser)
    
    cImage1 = img_url[0]
    cTitle1 = title[0]
    thumbnail_1 = thumbnail_src[0]

    cImage2 = img_url[1]
    cTitle2 = title[1]
    thumbnail_2 = thumbnail_src[1]

    cImage3 = img_url[2]
    cTitle3 = title[2]
    thumbnail_3 = thumbnail_src[2]

    cImage4 = img_url[3]
    cTitle4 = title[3]
    thumbnail_4 = thumbnail_src[3]

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "challenge_image_1": cImage1,
        "challenge_title_1": cTitle1,
        "thumbnail_1": thumbnail_1,
        "challenge_image_2": cImage2,
        "challenge_title_2": cTitle2,
        "thumbnail_2": thumbnail_2,
        "challenge_image_3": cImage3,
        "challenge_title_3": cTitle3,
        "thumbnail_3": thumbnail_3,
        "challenge_image_4": cImage4,
        "challenge_title_4": cTitle4,
        "thumbnail_4": thumbnail_4,
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def challenge_image(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    img_url = []
    title = []
    thumbnail_src = []

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    items = img_soup.find_all('div', class_='item')
    for item in items: 
        
        item_url_href = item.find('a', class_="itemLink product-item")['href']
        thumbnail_src.append(item.find('img', class_="thumb")['src'])
        item_url = f'https://astrogeology.usgs.gov{item_url_href}'
        browser.visit(item_url)

        html = browser.html
        img_soup_2 = BeautifulSoup(html, 'html.parser')

        try:
            title.append(img_soup_2.find('h2', class_='title').get_text())
            download_ele = img_soup_2.find('div', class_='downloads')
            img_url.append(download_ele.find('a')['href'])
        
        except AttributeError:
            return None, None, None
        
        
    return title, img_url, thumbnail_src

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())