from django.db.models.fields import files
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import CategoryForm, CommentForm, PostForm, Category
from .models import Post, Category

# Create your views here.

# untuk login user
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('frontpage')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug, category_slug=category_slug)
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form})

def write(request):

    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('frontpage')

    else:
        form = PostForm(data=request.POST, files=request.FILES)

    return render(request, 'blog/write.html', {'form': form })

def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('manage')

        else:
            form = PostForm(data=request.POST, files=request.FILES, instance=post)

    return render(request, 'blog/update_post.html', {'form': form, 'post': post})

def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('manage')

    return render(request, 'blog/delete_post.html', {'post': post})

def manage(request):
    posts = Post.objects.all()
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'blog/manage.html', context=context)

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    return render(request, 'blog/category.html', {'category': category, 'posts': posts})


def create_category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(data=request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('manage')

    else:
        form = CategoryForm(data=request.POST)

    return render(request, 'blog/create_category.html', {'form': form, 'categories': categories })



def search(request):
    query = request.GET.get('q', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search.html', {'posts': posts, 'query': query})

