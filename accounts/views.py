from django.shortcuts import render, redirect
from . import forms
from .models import CustomUser

# Login
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

# Email verification
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


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


def user_login(request):
    form = forms.LoginForm()
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)
            print(email, password)

            if user is not None:
                auth.login(request, user)
                return redirect("home")
            else:
                print("login failed")
    context = {"form": form}
    return render(request, "accounts/login.html", context=context)


def user_logout(request):
    auth.logout(request)
    return redirect("home")


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
