from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

User = get_user_model()
# Create your views here.


def redirect404(request):
    raise Http404('There is no matching url')


def check_mail(request):
    return render(request, "accounts/mail.html")


def signup(request, ):
    return render(request, "accounts/signup.html")

#uid, token
def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)

    if account_activation_token.check_token(user, token):
        user.is_validate = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
