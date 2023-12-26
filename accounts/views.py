from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from forum.models import Post, Comment
from . import forms
from .models import CustomUser

# User info change / deletion
from django.contrib.auth import update_session_auth_hash, logout
from .forms import PasswordConfirmationForm

# Login
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

# My page pagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Email verification
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Message
from django.contrib import messages


def register(request):
    form = forms.RegisterUserForm()
    if request.method == "POST":
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
            link = f"{request.scheme}://{current_site.domain}"

            subject = "Account verification email for CommuniTea"
            message = render_to_string(
                "accounts/registration/email-verification.html",
                {
                    "user": user,
                    "link": link,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return redirect("email-verification-sent")

    context = {"form": form}
    return render(request, "accounts/registration/register.html", context=context)


@login_required(login_url="user-login")
def update_user(request):
    form = forms.RegisterUserForm(instance=request.user)

    if request.method == "POST":
        form = forms.RegisterUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.info(request, "You have successfully deleted your account")
            return redirect("my-page")

    context = {"form": form}
    return render(request, "accounts/registration/update-user.html", context=context)


@login_required(login_url="user-login")
def delete_user(request):
    form = PasswordConfirmationForm()
    if request.method == "POST":
        password = request.POST.get("password")
        if request.user.check_password(password):
            request.user.delete()
            logout(request)
            messages.error(request, "You have successfully deleted your account")
            return redirect("home")
        else:
            pass
    return render(request, "accounts/registration/delete-user.html", {"form": form})


def user_login(request):
    form = forms.LoginForm()

    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Login success")
                    return redirect("home")
                else:
                    messages.info(request, "Please verify your email first")
            else:
                messages.error(request, "Invalid email or password")
    context = {"form": form}
    return render(request, "accounts/login.html", context=context)


@login_required(login_url="user-login")
def user_logout(request):
    auth.logout(request)
    messages.error(request, "Logout success")
    return redirect("home")


@login_required(login_url="user-login")
def my_page(request):
    user = request.user
    posts = Post.objects.filter(writer=user).order_by("-created_at")
    comments = Comment.objects.filter(commenter=user).order_by("-created_at")

    # Posts pagination
    posts_paginated = Paginator(posts, 10)
    posts_page_number = request.GET.get("page")
    try:
        posts_current_page = posts_paginated.page(posts_page_number)
    except PageNotAnInteger:
        posts_current_page = posts_paginated.page(1)
    except EmptyPage:
        posts_current_page = posts_paginated.page(posts_paginated.num_pages)

    # Comments pagination
    comments_paginated = Paginator(comments, 10)
    comments_page_number = request.GET.get("page")
    try:
        comments_current_page = comments_paginated.page(comments_page_number)
    except PageNotAnInteger:
        comments_current_page = comments_paginated.page(1)
    except EmptyPage:
        comments_current_page = comments_paginated.page(comments_paginated.num_pages)

    # pagination navigator
    page_numbers_range = 10
    if len(posts_paginated.page_range) > len(comments_paginated.page_range):
        max_index = len(posts_paginated.page_range)
        start_index = (
            int((posts_current_page.number - 1) / page_numbers_range)
            * page_numbers_range
        )
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            comments_end_index = max_index

        page_range = comments_paginated.page_range[start_index:comments_end_index]

    else:
        max_index = len(comments_paginated.page_range)
        start_index = (
            int((comments_current_page.number - 1) / page_numbers_range)
            * page_numbers_range
        )
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            comments_end_index = max_index

        page_range = comments_paginated.page_range[start_index:comments_end_index]

    context = {
        "post_page": posts_current_page,
        "comments_page": comments_current_page,
        "page_range": page_range,
    }

    return render(request, "accounts/mypage.html", context=context)


def email_verification(request, uid64, token):
    unique_id = force_str(urlsafe_base64_decode(uid64))
    user = CustomUser.objects.get(pk=unique_id)

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("email-verification-success")
    else:
        return redirect("email-verification-failed")


def email_verification_sent(request):
    return render(request, "accounts/registration/email-verification-sent.html")


def email_verification_success(request):
    return render(request, "accounts/registration/email-verification-success.html")


def email_verification_failed(request):
    return render(request, "accounts/registration/email-verification-failed.html")
