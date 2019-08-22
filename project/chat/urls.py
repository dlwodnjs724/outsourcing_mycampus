from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index),
    path('<str:username>/', views.chat),
]
