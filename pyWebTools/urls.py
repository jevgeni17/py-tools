from django.contrib import admin
from django.urls import path
from django.urls import re_path
from priceChecker import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    re_path(r'^price-checker', views.priceChecker),
]