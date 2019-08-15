from django.contrib import admin
from .models import Category,Post,Image,Comment

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)