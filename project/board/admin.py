from django.contrib import admin
from .models import Category,Post,Image,Comment


class PostAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id', 'title', 'ctgy', 'user', 'created_at',
        'likes_count','views', 'is_anonymous'
    )
    list_filter = ('ctgy',)
    search_fields = ('title',)
    ordering = ('-created_at', 'ctgy')

    def likes_count(self, obj):
        return obj.likes.count()

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment)
