from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('write/', views.write, name='write'),
    path('<slug:slug>/', views.category, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name='post_detail'),
]