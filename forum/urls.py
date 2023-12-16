from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "category-posts/<slug:category_slug>",
        views.category_posts,
        name="category-posts",
    ),
    path(
        "category-posts/<slug:category_slug>/create-post",
        views.create_post,
        name="create-post",
    ),
    path("category-posts/read-post/<int:post_id>", views.read_post, name="read-post"),
]
