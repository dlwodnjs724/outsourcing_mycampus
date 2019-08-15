from django.contrib import admin
from .models import Univ, Category, Post, Image,Comment
# Register your models here.
admin.site.register(Univ)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)