from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
from .checker import *
  
def index(request):
    return render(request, "index.html")

def priceChecker(request):

    if request.method == 'POST':
        name = request.POST.get("name")
        user_keywords = name.split(" ") 

        rahvaraamat_url = createURL(user_keywords,links_list[0]) 
        bookvoed_url = createURL(user_keywords,links_list[1])
        mnogoknig_url = createURL(user_keywords,links_list[2])

        rahvaraamat_links = item_url(rahvaraamat_url,'title', 'js-link-product') # def item_url(page,class1,secondClass=None)
        bookvoed_links = item_url(bookvoed_url,'o-row', 'title')
        mnogoknig_links = item_url(mnogoknig_url,'col-xs-8')

        rahvaraamat_prices = item_price(rahvaraamat_url, 'meta', 'price') # def item_price(page,class1,secondClass=None)
        bookvoed_prices = item_price(bookvoed_url, 'buy', 'span')
        mnogoknig_prices = item_price(mnogoknig_url, 'price')

        rahvaraamat_dict =  dict(zip(rahvaraamat_links, rahvaraamat_prices)) # combine links-list and price-list to dictionary
        rahvaraamat_dict = clean_dict(rahvaraamat_dict) # def clean_dict(dict1)
        bookvoed_dict =  dict(zip(bookvoed_links, bookvoed_prices))
        mnogoknig_dict =  dict(zip(mnogoknig_links, mnogoknig_prices))

        rahvaraamat_dict.update(bookvoed_dict) #combine dictionaries
        rahvaraamat_dict.update(mnogoknig_dict) #combine dictionaries

        converted_to_num = dict((k, float(v)) for k,v in rahvaraamat_dict.items()) # convert dict values to float

        lowest_price_url = min(converted_to_num, key=converted_to_num.get)
        highest_price_url = max(converted_to_num, key=converted_to_num.get)

        return render(request, "priceChecker.html", {'lowest_price_url': lowest_price_url})
    else:
        userform = UserForm()
        return render(request, "priceChecker.html",{"form": userform})