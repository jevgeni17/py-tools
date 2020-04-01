from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import requests

links_list = ['rahvaraamat.ee/search/productList/en?offset=0&limit=10&searchTerm={}', 'bookvoed.ee/search?q={}&count=50#page-1', 'mnogoknig.ee/search/{}']

def createURL(keywordsList,urlExample): # returns a serach url with user keywords
    """ NOTICE!  white fang  - there is a book title example (which user will write in the form as a keyword)
        urlExample -             rahvaraamat.ee/search/productList/en?offset=0&limit=10&searchTerm={} - where {} there are search keywords
        function will return =>  rahvaraamat.ee/search/productList/en?offset=0&limit=10&searchTerm=мартин+иден  - instead of  {} will paste search keywords
                                 bookvoed.ee/search?q={}&count=50#page-1 =>  bookvoed.ee/search?q=white+fang
                                 mnogoknig.ee/search/{}  =>   mnogoknig.ee/search/white+fang

    """
    plusKeywords = '+'.join(keywordsList)
    url = 'https://' + urlExample.replace("{}",plusKeywords)
    return url

def item_url(page,class1,secondClass=None): # returns list of links for each item in search page.
    #.title > a.js-link-product     - rahvaraamat
    #.o-row > a.title               - bookvoed
    #.col-xs-8 > a                  - mnogoknig
    page = requests.get(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    
    if secondClass == None:
        string = f".{class1} > a"
    else:
        string = f".{class1} > a.{secondClass}"

    for a in soup.select(string):
        href = urljoin(page.url, a.get('href'))
        links.append(href)

    return links

def item_price(page,class1,secondClass=None): # returns list of prices for each item in search page
    # .meta > p.price - rahvaraamat
    # .buy > span     - bookvoed
    # .price          -mnogoknig
    page = requests.get(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = []
    if secondClass == None:
        string = f".{class1}"
    elif secondClass == 'span':
        string = f".{class1} > {secondClass}"
    elif secondClass == 'price':
        string = f".{class1} > p.{secondClass}"

    for p in soup.select(string):
        p =  p.get_text()
        prices.append(p)
    prices = [i.partition(' €')[0] for i in prices] # delete unnecessary symbols
    prices = [i.strip() for i in prices] # delete whitespaces
    prices = [i.replace('€','') for i in prices] # delete unnecessary symbols
    return prices

def clean_dict(dict1):
    copy = dict1.copy()
    for k, v in copy.items():    
        if v == 'Out of stock':
            del dict1[k]
        elif v == 'This product is not available on e-store':
            del dict1[k]
    return dict1