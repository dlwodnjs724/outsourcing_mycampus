from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from board.forms import PostForm, SuggestForm
from board.serializers import PostSerializer, NotiSerializer, CommentSerializer
from board.models import Category, Post, Image, Comment, Report, Noti
from django.contrib.contenttypes.models import ContentType
from core.models import Univ
from core.utils.url_controll import redirect_with_next


def make_posts_set(category, univ, state, term=""):
    if category:
        ret = Post.objects.select_related('ctgy', 'author') \
            .prefetch_related('comments__author','ctgy__univ', 'likes', 'saved', 'viewed_by', 'comments', 'images') \
            .filter(ctgy__univ=univ, ctgy=category, is_notice=False, is_ctgy_notice=False) \
            .annotate(num_likes=Count('likes'))

    else:
        ret = Post.objects.select_related('ctgy', 'author') \
            .prefetch_related('comments__author', 'ctgy__univ', 'likes', 'saved', 'viewed_by', 'comments', 'images') \
            .filter(ctgy__univ=univ, is_notice=False, is_ctgy_notice=False) \
            .annotate(num_likes=Count('likes')) \


    if term:
        ret = ret.filter(Q(title__icontains=term) | Q(content__icontains=term))

    if state == "hot":
        gte_5 = ret.filter(num_likes__gte=5).order_by('-created_at')
        lt_5 = ret.exclude(pk__in=gte_5).order_by('-num_likes', '-created_at')
        # ret = gte_5 | lt_5
        ret = list(chain(gte_5, lt_5))
        # ret = ret.order_by('-num_likes', '-created_at')
    else:
        ret = ret.order_by('-created_at')

    return ret


def can_use(request, url_name, ck_category=False, ck_anon=False, ck_univ_url=False, use_category=""):
    state = request.GET.get("state") or "hot"
    term = request.GET.get("term")
    must_check = bool(term or (state == 'new'))

    univ = Univ.objects.prefetch_related('category').get(url_name=url_name)
    selected_category = None

    if use_category:
        selected_category = univ.category.get(name=use_category)

    if ck_category and not univ.category.count():
        raise Exception("There is no category in {}.".format(univ.full_name))

    if ck_anon and must_check and request.user.is_anonymous:
        raise Exception("anon")

    if ck_univ_url and must_check and request.user.univ.url_name != url_name:
        raise Exception('others')

    return [univ, state, term, selected_category]


@api_view(('POST', 'GET'))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def main(request, url_name):
    try:

        request.session['back_url'] = request.path
        # term, state 변경 했을 때 유저를 체크 해야 함
        [univ, state, term, selected_category] = can_use(request, url_name, True, True, True)

        post_sets = make_posts_set(None, univ, state, term)
        is_post = False if post_sets else True
        notice_sets = Post.objects.select_related('ctgy', 'author') \
            .prefetch_related('comments__author', 'ctgy__univ', 'likes', 'saved', 'viewed_by', 'comments', 'images')\
            .filter(ctgy__univ=univ, is_notice=True)
        post_paginator = Paginator(post_sets, 15).page
        posts = post_paginator(1)

        if request.is_ajax():  # 무한스크롤
            if not request.method == "POST":
                raise Exception("Not allowed request method")

            requested_page = request.POST.get('requestPage')
            next_posts = post_paginator(requested_page)
            serializer = PostSerializer(next_posts.object_list, many=True)

            has_next = next_posts.has_next()
            return Response(status=status.HTTP_200_OK, data={"next_posts": serializer.data, "has_next": has_next})

        else:
            url = reverse('core:board:main_board', args=[url_name])
            return render(request, 'board/main_board.html', {
                'univ': univ,
                "url_name": url_name,
                'categories': univ.category.all(),
                'use_category': False,
                'posts': posts.object_list,
                'notices': notice_sets,
                'state': state,
                'url': url,
                'has_next': posts.has_next(),
                'is_post': is_post,
            })
    except Univ.DoesNotExist as e:
        raise Http404(e)

    except Exception as e:
        if str(e) == 'anon':
            return redirect_with_next("core:accounts:login", "core:board:main_board",
                                      params={"to": [url_name], "next": [url_name]})

        if str(e) == 'others':
            return redirect("core:board:main_board", url_name=request.user.univ.url_name)
        return HttpResponseBadRequest(content="Bad Request: " + str(e))


