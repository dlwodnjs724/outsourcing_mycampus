from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import login, logout, signup, check_mail, mypage, policy, guideline

app_name = "accounts"


urlpatterns = [
    path('mypage/', mypage, name="mypage"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('check-mail/', check_mail),

    path('policy/', policy, name='policy'),
    path('guideline/', guideline, name='guideline'),
]