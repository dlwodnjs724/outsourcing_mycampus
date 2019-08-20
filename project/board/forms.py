from django import forms

from accounts.models import User
from .models import Univ, Category, Post, Comment, Suggested
from core.models import Univ


class UnivForm(forms.ModelForm):
    class Meta:
        model = Univ
        fields = ("full_name", "domain")


class CategoryForm(forms.ModelForm):
    univ = forms.ModelChoiceField(Univ.objects.all())

    class Meta:
        model = Category
        fields = ("name", "dscrp")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('ctgy', 'title', 'content', 'is_anonymous')
        labels = {
            'is_anonymous': 'anon'
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['ctgy'].queryset = Category.objects.filter(univ=self.request.user.univ)
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Please enter the title.',
        })
        self.fields['content'].widget.attrs.update({
            'placeholder': 'Please enter your contents.'
        })

    def save(self, commit=True):
        self.instance.author = self.request.user
        return super().save(commit=commit)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'is_anonymous')
        widgets = {
            'content': forms.Textarea
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.author = self.request.user
        return super().save(commit=commit)


class SuggestForm(forms.ModelForm):
    class Meta:
        model = Suggested
        fields = ('name', 'dscrp')
