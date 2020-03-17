from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
import time
from selenium import webdriver

  
def index(request):
    return render(request, "index.html")

links_list = ['rahvaraamat.ee/s/{}/ru?productType=&keyword={}', 'bookvoed.ee/search?q={}', 'mnogoknig.ee/search/{}']

def createURL(keywordsList,urlExample):
    """ NOTICE!  white fang  - there is a book title example (which user will write in the form as a keyword)
        urlExample -             rahvaraamat.ee/s/{}/ru?productType=&keyword={} - where {} there are search keywords
        function will return =>  rahvaraamat.ee/s/white+fang/ru?productType=&keyword=white+fang  - instead of  {} will paste search keywords
                                 bookvoed.ee/search?q={} =>  bookvoed.ee/search?q=white+fang
                                 mnogoknig.ee/search/{}  =>   mnogoknig.ee/search/white+fang

    """
    plusKeywords = '+'.join(keywordsList)
    url = 'https://' + urlExample.replace("{}",plusKeywords)
    return url

def crawl_data(url,product_link_class,price_class):
    item_dict = {}

    browser = webdriver.Chrome('chromedriver')
    browser.get(url)  
    time.sleep(4)
    html_source = browser.page_source  
    
    

    #soup = BeautifulSoup(html_source,'html.parser')  
    #class "postText" is not defined in the source code
    #titles = soup.findAll('p',{'class':'title'})
    #titles = browser.find_elements_by_xpath("//*[@id='endlessProducts']/li[1]/div/div/div/div[2]/div[1]/p[2]")
    #for link in titles:
     #   print (link.get_attribute("href"))
    elems = browser.find_elements_by_css_selector(".title [href]")
    links = [elem.get_attribute('href') for elem in elems]

    prices = browser.find_elements_by_class_name("price")
    price = [i.text for i in prices]
    #print(price)
    #for i in price:
    #    new_price = []
    #    x = i.partition('\n')[0]
    #    new_price.append(x)
    browser.quit()
    new_price = [i.partition('\n')[0] for i in price] # delete all after '\n'
    time.sleep(2)
    return new_price
    


    
def priceChecker(request):

    if request.method == 'POST':
        name = request.POST.get("name")
        user_keywords = name.split(" ") 
        test = createURL(user_keywords,links_list[1])
        test1 = crawl_data('https://www.rahvaraamat.ee/s/%D1%82%D1%80%D0%B8-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B8%D1%89%D0%B0/ru?productType=&keyword=%D1%82%D1%80%D0%B8+%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B8%D1%89%D0%B0','js-link-product','price')
        return HttpResponse(f"<a href={test1}>{test1}</a>")
    else:
        userform = UserForm()
        return render(request, "priceChecker.html",{"form": userform})