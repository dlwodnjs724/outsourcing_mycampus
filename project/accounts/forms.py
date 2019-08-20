from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'gender', 'class_of', 'terms_acceptance']


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']