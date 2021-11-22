from os import name
from django.urls import path
from .views import categoryList, frontpage, aboutpage

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('about/', aboutpage, name='about'),
    path('categories/', categoryList, name='categories')
]