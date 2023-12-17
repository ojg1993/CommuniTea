from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from .forms import CreatePostForm
from django.urls import reverse


def home(request):
    latest_posts = Post.objects.all().order_by("-created_at")[:7]
    context = {"latest_posts": latest_posts}
    return render(request, "forum/index.html", context=context)


def category_posts(request, category_slug=None):
    if category_slug not in ['all_post', 'best']:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category)
    else:
        if category_slug == 'all_post':
            category = None
            posts = Post.objects.all()
        elif category_slug == 'best':
            category = None
            # best posts logic
            posts = Post.objects.all().order_by("created_at")[:50]

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


def read_post(request, post_id=None):
    post = get_object_or_404(Post, id=post_id)
    context = {"post": post}
    post.increase_hits()
    return render(request, "forum/posts/read_post.html", context=context)
