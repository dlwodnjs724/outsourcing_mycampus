from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name="index"),
=======
    path('', views.index),
>>>>>>> parent of 20ddaf7... Merge pull request #57 from dlwodnjs724/front/mypage_mobile
    path('<str:username>/', views.chat),
]
