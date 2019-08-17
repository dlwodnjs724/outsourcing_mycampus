from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View


def redirect404(request):
    raise Http404('There is no matching url')

def check_mail(request):
    return render(request, "accounts/mail.html")