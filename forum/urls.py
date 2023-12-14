from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category-posts/<slug:category_slug>", views.category_posts, name="category-posts")
]
