from django.urls import path, re_path
from . import views

app_name = "api"

urlpatterns = [
    path('mail/', views.send_mail, name="send_mail"),
    path('activate/', views.activate, name="activate"),
    path('like/', views.post_like, name='post_like'),
    path('bookmark/', views.post_bookmark, name='post_bookmark'),
    path('comment-like/', views.comment_like, name='comment_like'),
    path('report/', views.report_content, name='report_content')
]
