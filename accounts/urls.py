from django.urls import path
from . import views

# Password reset
from django.contrib.auth import views as auth_view

urlpatterns = [
    # User
    path("register", views.register, name="register"),
    path("user-login", views.user_login, name="user-login"),
    path("user-logout", views.user_logout, name="user-logout"),
    path("my-page", views.my_page, name="my-page"),
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
    # Password reset
    # 1) submit email & send password reset link
    path(
        "reset-password",
        auth_view.PasswordResetView.as_view(
            template_name="accounts/password/password-reset.html"
        ),
        name="reset_password",
    ),
    # 2) display success message for a password reset email was sent
    path(
        "reset-password-sent",
        auth_view.PasswordResetDoneView.as_view(
            template_name="accounts/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    # 3) password reset form link
    path(
        "reset/<uidb64>/<token>",
        auth_view.PasswordResetConfirmView.as_view(
            template_name="accounts/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    # 4) display success message for a password reset was successfully done
    path(
        "reset-password-complete",
        auth_view.PasswordResetCompleteView.as_view(
            template_name="accounts/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
]
