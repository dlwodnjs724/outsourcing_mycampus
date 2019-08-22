from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })
        self.fields['class_of'].widget.attrs.update({
            'placeholder': 'ex) 2022'
        })

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'gender', 'class_of', 'terms_acceptance']


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']