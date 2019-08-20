from django.urls import path
from django.conf import settings
from board import views

app_name = 'board'

urlpatterns = [
    path('', views.main_board, name='main_board'),
    path('new/', views.main_board_new, name='main_board_new'),
    path('create/', views.post_create, name='post_create'),
    path('like/', views.post_like, name='post_like'),
    path('bookmark/', views.post_bookmark, name='post_bookmark'),
    path('<str:category_name>/', views.category_board, name='category_board'),
    path('<str:category_name>/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<str:category_name>/<int:post_pk>/edit/', views.post_edit, name='post_edit'),
    path('<str:category_name>/<int:post_pk>/new/', views.comment_new, name='comment_new'),
    path('<str:category_name>/<int:post_pk>/like/', views.comment_like, name='comment_like'),
    # path('<str:category>/new/', views.create_Comment, name="create_Comment"),
    # path('<str:category>/<int:pk>/', views.read_Post, name="read_Post"),
    # path('<str:category>/', views.read_Board, name="read_Board"),
]
