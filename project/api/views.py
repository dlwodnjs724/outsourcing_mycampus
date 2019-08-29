# Create your views here.

# reqeust, User 모델 인스턴스, 보낼 이메일 주소
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
import arrow
import random
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from accounts.models import User
from board.models import Post, Comment, Noti, ReportedContent, Report
from core.models import Univ
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
        if not request.method == "POST":
            raise Exception("Not allowed method")

        email = request.POST.get('email')
        email_domain = email.split('@')[1]

        univ = request.POST.get('univ')
        univ_domain = Univ.objects.get(url_name=univ).domain

        if univ_domain != email_domain:
            raise Exception(f'Invalid email format. Please enter it according to your school email format. e.g. @{univ_domain}')

        token = get_token(email)

        url = request.build_absolute_uri(reverse('api:activate') + '?email=' + email + "&token=" + token.token + "&univ=" + univ)

        mail_subject = '[MY CAMPUS] Activate your account.'
        message = render_to_string('accounts/mail.html', {
            "url": url
        })

        email = EmailMessage(
                    mail_subject, message, to=[email]
        )
        email.content_subtype = "html"
        email.send()
        return HttpResponse(status=200)

    except Exception as e:
        print(e)
        return HttpResponseBadRequest(content="Failed: " + str(e))


def activate(request):
    url_name = request.GET.get('univ')
    token = request.GET.get('token')
    user_email = request.GET.get('email')

    try:
        token = Token.objects.get(token=token, target_email=user_email)
        univ = Univ.objects.get(url_name=url_name)

        if token.is_expired:
            return HttpResponseBadRequest(content="Token is expired")

        #인증 성공
        token.is_accepted = True
        token.save()

        return redirect(reverse("core:accounts:signup", args=[url_name]) + "?email=" + user_email)
    except Token.DoesNotExist:
        return HttpResponseBadRequest(content="Unauthorized token")


def post_bookmark(request):
    if request.user.is_anonymous:
        post = Post.objects.select_related('author', 'author__univ').get(pk=request.POST.get('pk', None))
        univ_url = post.author.univ.url_name
        return JsonResponse({
            'univ_url': univ_url,
        })

    try:
        if not request.user.is_authenticated:
            raise Exception("User is not authenticated")

        if request.user.is_anonymous:
            raise Exception("User is anonymous")

        if not request.method == 'POST':
            raise Exception("Not allowed request method")

        user = request.user
        post = Post.objects.get(pk=request.POST.get('pk', None))

        if post.saved.filter(pk=user.pk).exists():
            post.saved.remove(user)
        else:
            post.saved.add(user)
        context = {
            'pk': post.pk,
        }
        return JsonResponse(context)

    except Exception as e:
        return HttpResponseBadRequest(content="Bad request: " + str(e))


def post_like(request):
    if request.user.is_anonymous:
        post = Post.objects.select_related('author', 'author__univ').get(pk=request.POST.get('pk', None))
        univ_url = post.author.univ.url_name
        return JsonResponse({
            'univ_url': univ_url,
        })

    try:
        if not request.user.is_authenticated:
            raise Exception("User is not authenticated")

        if request.user.is_anonymous:
            raise Exception("User is anonymous")

        if not request.method == 'POST':
            raise Exception("Not allowed request method")

        user = request.user
        post = Post.objects.get(pk=request.POST.get('pk', None))

        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            Noti.objects.create(_from=request.user, _to=post.author, object_id=post.pk, content_type=ContentType.objects.get(app_label='board', model='post'))
            
        context = {
            'pk': post.pk,
            'likes_count': post.total_likes(),
        }
        return JsonResponse(context)
    except Exception as e:
        return HttpResponseBadRequest(content="Bad request:" + str(e))


def comment_like(request):
    if request.user.is_anonymous:
        comment = Comment.objects.select_related('author', 'author__univ').get(pk=request.POST.get('pk', None))
        univ_url = comment.author.univ.url_name
        return JsonResponse({
            'univ_url': univ_url,
        })

    try:
        if not request.user.is_authenticated:
            raise Exception("User is not authenticated")

        if request.user.is_anonymous:
            raise Exception("User is anonymous")

        if not request.method == 'POST':
            raise Exception("Not allowed request method")

        user = request.user
        comment = Comment.objects.get(pk=request.POST.get('pk', None))

        if comment.comment_likes.filter(pk=user.pk).exists():
            comment.comment_likes.remove(user)
        else:
            comment.comment_likes.add(user)
            Noti.objects.create(_from=request.user, _to=comment.author, object_id=comment.pk, content_type=ContentType.objects.get(app_label='board', model='comment'))

        context = {
            'pk': comment.pk,
            'likes_count': comment.total_likes(),
        }
        return JsonResponse(context)

    except Exception as e:
        return HttpResponseBadRequest(content="Bad request: " + str(e))


def report_content(request):
    """
    :param request:
    pk: 댓글, 게시글 pk
    targetType: c or p (댓글, 게시글)
    abuseType: (sexual, bully, racist, illegal, others)
    reporter: 신고 하는 사람 pk

    :return:
    로그인 안 한 유저는 univ_url
    한 유저는 200 ok
    """
    if not request.is_ajax():
        return JsonResponse({
            "err": "Only for api"
        })

    if not request.method == 'POST':
        return JsonResponse({
            "err": "Not allowed request method"
        })

    pk = request.POST.get('pk')
    target_type = request.POST.get('targetType')
    target = None

    if not request.user.is_anonymous:
        if target_type == 'c':
            target = Comment.objects.select_related('author', 'author__univ').get(pk=pk)
            url_name = target.author.univ.url_name
        else:
            target = Post.objects.select_related('author', 'author__univ').get(pk=pk)
            url_name = target.author.univ.url_name
        

    abuse_type = request.POST.get('abuseType')
    reporter_pk = request.POST.get('reporter')
    reporter = User.objects.get(pk=reporter_pk)
    abuser = target.author
    if request.user == abuser:
            return JsonResponse({
            "err": "You can't report yourself"
        })

    if target_type == 'p':
        report_content = ReportedContent(origin_post=target, content=target.content)
        report_content.title = target.title
    else:
        report_content = ReportedContent(origin_comment=target, content=target.content)
        report_content.title = target.content

    report_content.save()
    report_paper = Report(target_type=target_type, target_content=report_content, report_type=abuse_type, abuser=abuser, reporter=reporter)
    report_paper.save()

    abuser.is_reported = True
    abuser.save()

    return JsonResponse({
        "message": "Reporting is success"
    })
