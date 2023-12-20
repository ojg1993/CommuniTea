from django.urls import path
from . import views

urlpatterns = [
    # Register
    path("register", views.register, name="register"),
    # User login/out
    path("user-login", views.user_login, name="user-login"),
    path("user-logout", views.user_logout, name="user-logout"),
    # Email verification
    path(
        "email-verification/<str:uid64>/<str:token>",
        views.email_verification,
        name="email-verification",
    ),
    path(
        "email-verification-sent",
        views.email_verification_sent,
        name="email-verification-sent",
    ),
    path(
        "email-verification-sucess",
        views.email_verification_success,
        name="email-verification-success",
    ),
    path(
        "email-verification-failed",
        views.email_verification_failed,
        name="email-verification-failed",
    ),
]
