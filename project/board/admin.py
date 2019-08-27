from django.contrib import admin
from django.contrib import messages
from .models import Category, Post, Image, Comment, Suggested, Report
from core.models import Univ
# from django.urls import path
# from django.shortcuts import render, redirect,get_object_or_404


class PostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id', 'title', 'ctgy', 'author', 'created_at',
        'likes_count', 'views', 'is_anonymous'
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
    ordering = ('-created_at',)

    def post_count(self, obj):
        return Post.objects.filter(ctgy=obj).count()


class SuggestedAdmin(admin.ModelAdmin):
    actions = ['suggestion_approve_view']
    list_per_page = 20
    list_display = (
        'id', 'univ', 'name', 'suggested_at', 'suggested_by'
    )
    ordering = ('-suggested_at',)

    def suggestion_approve_view(self, request, queryset):
        c = 0
        for q in queryset:
            instance = Category(
                univ = q.univ,
                name = q.name,
                dscrp = q.dscrp,
            )
            exist = Category.objects.filter(univ=q.univ).values_list('name', flat=True)
            if q.name in exist:
                messages.error(request, f'『{ q.name }』 already exist at 『{ q.univ.full_name }』')
            else:
                instance.save()
                q.delete()
                c += 1
        if c > 0:        
            messages.success(request, f'{ c } suggestion(s) successfully approved!!!!!!!!!!!!!!!!!!!!!!!!!!')
    suggestion_approve_view.short_description = "approve suggestions"

    # def get_urls(self):
    #     urls = super(SuggestedAdmin, self).get_urls()
    #     suggested_urls = [
    #         path('suggested', self.admin_site.admin_view(self.suggestion_confirm_view)),
    #         path('suggested/<int:pk>/', self.admin_site.admin_view(self.suggestion_detail_view), name="s_detail"),
    #         # path('suggested/<int:pk>/edit', self.admin_site.admin_view(self.suggestion_edit_view), name="s_edit"),
    #         # path('suggested/<int:pk>/delete', self.admin_site.admin_view(self.suggestion_delete_view), name="s_delete"),

    #     ]
    #     return suggested_urls + urls

    # def suggestion_confirm_view(self, request):
    #     ctx = dict(
    #         self.admin_site.each_context(request),
    #         s_ctgy=Suggested.objects.all(),
    #     )
    #     return render(request, "admin/suggestions.html", ctx)

    # def suggestion_detail_view(self, request, pk):
    #     suggested = get_object_or_404(Suggested, pk=pk)
    #     univ = suggested.univ
    #     dscrp = suggested.dscrp
    #     ctx = {
    #         'suggested': suggested,
    #         'univ': univ,
    #         'dscrp': dscrp,
    #     }
    #     ctx2 = dict(
    #         self.admin_site.each_context(request),
    #         s_ctgy=Suggested.objects.all(),
    #     )
        # print("hello ><")
        # print(request.content_type)
        # exist = Category.objects.filter(univ=univ).values_list('name', flat=True)

        # if request.method =='POST':
        #     instance = Category(
        #     univ = suggested.univ,
        #     name = suggested.name,
        #     dscrp = suggested.dscrp,
        #     )
        #     print(request.body)
        #     if suggested.name in exist:
        #         ctx['message'] = 'already exist in this Univ'
        #         return render(request, "admin/suggestions_detail.html", ctx)
        #     instance.save()
        #     suggested.delete()
        #     ctx['message'] = 'Create New Category, Delete Suggestion'
        #     return render(request, "admin/suggestions.html", ctx2)
        
        # return render(request, "admin/suggestions_detail.html", ctx)

    # def suggestion_edit_view(self, request, pk):
    #     suggested = get_object_or_404(Suggested, pk=pk)
    #     univ = suggested.univ
    #     dscrp = suggested.dscrp
    #     ctx = {
    #         'suggested': suggested,
    #         'univ': univ,
    #         'dscrp': dscrp,
    #     }
    #     if request.method == 'POST':
    #         form = SuggestForm(request.POST, instance=suggested)
    #         if form.is_valid():
    #             suggested = form.save()
    #             return redirect('/admin/board/suggested/', ctx)
    #     else:
    #         form = SuggestForm(instance=suggested)
    #     return render(request, 'admin/suggestions_edit.html', {
    #         'pk':pk,
    #         'suggested': suggested,
    #         'form': form,
    #         })

    # def suggestion_delete_view(self, request, pk, queryset):
    #     suggested = get_object_or_404(Suggested, pk=pk)
    #     ctx = dict(
    #         self.admin_site.each_context(request),
    #         s_ctgy=Suggested.objects.all(),
    #     )
    #     suggested.delete()
    #     return redirect('/admin/board/suggested/')


class CommentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id', 'post', 'parent', 'content', 'author', 'created_at', 'is_anonymous', 'likes_count',
    )

    def likes_count(self, obj):
        return obj.comment_likes.count()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Suggested, SuggestedAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Report)