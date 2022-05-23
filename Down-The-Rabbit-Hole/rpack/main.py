from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests


def set_up_page(subtheme):
    # get_driver = GetChromeDriver() 
    # get_driver.install()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    # options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.wikipedia.com")
    searchbar = browser.find_element_by_name("search")
    searchbar.send_keys(subtheme)
    searchbar.send_keys(Keys.RETURN)
    url = browser.current_url
    word = "search="
    if word in url:
        newUrls = find_pages(url)
        return newUrls
    else:
        return url

def find_info(url):
    page = requests.get(url)
    ramen = BeautifulSoup(page.content, 'html.parser')
    paras = ramen.find_all("p", class_="")[0:5]
    information = []
    for para in paras:
        information.append(para.text)
    return information


def find_pages(url):
    page = requests.get(url)
    ramen = BeautifulSoup(page.content, 'html.parser')
    names = ramen.find_all("li", class_="mw-search-result") #, class_="mw-search-result-heading"
    newUrls = []
    for name in names[:2]:
        name = name.find("a")['href']
        new_url = f"https://www.wikipedia.com/{name}"
        newUrls.append(new_url)
    return newUrls

def find_multiple_info(newUrls):
    paragraphs = {}
    for url in newUrls:
        page = requests.get(url)
        site_paragraphs = []
        ramen = BeautifulSoup(page.content, 'html.parser')
        paras = ramen.find_all("p", class_="")[0:5]
        for para in paras:
            site_paragraphs.append(para.text)
        paragraphs[url] = site_paragraphs
    return paragraphs

# all_information = []
# for subtheme in subthemes:
#     returned_value = set_up_page(subtheme)
#     if isinstance(returned_value, list):
#         newUrls = returned_value
#         paragraphs = find_multiple_info(newUrls)
#         all_information.append(paragraphs)
#     else:
#         url = returned_value
#         information = find_info(url)
#         all_information.append(information)


# print(all_information)

