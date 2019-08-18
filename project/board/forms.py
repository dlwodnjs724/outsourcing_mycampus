from django import forms
from .models import Univ, Category, Post, Comment
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
        fields = ("title", "content")


class CommentForm(forms.ModelForm):
    post = forms.ModelChoiceField(Post.objects.all())

    class Meta:
        model = Comment
        fields = ("content",)
