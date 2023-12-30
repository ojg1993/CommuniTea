from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect

# Model & ModelForm
from .models import Category, Post, Comment, Emotion
from .forms import CreatePostForm, CreateCommentForm
from django.urls import reverse

# Pagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Message
from django.contrib import messages


def home(request):
    latest_posts = Post.objects.all().order_by("-created_at")[:10]
    context = {"latest_posts": latest_posts}
    return render(request, "forum/index.html", context=context)


def search_post(request):
    search_keyword = request.GET.get('query', '')
    if len(search_keyword) < 2:
        messages.warning(request, 'Input 2 or more characters to search posts.')
        return redirect('home')
    else:
        searched_posts = (Post.objects
                          .filter(Q(title__icontains=search_keyword) |
                                  Q(content__icontains=search_keyword) |
                                  Q(writer__email__icontains=search_keyword))
                          .order_by("-id"))

        if searched_posts.exists():
            paginated = Paginator(searched_posts, 12)
            page_number = request.GET.get("page")

            try:
                current_page = paginated.page(page_number)

            except PageNotAnInteger:
                current_page = paginated.page(1)

            except EmptyPage:
                current_page = paginated.page(paginated.num_pages)

            page_numbers_range = 10
            max_index = len(paginated.page_range)

            start_index = (
                    int((current_page.number - 1) / page_numbers_range) * page_numbers_range
            )
            end_index = start_index + page_numbers_range
            if end_index >= max_index:
                end_index = max_index

            page_range = paginated.page_range[start_index:end_index]

            current_url_params = request.GET.copy()
            current_url_params.pop('page', None)
            current_url_params['query'] = search_keyword
            context = {
                "page": current_page,
                "page_range": page_range,
                "current_url_params": current_url_params.urlencode(),
            }
            return render(request, "forum/posts/search-post.html", context=context)
        else:
            messages.warning(request, 'No posts found with the given search criteria.')
            return redirect('home')


def category_posts(request, category_slug=None):
    # Categorised posts
    if category_slug not in ["all-post", "best"]:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category).order_by("-id")

    # Not categorised posts
    else:
        if category_slug == "all-post":
            category = "all-post"
            posts = Post.objects.all().order_by("-id")
        elif category_slug == "best":
            category = "best"
            posts = Post.objects.annotate(
                like_count=Count("post_emotion", filter=Q(post_emotion__like=True))
            ).order_by("-like_count", "-hits", "-id")[:48]

    # Pagination
    paginated = Paginator(posts, 12)
    page_number = request.GET.get("page")

    # Get current page
    try:
        current_page = paginated.page(page_number)

    # If page is not an integer, deliver first page.
    except PageNotAnInteger:
        current_page = paginated.page(1)

    # If page is out of range, deliver last page of results.
    except EmptyPage:
        current_page = paginated.page(paginated.num_pages)

    # Range of pages limiting logic
    page_numbers_range = 10
    max_index = len(paginated.page_range)

    start_index = (
            int((current_page.number - 1) / page_numbers_range) * page_numbers_range
    )
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
        end_index = max_index

    page_range = paginated.page_range[start_index:end_index]

    context = {
        "category": category,
        "page": current_page,
        "page_range": page_range,
    }
    return render(request, "forum/category-posts.html", context=context)


