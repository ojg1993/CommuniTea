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
]
