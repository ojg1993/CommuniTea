from django import forms
from .models import CustomUser

# User register modules
from django.contrib.auth.forms import UserCreationForm

# User login modules
from django.contrib.auth.forms import AuthenticationForm

from django.forms.widgets import PasswordInput, EmailInput


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "password1", "password2"]


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput())
