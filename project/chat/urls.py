from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index),
    path('<str:user_name>/', views.chat),
]
