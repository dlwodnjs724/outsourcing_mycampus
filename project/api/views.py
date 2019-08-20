# Create your views here.

# reqeust, User 모델 인스턴스, 보낼 이메일 주소
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
import arrow
import random
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Token


def random_token(length):
     available = 'qwertyuiopasdfghjklzxcvbnm123456789QWERTYUIOPASDFGHJKLZXCVBNM'
     return "".join([random.choice(available) for _ in range(length)])


def get_token(email):
    try:
        exist_token = Token.objects.get(target_email=email)
        exist_token.created_at = arrow.now().timestamp
        exist_token.token = random_token(10)
        exist_token.save()

        return exist_token;

    except Token.DoesNotExist:
        new_token = Token.objects.create(target_email=email, created_at=arrow.now().timestamp, token=random_token(10))
        return new_token



@csrf_exempt
def send_mail(request):
    try:
        if request.method == "POST":

            email = request.POST.get('email')
            univ = request.POST.get('univ')
            token = get_token(email)

            url = reverse("api:activate") + "?email=" + email + "&token=" + token.token + "&univ=" + univ

            mail_subject = '[MY CAMPUS] Activate your account.'
            message = render_to_string('accounts/mail.html', {
                "url": url
            })

            email = EmailMessage(
                        mail_subject, message, to=[email]
            )
            email.send()
            return HttpResponse(status=200)
        else:
            raise Exception
    except Exception as e:
        print(e)
        return HttpResponse(status=400, content="Failed")


def activate(request):
    univ = request.GET.get('univ')
    token = request.GET.get('token')
    user_email = request.GET.get('email')

    try:
        token = Token.objects.get(token=token, target_email=user_email)

        if token.is_expired:
            return HttpResponseBadRequest(content="Token is expired")

        return redirect(reverse("core:accounts:signup") + "?email=" + user_email, url_name=univ)
    except Token.DoesNotExist:
        return HttpResponseBadRequest(content="Unauthorized token")


