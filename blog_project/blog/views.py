from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.models import Group, User

from .forms import CategoryForm, CommentForm, PostForm, Category, CreateUserForm, WriterForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import Post, Category, Writer

# Create your views here.

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = form.cleaned_data['group']
                group.user_set.add(user)
                username = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + username)

                return redirect('login')


	context = {'form':form}
	return render(request, 'blog/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('manage')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'blog/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('frontpage')

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

@login_required(login_url='login')
@allowed_users(allowed_roles=['writer'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['writer'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['writer'])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('manage')

    return render(request, 'blog/delete_post.html', {'post': post})

@login_required(login_url='login')
@allowed_users(allowed_roles=['writer'])

def manage(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    writer = User.objects.all()

    if request.user.is_authenticated:
        current_user = request.user
    else :
        current_user = None

    context = {
        'posts': posts,
        'categories': categories,
        'writer': writer,
        'current_user': current_user
    }

    return render(request, 'blog/manage.html', context=context)

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    return render(request, 'blog/category.html', {'category': category, 'posts': posts})


@login_required(login_url='login')
@allowed_users(allowed_roles=['writer'])
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

def profile(request):

    # writer = Writer.objects.get(id=pk)
    # form = WriterForm(instance=writer)

    if request.method == 'POST':
        form = WriterForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('frontpage')

    else:
        form = WriterForm(data=request.POST, files=request.FILES)

    context = {'form': form}

    return render(request, 'blog/profile.html', context)

