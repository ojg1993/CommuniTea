# RESTful API
from django.shortcuts import render, get_object_or_404, redirect

# Model & ModelForm
from .models import Category, Post
from .forms import CreatePostForm
from django.urls import reverse

# Pagination
from django.core.paginator import Paginator


def home(request):
    latest_posts = Post.objects.all().order_by("-created_at")[:7]
    context = {"latest_posts": latest_posts}
    return render(request, "forum/index.html", context=context)


def category_posts(request, category_slug=None):
    # Categorised posts
    if category_slug not in ["all-post", "best"]:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category)

    # Not categorised posts
    else:
        if category_slug == "all-post":
            category = "all-post"
            posts = Post.objects.all()
        elif category_slug == "best":
            category = "best"
            # best posts logic
            posts = Post.objects.all().order_by("-hits")[:45]

    # pagination
    paginated = Paginator(posts, 10)
    page_number = request.GET.get("page")
    current_page_number = paginated.get_page(page_number)

    context = {"category": category, "posts": posts, "page": current_page_number}
    return render(request, "forum/category-posts.html", context=context)


def post_info(request, category_slug=None, post_id=None):
    cur_category = Category.objects.get(slug=category_slug)
    post = get_object_or_404(Post, id=post_id)
    context = {"post": post, "category_slug": category_slug}
    if Post.objects.filter(category=cur_category.id, id__lt=post_id):
        context["has_previous_post"] = True
    if Post.objects.filter(category=cur_category.id, id__gt=post_id):
        context["has_next_post"] = True
    post.increase_hits()
    return render(request, "forum/posts/post-info.html", context=context)


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
    return render(request, "forum/posts/create-post.html", context=context)


def update_post(request, post_id=None, category_slug=None):
    cur_post = Post.objects.get(id=post_id)
    form = CreatePostForm(instance=cur_post)

    if request.method == "POST":
        form = CreatePostForm(request.POST, instance=cur_post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.save()
            post_info_url = reverse(
                "post-info",
                kwargs={"category_slug": edited_post.category.slug, "post_id": post_id},
            )
            return redirect(post_info_url)

    context = {"form": form, "category_slug": category_slug}
    return render(request, "forum/posts/update-post.html", context=context)


def delete_post(request, post_id=None, category_slug=None):
    cur_post = Post.objects.get(id=post_id)
    cur_post.delete()
    return redirect("category-posts", category_slug=category_slug)


def previous_post(request, category_slug=None, post_id=None):
    cur_category = Category.objects.get(slug=category_slug)
    previous_post = (
        Post.objects.filter(category=cur_category.id, id__lt=post_id)
        .order_by("-id")
        .first()
    )
    return redirect("post-info", category_slug=category_slug, post_id=previous_post.id)


def next_post(request, category_slug=None, post_id=None):
    cur_category = Category.objects.get(slug=category_slug)
    previous_post = (
        Post.objects.filter(category=cur_category.id, id__gt=post_id)
        .order_by("id")
        .first()
    )
    return redirect("post-info", category_slug=category_slug, post_id=previous_post.id)
