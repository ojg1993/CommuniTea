from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search", views.search_post, name="search"),
    # Post CRUD
    path("<slug:category_slug>/create-post", views.create_post, name="create-post"),
    path("<slug:category_slug>/posts", views.category_posts, name="category-posts"),
    path("<slug:category_slug>/posts/<int:post_id>", views.post_info, name="post-info"),
    path(
        "<slug:category_slug>/posts/<int:post_id>/update-post",
        views.update_post,
        name="update-post",
    ),
    path(
        "<slug:category_slug>/posts/<int:post_id>/delete-post",
        views.delete_post,
        name="delete-post",
    ),
    # Post navigation
    path(
        "<slug:category_slug>/posts/<int:post_id>/previous-post",
        views.previous_post,
        name="previous-post",
    ),
    path(
        "<slug:category_slug>/posts/<int:post_id>/next-post",
        views.next_post,
        name="next-post",
    ),
    # Comment CRUD
    path(
        "<slug:category_slug>/posts/<int:post_id>/create-comment",
        views.create_comment,
        name="create-comment",
    ),
    path(
        "<slug:category_slug>/posts/<int:post_id>/comments/<int:comment_id>/update-comment",
        views.update_comment,
        name="update-comment",
    ),
    path(
        "<slug:category_slug>/posts/<int:post_id>/delete-comment/<int:comment_id>",
        views.delete_comment,
        name="delete-comment",
    ),
    # Emotions
    path(
        "<slug:category_slug>/posts/<int:post_id>/<int:like>",
        views.emotion,
        name="emotion",
    ),
]
