from django.shortcuts import render
from accounts.models import User

# Create your views here.

def index(request, url_name):
    request.GET.get('target')
    return render(request, 'chat/index.html', {'users':User.objects.all(), 'univ':request.user.univ, 'other' : request.GET.get('other'), 'type' : request.GET.get('type')})

def chat(request, url_name, username):
    user = User.objects.get(username=username)
    return render(request, 'chat/chat.html', {'partner':user})






