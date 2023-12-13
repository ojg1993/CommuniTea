from django.shortcuts import render, redirect
from . import forms

# login
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

def register(request):
    form = forms.RegisterUserForm()
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            return redirect('home')

    context = {'form':form}
    return render(request, "accounts/registration/register.html", context=context)

def user_login(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email,":", password)
            user = authenticate(request, email=email, password=password)
            print("user:", user)

            if user is not None:
                auth.login(request, user)
                print("login success")
                return redirect('home')
            else:
                print("login failed")
    context = {'form':form}
    return render(request, "accounts/login.html", context=context)

def logout(request):
    pass