def post_info(request, category_slug=None, post_id=None):
    cur_category = Category.objects.get(slug=category_slug)
    post = get_object_or_404(Post, id=post_id)

    time_diff = post.modified_at - post.created_at
    time_difference_seconds = time_diff.total_seconds()

    if time_difference_seconds > 1:
        post_edited = True
    else:
        post_edited = False


    comments = Comment.objects.filter(post_id=post_id).order_by("-created_at")

    paginated = Paginator(comments, 7)
    page_number = request.GET.get("page")

    try:
        current_page = paginated.page(page_number)
    except PageNotAnInteger:
        current_page = paginated.page(1)
    except EmptyPage:
        current_page = paginated.page(paginated.num_pages)

    # Range of pages limiting logic
    page_numbers_range = 5
    max_index = len(paginated.page_range)

    start_index = (
        int((current_page.number - 1) / page_numbers_range) * page_numbers_range
    )
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
        end_index = max_index

    page_range = paginated.page_range[start_index:end_index]

    form = CreateCommentForm()

    if request.user.is_authenticated:
        user_vote_info = {
            "has_liked": post.has_user_liked(expresser=request.user, post=post),
            "has_disliked": post.has_user_disliked(expresser=request.user, post=post),
        }
    else:
        user_vote_info = {"has_liked": False, "has_disliked": False}

    context = {
        "post": post,
        "post_edited": post_edited,
        "category_slug": category_slug,
        "form": form,
        "comment_page": current_page,
        "page_range": page_range,
        "user_vote_info": user_vote_info,
    }
    if Post.objects.filter(category=cur_category.id, id__lt=post_id):
        context["has_previous_post"] = True
    if Post.objects.filter(category=cur_category.id, id__gt=post_id):
        context["has_next_post"] = True
    post.increase_hits()
    return render(request, "forum/posts/post-info.html", context=context)


@login_required(login_url="user-login")
def create_post(request, category_slug=None):
    current_category = Category.objects.get(slug=category_slug)
    form = CreatePostForm(category=current_category)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.writer = request.user
            form.save()
            category_posts_url = reverse(
                "category-posts", kwargs={"category_slug": category_slug}
            )
            messages.info(request, "Post uploaded successfully")
            return redirect(category_posts_url)
    context = {"form": form}
    return render(request, "forum/posts/create-post.html", context=context)


@login_required(login_url="user-login")
def update_post(request, post_id=None, category_slug=None):
    cur_post = Post.objects.get(id=post_id)
    form = CreatePostForm(instance=cur_post)

    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=cur_post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.save()
            post_info_url = reverse(
                "post-info",
                kwargs={"category_slug": edited_post.category.slug, "post_id": post_id},
            )
            messages.info(request, "Post updated successfully")

            return redirect(post_info_url)

    context = {"form": form, "category_slug": category_slug}
    return render(request, "forum/posts/update-post.html", context=context)


@login_required(login_url="user-login")
def delete_post(request, post_id=None, category_slug=None):
    cur_post = Post.objects.get(id=post_id)
    cur_post.delete()
    messages.warning(request, "Post deleted successfully")
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


@login_required(login_url="user-login")
def create_comment(request, post_id, category_slug):
    comment_form = CreateCommentForm(request.POST)
    post = get_object_or_404(Post, id=post_id)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.commenter = request.user
        comment.save()
        messages.info(request, "Comment added successfully")
        return redirect("post-info", category_slug=category_slug, post_id=post_id)


@login_required(login_url="user-login")
def update_comment(request, comment_id, post_id, category_slug):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        form = CreateCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.info(request, "Comment updated successfully")
            return redirect("post-info", category_slug=category_slug, post_id=post_id)

    form = CreateCommentForm(instance=comment)
    context = {"form": form, "comment": comment}

    return render(request, "forum/posts/update-comment.html", context=context)


@login_required(login_url="user-login")
def delete_comment(request, comment_id, post_id, category_slug):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    messages.warning(request, "Comment deleted successfully")
    return redirect("post-info", category_slug=category_slug, post_id=post_id)


@login_required(login_url="user-login")
def emotion(request, post_id, category_slug, like):
    post = get_object_or_404(Post, id=post_id)
    emotion, created = Emotion.objects.get_or_create(post=post, expresser=request.user)
    if not created:
        if like:
            if emotion.dislike:
                emotion.dislike = False
                emotion.like = True
                emotion.save()
            else:
                emotion.delete()
        else:
            if emotion.like:
                emotion.like = False
                emotion.dislike = True
                emotion.save()

            else:
                emotion.delete()

    else:
        if like:
            emotion.like = True
        else:
            emotion.dislike = True
        emotion.save()

    return redirect("post-info", category_slug=category_slug, post_id=post_id)
