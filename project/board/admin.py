from django.contrib import admin
from .models import Category,Post,Image,Comment


class PostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id', 'title', 'ctgy', 'user', 'created_at',
        'likes_count','views', 'is_anonymous'
    )
    search_fields = ('title',)
    ordering = ('-created_at', 'ctgy')

    def likes_count(self, obj):
        return obj.likes.count()

class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id', 'univ', 'name', 'created_at', 'status', 'post_count'
    )
    search_fields = ('name', 'univ', 'status')
    ordering = ('created_at', )

    def post_count(self, obj):
        return Post.objects.filter(ctgy=obj).count()

class CommentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id', 'post', 'parent', 'content','author', 'created_at', 'is_anonymous', 'likes_count', 
    )

    def likes_count(self, obj):
        return obj.comment_likes.count()

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment, CommentAdmin)
