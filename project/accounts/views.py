from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .models import User
# Create your views here.
from django.views.generic.base import View


def sendMail(request, user, to_email):
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account.'
    message = render_to_string('activationMail.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    })
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()


def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')