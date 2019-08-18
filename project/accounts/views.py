from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponse
from django.shortcuts import render
User = get_user_model()
# Create your views here.


def redirect404(request):
    raise Http404('There is no matching url')


def check_mail(request):
    return render(request, "accounts/mail.html")


def signup(request):
    email = request.GET.get('email')

    return render(request, "accounts/signup.html", {"email": email})
