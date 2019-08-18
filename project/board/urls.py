from django.urls import path
from django.conf import settings
from board import views

app_name = 'board'

urlpatterns = [
    path('', views.main_board, name='main_board'),
    path('<str:category_name>/', views.category_board, name='category_board'),
    path('<str:category_name>/<int:post_pk>', views.post_detail, name='post_detail'),
    # path('<str:category>/<int:pk>/new', views.create_Comment, name="create_Comment"),
    # path('<str:category>/<int:pk>/', views.read_Post, name="read_Post"),
    # path('<str:category>/', views.read_Board, name="read_Board"),
]
