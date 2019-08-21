from django.shortcuts import render
from accounts.models import User

# Create your views here.

def index(request, url_name):
    return render(request, 'chat/index.html', {'users':User.objects.all()})

def chat(request, url_name, user_name):
    user = User.objects.get(username=user_name)
    return render(request, 'chat/chat.html', {'partner':user})