from django.shortcuts import render

# Create your views here.

def chat(request, url_name):
    return render(request, 'chat/chat.html')