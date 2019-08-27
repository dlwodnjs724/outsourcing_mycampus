from django.urls import path, re_path
from . import views

app_name = "api"

urlpatterns = [
    path('mail/', views.send_mail, name="send_mail"),
    path('activate/', views.activate, name="activate")
]
