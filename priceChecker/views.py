from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm

  
def index(request):
    return render(request, "index.html")
 
def priceChecker(request):

    if request.method == 'POST':
        name = request.POST.get("name")
        return HttpResponse("<h2>Hello, {0}</h2>".format(name))
    else:
        userform = UserForm()
        return render(request, "priceChecker.html",{"form": userform})