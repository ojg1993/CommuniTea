from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # main page
    path("", include("forum.urls")),
    # accounts app
    path("accounts/", include("accounts.urls")),
]
