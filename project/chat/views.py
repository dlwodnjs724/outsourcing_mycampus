from django.shortcuts import render
from accounts.models import User

# Create your views here.

def index(request, url_name):
    return render(request, 'chat/index.html', {'users':User.objects.all(),  'url_name':url_name, 'univ':request.user.univ, 'other' : request.POST.get('other'), 'type' : request.POST.get('type'), 'match' : request.GET.get('match')})

def chat(request, url_name, username):
    user = User.objects.get(username=username)
    return render(request, 'chat/chat.html', {'partner':user, 'url_name':url_name, 'univ': request.user.univ })
