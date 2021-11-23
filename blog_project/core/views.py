from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Category, Post

# Create your views here.
def frontpage(request):
    posts = Post.objects.filter(status=Post.ACTIVE)
    recommended_posts = Post.objects.filter(priority=Post.RECOMMENDED)
    default_posts = Post.objects.filter(priority=Post.DEFAULT)
    return render(request, 'core/frontpage.html', {'recommended_posts': recommended_posts, 'default_posts': default_posts})

def aboutpage(request):
    return render(request, 'core/about.html')

def category_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    
    return render(request, 'core/category_list.html', {'posts': posts, 'categories': categories})

def robots_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")