def post_create(request, url_name):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:post_create',
            params={
                'to': [url_name],
                'next': [url_name]
            }
        )
    try:
        can_use(request, url_name, ck_univ_url=True, ck_anon=True)
        univ = get_object_or_404(Univ, url_name=url_name)
        form = PostForm(request.POST or None, request=request)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                if post.ctgy.is_anonymous:
                    post.is_anonymous = True
                post.save()
                for image in request.FILES.getlist('images'):
                    Image.objects.create(post=post, image=image)
                return redirect(reverse('core:board:main_board', args=[url_name]) + '?state=new')
        return render(request, 'board/post_new.html', {
            'form': form,
            'univ': univ,
            'url_name': url_name,
        })

    except Exception as e:
        if str(e) == 'anon':
            return redirect_with_next("core:accounts:login", "core:board:main_board",
                                      params={"to": [url_name], "next": [url_name]})
        if str(e) == 'others':
            return redirect("core:board:main_board", url_name=request.user.univ.url_name)

        return HttpResponseBadRequest(content="Bad request: " + str(e))


@api_view(('POST', 'GET'))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def category_board(request, url_name, category_name):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:category_board',
            params={
                'to': [url_name],
                'next': [url_name, category_name]
            }
        )
    try:
        [univ, state, term, selected_category] = can_use(request, url_name, ck_univ_url=True, ck_anon=True,
                                                         use_category=category_name)

        request.session['back_url'] = request.path
        post_sets = make_posts_set(selected_category, univ, state, term)
        is_post = False if post_sets else True
        notice_sets = Post.objects.select_related('ctgy', 'author') \
            .prefetch_related('comments__author', 'ctgy__univ', 'likes', 'saved', 'viewed_by', 'comments', 'images') \
            .filter(ctgy__univ=univ, is_ctgy_notice=True)
        current_page = 1

        post_paginator = Paginator(post_sets, 15).page
        posts = post_paginator(current_page)

        if request.is_ajax():  # 무한스크롤
            if not request.method == "POST":
                raise Exception("Not allowed request method")

            requested_page = request.POST.get('requestPage')
            next_posts = post_paginator(requested_page)
            serializer = PostSerializer(next_posts.object_list, many=True)

            has_next = next_posts.has_next()

            return Response({"next_posts": serializer.data, "has_next": has_next})

        else:
            url = reverse("core:board:category_board", args=[url_name, category_name])

            return render(request, 'board/main_board.html', {
                'univ': univ,
                'url_name': url_name,
                'categories': univ.category.all(),
                'selected_category': selected_category,
                'use_category': False,
                'state': state,
                'posts': posts.object_list,
                'notices': notice_sets,
                'url': url,
                'has_next': posts.has_next(),
                'is_post': is_post,
            })

    except Exception as e:
        if str(e) == 'anon':
            return redirect_with_next("core:accounts:login", "core:board:main_board",
                                      params={"to": [url_name], "next": [url_name]})
        if str(e) == 'others':
            return redirect("core:board:main_board", url_name=request.user.univ.url_name)

        return HttpResponseBadRequest(content="Bad request: " + str(e))


