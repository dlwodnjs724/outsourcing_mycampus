from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'gender', 'class_of', 'terms_acceptance']


class LoginForm(forms.ModelForm):

    model = get_user_model()
    fields = ['username', 'password']