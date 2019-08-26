from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index, name='chat'),
    path('<str:username>/', views.chat),
]
