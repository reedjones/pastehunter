# PasteHunter v.10
# Author : Dibyendu Sikdar  
# Credits: 
# Code of Python to scrap urls from results is taken from here... 
# https://raw.githubusercontent.com/getlinksc/scrape_google/master/search.py
import urllib
import requests
from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Back, Style
import re

init()

#stores the pastes in raw/ directory
basedir = "raw/"

#CHANGE THE intext: WITH THE INFORMATION YOU WANT TO SEARCH
query = "site:pastebin.com intext:smtp"
query = query.replace(' ', '+')

def good_links(soup):
    return soup.find_all("a", href=lambda href: href and "http" in href and not "google" in href and not "cdn" in href)


def getContentRaw(url):
    fname = url[url.rindex("/")+1:len(url)]
    url = "https://pastebin.com/raw/"+url[url.rindex("/")+1:len(url)]
    print(f"checking {url} {fname}")
    USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    headers = {"user-agent": USER_AGENT}
    r = requests.get(url,headers=headers)
    w = open(basedir+fname,'w+')
    w.write(r.text)
    w.close()

def beginScraping():
    print(Fore.GREEN+"Starting digging google to find juicy information about "+query)


    #user-agent
    USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    headers = {"user-agent": USER_AGENT}

    results = []

    #Searching 10 results results only at a time ( per page returns 10 results )
    #Just querying 1 page to avoid detection/blacklisting, adjust as you want 
    #Change the 2nd parameter with multiple of 10 to scrap pages, like 10, 20, 30, etc
    for start in range(0,10,10):

        pos = str(start)
        URL = f"https://google.com/search?q={query}&start{pos}"
        resp = requests.get(URL, headers=headers)
        print(URL)
        if resp.status_code == 200:
            print('soup')
            soup = BeautifulSoup(resp.content, "html.parser")
            for g in good_links(soup):
                link = g['href']
                results.append(link)

    #Get the results
    for url in results:
        print(Fore.RED+"Fetching contents of "+url)
        getContentRaw(url)

if __name__ == '__main__':
    beginScraping()