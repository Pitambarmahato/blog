from django.db import connection
from django.db.models import F
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import PostForm, CommentForm
from .models import Category, Post, Comment, Like

# Create your views here.
def index(request):
    keywords = request.POST.get('search')
   
    if keywords:
        posts = Post.objects.filter(title__icontains=keywords)
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    # title = request.session.get('post_title')
    # print("this is session: ", request.session.get('post_title'))
    categories = Category.objects.all()
    print(categories.query)
    paginator = Paginator(posts, 10)
    page_number  = request.GET.get('page')
    post_pages = paginator.get_page(page_number)
    # print(connection.queries)

    context = {
        'posts':post_pages,
        'categories':categories
    }
    return render(request, 'posts/index.html', context=context)

def post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        user = request.user
        if form.is_valid():
            post = Post(title = form.cleaned_data['title'], 
                    category=form.cleaned_data['category'], 
                    description = form.cleaned_data['description'], user=user)
            post.save()
            return redirect('index')
    context = {
        'form':form
    }
    return render(request, 'posts/create.html', context=context)

def get_post(request, pk):
    user = request.user
    print(user.id)
    if user.is_authenticated:
        post = Post.objects.get(id=pk)
        # request.session['post_id'] = post.id
        # request.session['post_title'] = post.title
        if not user == post.user:
            Post.objects.filter(id=pk).update(views=F('views')+1)
    posts = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id = pk)
    form = CommentForm()
    likes = Like.objects.filter(user = user.id, post_id = pk)
    # if likes:
    #     print("Hes")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            comment = Comment(user=request.user, post = posts, comment = form.cleaned_data['comment'])
            print(comment)
            comment.save()
            comments = Comment.objects.filter(post_id = pk).values()
            comment_list = list(comments)
            return JsonResponse({'status':'Save', 'comments':comment_list})
        else:
            return JsonResponse({'status':'Not Saved'})
    context = {
        'post': posts,
        'form': form,
        'comments':comments,
        'liked': likes
    }
    return render(request, 'posts/post.html', context = context)

def update_post(request, pk):
    post = Post.objects.get(id = pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('post_detail', kwargs={'pk':pk}))
    context ={
        'form':form,
        'user':post.user
    }
    return render(request, 'posts/update.html', context=context)
        
def delete_post(request, pk):
    post = Post.objects.get(id=pk).delete()
    return redirect('index')

def filter_post(request, pk):
    keywords = request.POST.get('search')
    if keywords:
        posts = Post.objects.filter(category_id = pk).filter(title__icontains=keywords)
    else:
        posts = Post.objects.filter(category_id = pk).order_by('-created_at')
        # category = Category.objects.filter(id=pk).get()
        # post = category.category_set()
        print(post)
    categories = Category.objects.all()
    paginator = Paginator(posts, 10)
    page_number  = request.GET.get('page')
    post_pages = paginator.get_page(page_number)
    context = {'posts':post_pages, 'categories':categories}
    return render(request, 'posts/index.html', context = context)


def post_like(request, pk):
    user = request.user
    # post_id = pk

    post = Post.objects.get(id=pk)
    like = Like.objects.filter(user = user, post_id = pk)
    liked = True if like else False

    if liked:
        Like.dislike(post, user)
        liked = False
    else:
        Like.liked(post, user)
        liked = True

    resp = {'like':liked}
    return JsonResponse(resp)