def post_detail(request, url_name, category_name, post_pk):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:post_detail',
            params={
                'to': [url_name],
                'next': [url_name, category_name, post_pk]
            }
        )

    univ = get_object_or_404(Univ, url_name=url_name)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    anon = True if selected_category.is_anonymous else False
    post = get_object_or_404(
        Post.objects.select_related('author')
            .prefetch_related('likes', 'saved', 'comments', 'images'),
        ctgy=selected_category, pk=post_pk
    )
    comments = Comment.objects.prefetch_related('comment_likes', 'parent', 'parent__author')\
        .select_related('author', 'parent', 'post', 'post__author')\
        .filter(post=post, parent=None).order_by('created_at')
    is_author = True if request.user == post.author else False
    # post.viewed_by.add(request.user)
    # post.views_double_check.add(request.user)
    # if not request.user in post.views_double_check: 
    #     post.views += 1
    # post.save()
    # print(post.viewed_by.all)

    ctx = {
        'univ': univ,
        'url_name': url_name,
        'post': post,
        'selected_category': selected_category,
        'comments': comments,
        'anon': anon,
        'is_author': is_author,
        # 'comment_form': CommentForm(request=request),
    }

    response = render(request, 'board/post_detail.html', ctx)

    cookie_name = f'hit:{request.user}'
    # print(cookie_name)
    tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(post_pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{post_pk}', expires=expires)
            post.views += 1
            post.viewed_by.add(request.user)
            post.save()
            return response
    else:
        response.set_cookie(cookie_name, post_pk, expires=expires)
        post.views += 1
        post.viewed_by.add(request.user)
        post.save()
        return response

    return render(request, 'board/post_detail.html', ctx)


def post_edit(request, url_name, category_name, post_pk):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:post_detail',
            params={
                'to': [url_name],
                'next': [url_name, category_name, post_pk]
            }
        )
    univ = get_object_or_404(Univ, url_name=url_name)
    post = Post.objects.get(pk=post_pk)
    if request.user != post.author:
        return redirect(
            'core:board:post_detail',
            url_name, category_name, post_pk
        )

    form = PostForm(request.POST or None, request=request, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            if post.ctgy.is_anonymous:
                post.is_anonymous = True
            post.save()
            for image in request.FILES.getlist('images'):
                Image.objects.create(post=post, image=image)
            return redirect(
                'core:board:post_detail',
                url_name, category_name, post_pk
            )
    return render(request, 'board/post_new.html', {
        'form': form,
        'univ': univ,
        'url_name': url_name
    })


def post_delete(request, url_name, category_name, post_pk):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:post_detail',
            params={
                'to': [url_name],
                'next': [url_name, category_name, post_pk]
            }
        )

    post = Post.objects.get(pk=post_pk)
    if request.user != post.author:
        return redirect(
            'core:board:post_detail',
            url_name, category_name, post_pk
        )

    if request.method == 'POST':
        post.delete()
        return redirect('core:board:main_board', url_name)

    return redirect(
        'core:board:post_detail',
        url_name, category_name, post_pk
    )


def comment_create(request, url_name, category_name, post_pk):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:post_detail',
            params={
                'to': [url_name],
                'next': [url_name, category_name, post_pk]
            }
        )
    noti_target = Post.objects.get(pk=post_pk).author
    if request.method == 'POST':
        is_anonymous = True if request.POST.get('is_anonymous') else False
        comment = Comment.objects.create(
            post_id=post_pk,
            author=request.user,
            content=request.POST.get('content', ''),
            is_anonymous=is_anonymous
        )
        if  noti_target != request.user:
            Noti.objects.create(from_n=request.user,noti_type='c', to_n=noti_target, object_id=post_pk, content_type=ContentType.objects.get(app_label='board', model='post'))
        return redirect('core:board:post_detail', url_name, category_name, post_pk)
    # if request.method == 'POST':
    #     is_anonymous = True if request.POST.get('comment_is_anonymous', '') == 'true' else False
    #     comment = Comment.objects.create(
    #         post_id=post_pk,
    #         author=request.user,
    #         content=request.POST.get('comment_content', ''),
    #         is_anonymous=is_anonymous
    #     )
    #
    #     comments_queryset = Comment.objects.filter(post_id=post_pk, parent=None)
    #     comments = list(comments_queryset.values('pk', 'content', 'created_at'))
    #
    #     for i, comment in enumerate(comments_queryset):
    #         comments[i]['name'] = comment.name
    #         comments[i]['comment_likes'] = comment.total_likes()
    #
    #     context = {
    #         'comments': comments
    #     }
    #     return JsonResponse(context)
    # return redirect('core:board:post_detail', url_name, category_name, post_pk)


