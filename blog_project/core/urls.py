from os import name
from django.urls import path
from .views import frontpage, aboutpage

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('about/', aboutpage, name='about')
]