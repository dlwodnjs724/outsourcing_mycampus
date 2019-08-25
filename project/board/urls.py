from django.urls import path
from django.conf import settings
from board import views

app_name = 'board'

urlpatterns = [
    path("", views.main, name="main_board"),

    path('create/', views.post_create, name='post_create'),
    path('<str:category_name>/', views.category_board, name='category_board'),

    path('<str:category_name>/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<str:category_name>/<int:post_pk>/edit/', views.post_edit, name='post_edit'),
    path('<str:category_name>/<int:post_pk>/comment/', views.comment_create, name='comment_create'),
    path('<str:category_name>/<int:post_pk>/nested-comment/', views.comment_nest_create, name='comment_nest_create'),
    path('<str:category_name>/<int:post_pk>/report', views.report_send, name='report_send'),
]
