from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "<slug:category_slug>/posts",
        views.category_posts,
        name="category-posts",
    ),
    path(
        "<slug:category_slug>/create-post",
        views.create_post,
        name="create-post",
    ),
    path("<slug:category_slug>/posts/<int:post_id>", views.post_info, name="post-info"),
    path("<slug:category_slug>/posts/<int:post_id>/update-post", views.update_post, name="update-post"),
    path("<slug:category_slug>/posts/<int:post_id>/delete-post", views.delete_post, name="delete-post"),
    path("<slug:category_slug>/posts/<int:post_id>/previous-post", views.previous_post, name="previous-post"),
    path("<slug:category_slug>/posts/<int:post_id>/next-post", views.next_post, name="next-post"),
]
