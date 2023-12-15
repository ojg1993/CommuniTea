from django.shortcuts import render, redirect
from . import forms

# login
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate


def register(request):
    form = forms.RegisterUserForm()
    if request.method == "POST":
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            return redirect("home")

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
