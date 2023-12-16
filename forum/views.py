from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from .forms import CreatePostForm
from django.urls import reverse


def home(request):
    return render(request, "forum/index.html")


def category_posts(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    context = {"category": category, "posts": posts}
    return render(request, "forum/category_post.html", context=context)


def create_post(request, category_slug=None):
    current_category = Category.objects.get(slug=category_slug)
    form = CreatePostForm(category=current_category)
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form.instance.writer = request.user
            form.save()
            category_posts_url = reverse(
                "category-posts", kwargs={"category_slug": category_slug}
            )
            return redirect(category_posts_url)
    context = {"form": form}
    return render(request, "forum/posts/create_post.html", context=context)
