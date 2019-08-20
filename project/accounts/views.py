from django.contrib import auth
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from api.models import Token
from accounts.forms import SignupForm, LoginForm
from django.urls import reverse

from core.models import Univ

User = get_user_model()


# Create your views here.

def login(request, url_name):
    univ = Univ.objects.get(url_name=url_name)

    if not request.user.is_anonymous:
        return redirect("core:board:main_board", url_name=request.user.univ.url_name)

    ctx = {"univ" : univ}
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('core:board:main_board', url_name=url_name)
        else:
            ctx["error"] = "Login failed"

    return render(request, 'registration/login.html', ctx)


@login_required
def logout(request, url_name):
    auth.logout(request)
    return redirect('main')


def check_mail(request, url_name):
    return render(request, "accounts/mail.html")


# activate 에서 넘겨줌

def signup(request, url_name):
    try:
        email = request.GET.get('email')
        token = Token.objects.get(target_email=email)
        univ = Univ.objects.get(url_name=url_name)  # 이 부분, 파라미터 받는 걸로 수정 필요

        form = SignupForm(request.POST or None)
        if request.method == "GET":

            if not email:
                raise Exception("The wrong approach.")

            # email이 Token 인증 받은 이메일인지 체크
            if not token.is_accepted:
                raise Exception("Not a valid token")

            # 이미 가입한 이메일인지 체크
            if token.is_used:
                raise Exception("used email")

        if request.method == "POST":
            if form.is_valid():
                user = form.save(commit=False)

                user.email = email
                user.univ = univ
                user.save()

                # 이메일이 사용뒴
                token.is_used = True
                token.save()


                # 가입 후 바로 로그인 되게 하려면 씀
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')

                login_user = authenticate(username=username, password=raw_password)
                auth.login(request, login_user)

                return redirect("core:board:main_board", url_name=url_name)

        return render(request, "accounts/signup.html", {"form": form})

    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Bad Request: " + str(e))