def comment_nest_create(request, url_name, category_name, post_pk):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:post_detail',
            params={
                'to': [url_name],
                'next': [url_name, category_name, post_pk]
            }
        )
    noti_target_comment =Comment.objects.get(pk=request.POST.get('parent_id')).author
    noti_target_post = Post.objects.get(pk=post_pk).author
    if request.method == 'POST':
        is_anonymous = True if request.POST.get('nested_is_anonymous') else False
        comment = Comment.objects.create(
            post_id=post_pk,
            author=request.user,
            content=request.POST.get('nested_content', ''),
            is_anonymous=is_anonymous,
            parent_id=request.POST.get('parent_id')
        )
        if (noti_target_comment or noti_target_post) != request.user :
            Noti.objects.create(from_n=request.user,noti_type='c_c', to_n=noti_target, object_id=request.POST.get('parent_id'), content_type=ContentType.objects.get(app_label='board', model='comment'))

        return redirect('core:board:post_detail', url_name, category_name, post_pk)

    # if request.method == 'POST':
    #     is_anonymous = True if request.POST.get('nested_comment_is_anonymous', '') == 'true' else False
    #     comment = Comment.objects.create(
    #         post_id=post_pk,
    #         author=request.user,
    #         content=request.POST.get('nested_comment_content', ''),
    #         is_anonymous=is_anonymous,
    #         parent_id=request.POST.get('parent_id')
    #     )
    #
    #     comments_queryset = Comment.objects.filter(parent_id=request.POST.get('parent_id'))
    #     comments = list(comments_queryset.values('pk', 'content', 'created_at'))
    #
    #     for i, comment in enumerate(comments_queryset):
    #         comments[i]['name'] = comment.name
    #         comments[i]['comment_likes'] = comment.total_likes()
    #
    #     context = {
    #         'comments': comments
    #     }
    #     return JsonResponse(context)
    # return redirect('core:board:post_detail', url_name, category_name, post_pk)


def comment_delete(request, url_name, category_name, post_pk, comment_pk):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:post_detail',
            params={
                'to': [url_name],
                'next': [url_name, category_name, post_pk]
            }
        )

    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        if request.user != comment.author:
            return redirect('core:board:post_detail', url_name, category_name, post_pk)
        comment.content = '(deleted reply)'
        comment.save()
        return redirect('core:board:post_detail', url_name, category_name, post_pk)
    return redirect('core:board:post_detail', url_name, category_name, post_pk)


def category_create(request, url_name):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:category_create',
            params={
                'to': [url_name],
                'next': [url_name]
            }
        )

    form = SuggestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            suggest = form.save(commit=False)
            suggest.suggested_by = request.user
            suggest.univ = request.user.univ
            suggest.save()
            return render(request, 'board/category_success.html', {
                'univ': request.user.univ,
                'url_name': url_name,
                'category_name': suggest.name,
            })
    return render(request, 'board/category_new.html', {
        'univ': request.user.univ,
        'url_name': url_name,
        'form': form,
    })


def notification(request, url_name):
    if request.user.is_anonymous:
        return redirect_with_next(
            'core:accounts:login',
            'core:board:notification',
            params={
                'to': [url_name],
                'next': [url_name]
            }
        )

    univ = request.user.univ
    notifications = Noti.objects.prefetch_related(
        'from_n__comment_set__post',
        'from_n__posts__ctgy',
    ).filter(to_n=request.user).order_by('-id')
    
    return render(request, 'board/notification.html', {
        'notifications': notifications,
        'univ': univ,
        'url_name': url_name,
    })


def notificationJson(request, url_name):
    univ = request.user.univ
    notifications = Noti.objects.filter(to_n=request.user).order_by('-id')[:5]
    serializer = NotiSerializer(notifications, many=True)
    data = {'noti': serializer.data}

    return JsonResponse(data)


def getObjectNoti(request, url_name):
    univ = request.user.univ
    content_type = request.GET.get('contentType')
    object_id = request.GET.get('objectId')

    if content_type == 10:
        content = Post.objects.get(pk=object_id)
        serializer = PostSerializer(content)
    else:
        content = Comment.objects.get(pk=object_id)
        serializer = CommentSerializer(content)

    data = {'content': serializer.data}

    return JsonResponse(data)
