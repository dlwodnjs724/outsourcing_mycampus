from django.contrib import admin
from django.urls import path
from django.shortcuts import render

from .models import Category,Post,Image,Comment,Suggested


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
    ordering = ('-created_at', )

    def post_count(self, obj):
        return Post.objects.filter(ctgy=obj).count()

class SuggestedAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id', 'univ', 'name', 'suggested_at', 'suggested_by'
    )
    ordering = ('-suggested_at', )

    def get_urls(self):
        urls = super(SuggestedAdmin, self).get_urls()
        suggested_urls = [
            path('suggested', self.admin_site.admin_view(self.suggestion_confirm_view))
        ]
        return suggested_urls + urls
    
    def suggestion_confirm_view(self, request):
        ctx = dict(
            self.admin_site.each_context(request),
            s_ctgy = Suggested.objects.all(),
        )
        return render(request, "admin/suggestions.html", ctx)

    


class CommentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id', 'post', 'parent', 'content','author', 'created_at', 'is_anonymous', 'likes_count', 
    )

    def likes_count(self, obj):
        return obj.comment_likes.count()

admin.site.register(Category, CategoryAdmin)
admin.site.register(Suggested, SuggestedAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment, CommentAdmin)
