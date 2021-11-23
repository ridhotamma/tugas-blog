from os import name
from django.urls import path
from .views import frontpage, aboutpage, category_list

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('about/', aboutpage, name='about'),
    path('category_list', category_list, name='category_list')
]