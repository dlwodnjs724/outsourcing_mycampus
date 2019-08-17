from django.urls import path
from django.conf import settings
from board import views

urlpatterns = [
    path('', views.main_board, name='main_board'),
    # path('<str:category>/', views.univ, name='category_board'),
    # path('<str:category>/new', views.create_Post, name="create_Post"),
    # path('<str:category>/<int:pk>/new', views.create_Comment, name="create_Comment"),
    # path('<str:category>/<int:pk>/', views.read_Post, name="read_Post"),
    # path('<str:category>/', views.read_Board, name="read_Board"),
]
