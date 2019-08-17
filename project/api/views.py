# Create your views here.

# reqeust, User 모델 인스턴스, 보낼 이메일 주소
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
import arrow
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_mail(request):
    try:
        email = request.GET.get('email')
        univ = request.GET.get('univ')
        deploy_time = arrow.now().timestamp
        mail_subject = '[MY CAMPUS] Activate your account.'
        message = render_to_string('accounts/mail.html',{
            "univ": univ,
            "deploy_time": deploy_time,
            "user_email": email
        })
        email = EmailMessage(
                    mail_subject, message, to=[email]
        )
        email.send()
        return HttpResponse(status=200)

    except:
        return HttpResponse(status=400)


def activate(request):
    univ = request.GET.get('univ')
    deploy_time = request.GET.get('deploy_time')
    user_email = request.GET.get('user_email')

    diff = arrow.now().timestamp - deploy_time

    if diff < 60 * 5:
        return redirect(reverse("accounts:signup"))


