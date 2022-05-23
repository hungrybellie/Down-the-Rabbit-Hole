from . import db
from .models import User, Snippet, Info
from flask import Blueprint, jsonify, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user


#----------------------------------------------------------------------------#
#RPACK STUFF (MOVE THIS LATER)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

subthemes = ['feminist literature', 'queer love letters', 'top horror novels turned to movies','top 10 fanfictions','most tear-jerking poems']

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
    paragraphs = []
    for url in newUrls:
        page = requests.get(url)
        site_paragraphs = []
        ramen = BeautifulSoup(page.content, 'html.parser')
        paras = ramen.find_all("p", class_="")[0:5]
        for para in paras:
            site_paragraphs.append(para.text)
        paragraphs = site_paragraphs
    return paragraphs


views = Blueprint('views', __name__)

#----------------------------------------------------------------------------#
#FIXED/CONSTANT PAGES

@views.route('/')
def first_landing():
    return render_template("landing.html")

@views.route('/enter')
def user_auth():
    return render_template("log_or_sign.html")

@views.route('/welcome')
@login_required
def welcome_user():
    return render_template("welcome.html")

@views.route('/message')
@login_required
def see_message():
    return render_template("message.html")

@views.route('/options', methods=['GET', 'POST'])
@login_required
def theme_options():
    return render_template("options.html")

#----------------------------------------------------------------------------#
#THESE PAGES SHOULD ALL HAVE SIMILAR FUNCTIONALITIES

@views.route('/literature', methods=['GET', 'POST'])
@login_required
def literature():
    if request.method == 'POST':
        # subthemes = ['feminist literature', 'queer love letters', 'top horror novels turned to movies','top 10 fanfictions','most tear-jerking poems']
        # all_information = do_everything(subthemes)
        # print(all_information)
        print(Info.query.all())
    return render_template("literature.html")

@views.route('/art', methods=['GET', 'POST'])
@login_required
def art():
    subthemes = ['renaissance', 'philosophy', 'highest valued paintings', 'calligraphy']
    return render_template("art.html")

@views.route('/music', methods=['GET', 'POST'])
@login_required
def music():
    subthemes = ['brass intrument','latest hip hop releases', 'billboard top 200', 'highest streams ever', 'longest songs in history']
    return render_template("music.html")

@views.route('/tech', methods=['GET', 'POST'])
@login_required
def tech():
    subthemes = ['robots', 'VR', 'biometrics', 'DevOps', 'social media']
    return render_template("tech.html")

#----------------------------------------------------------------------------#
#PAGE FOR SEEING SEARCH FINDINGS + MAKING SNIPPETS

@views.route('/info', methods=['GET', 'POST'])
@login_required
def snip_and_sip(): #lolol sorry but this is too funny
    subthemes = ['feminist literature'] #'top horror novels turned to movies','top 10 fanfictions','most tear-jerking poems'
    def do_everything(subthemes):
        all_information = []
        for subtheme in subthemes:
            returned_value = set_up_page(subtheme)
            if isinstance(returned_value, list):
                newUrls = returned_value
                paragraphs = find_multiple_info(newUrls)
                all_information.append(paragraphs)

            else:
                url = returned_value
                information = find_info(url)
                all_information.append(information)
        return all_information

    all_information = do_everything(subthemes)
    print(all_information)
    if request.method == 'POST':
        snipText = request.form.get('snip_text')
        if len(snipText) < 5:
            flash('This snippet is too small!', category='error')
        else:
            newSnippet = Snippet(snipText=snipText, user_name=current_user.username)
            db.session.add(newSnippet)
            db.session.commit()
            print("Added information")
            return render_template("info.html", user=current_user)
    else:
        print("")
        # all_info = Info.query.all()
        # print(all_info)
        return render_template("info.html", user=current_user, all_information=all_information)
    return render_template("info.html", user=current_user)

#----------------------------------------------------------------------------#

@views.route('/my-snippets') #no POST because POST is done from the pages above
def show_snippets():
    snippets = Snippet.query.all()
    return render_template("my_snippets.html", user=current_user, snippets=snippets)