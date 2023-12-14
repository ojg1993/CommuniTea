from django.shortcuts import render, get_object_or_404
from .models import Category, Post

def home(request):
    return render(request, "forum/index.html")

def category_posts(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    context = {'category':category, 'posts':posts}
    return render(request, 'forum/category_post.html', context=context)