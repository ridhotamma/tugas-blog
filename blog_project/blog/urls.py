from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    
    path('search/', views.search, name='search'),
    path('write/', views.write, name='write'),
    path('manage/', views.manage, name='manage'),
    path('create-category/', views.create_category, name='create-category'),
    path('delete-post/<int:pk>/', views.deletePost, name='delete-post'),
    path('update-post/<int:pk>/', views.updatePost, name='update-post'),
    path('<slug:slug>/', views.category, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name='post_detail'),
]