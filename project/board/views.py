from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
import datetime

from django.urls import reverse

from board.forms import PostForm, CommentForm
from board.models import Category, Post, Image, Comment, Report, Noti
from django.contrib.contenttypes.models import ContentType
from core.models import Univ
from core.utils.url_controll import redirect_with_next
from .forms import ReportForm


def make_posts_set(category, univ, state, term=""):
    if category:
        ret = Post.objects.select_related('ctgy', 'author') \
            .prefetch_related('ctgy__univ', 'likes', 'saved', 'viewed_by', 'comments', 'images') \
            .filter(ctgy__univ=univ, ctgy=category) \
            .annotate(num_likes=Count('likes'))

    else:
        ret = Post.objects.select_related('ctgy', 'author') \
            .prefetch_related('ctgy__univ', 'likes', 'saved', 'viewed_by', 'comments', 'images') \
            .filter(ctgy__univ=univ) \
            .annotate(num_likes=Count('likes'))

    if term:
        ret = ret.filter(Q(title__icontains=term) | Q(content__icontains=term))

    if state == "hot":
        ret = ret.order_by('-num_likes', '-created_at')
    else:
        ret = ret.order_by('-created_at')

    return ret


def can_use(request, url_name, ck_category=False, ck_anon=False, ck_univ_url=False, use_category=""):
    state = request.GET.get("state") or "hot"
    term = request.GET.get("term")
    must_check = bool(term)

    univ = Univ.objects.prefetch_related('category').get(url_name=url_name)
    selected_category = None

    if use_category:
        selected_category = univ.category.get(name=use_category)

    if ck_category and not len(univ.category.all()):
        raise Exception("There is no category in {}.".format(univ.full_name))

    if ck_anon and must_check and request.user.is_anonymous:
        raise Exception("anon")

    if ck_univ_url and must_check and request.user.univ.url_name != url_name:
        raise Exception('others')

    return [univ, state, term, selected_category]


def main(request, url_name):
    try:

        # term, category를 변경 했을 때 유저를 체크 해야 함
        [univ, state, term, selected_category] = can_use(request, url_name, True, True, True)

        post_sets = make_posts_set(None, univ, state, term)

        post_paginator = Paginator(post_sets, 15).page
        posts = post_paginator(1)
        if request.is_ajax():  # 무한스크롤
            if not request.method == "POST":
                raise Exception("Not allowed request method")

            requested_page = request.POST.get('requestPage')
            next_posts = post_paginator(requested_page)
            object_list = serializers.serialize("json", next_posts.object_list)
            has_next = next_posts.has_next()

            return JsonResponse({"next_posts": object_list, "has_next": has_next})

        else:
            url = reverse('core:board:main_board', args=[url_name])
            return render(request, 'board/main_board.html', {
                'univ': univ,
                "url_name": url_name,
                'categories': univ.category.all(),
                'use_category': False,
                'posts': posts.object_list,
                'state': state,
                'url': url
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
    try:
        can_use(request, url_name, ck_univ_url=True, ck_anon=True)

        form = PostForm(request.POST or None, request=request)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save()
                for image in request.FILES.getlist('images'):
                    Image.objects.create(post=post, image=image)
                return redirect(reverse('core:board:main_board', args=[url_name]) + '?state=new')
        return render(request, 'board/post_new.html', {
            'form': form,
            'url_name': url_name,
        })

    except Exception as e:
        if str(e) == 'anon':
            return redirect_with_next("core:accounts:login", "core:board:main_board",
                                      params={"to": [url_name], "next": [url_name]})
        if str(e) == 'others':
            return redirect("core:board:main_board", url_name=request.user.univ.url_name)

        return HttpResponseBadRequest(content="Bad request: " + str(e))


def category_board(request, url_name, category_name):
    try:
        [univ, state, term, selected_category] = can_use(request, url_name, ck_univ_url=True, ck_anon=True,
                                                         use_category=category_name)


        post_sets = make_posts_set(selected_category, univ, state, term)

        current_page = 1

        post_paginator = Paginator(post_sets, 15).page
        posts = post_paginator(current_page)

        if request.is_ajax():  # 무한스크롤
            if not request.method == "POST":
                raise Exception("Not allowed request method")

            requested_page = request.POST.get('requestPage')
            next_posts = post_paginator(requested_page)
            object_list = serializers.serialize("json", next_posts.object_list)
            has_next = next_posts.has_next()

            return JsonResponse({"next_posts": object_list, "has_next": has_next})

        else:
            url = reverse("core:board:category_board", args=[url_name, category_name])

            return render(request, 'board/main_board.html', {
                'univ': univ,
                'categories': univ.category.all(),
                'selected_category': selected_category,
                'use_category': False,
                'state': state,
                'posts': posts,
                'url': url
            })

    except Exception as e:
        if str(e) == 'anon':
            return redirect_with_next("core:accounts:login", "core:board:main_board",
                                      params={"to": [url_name], "next": [url_name]})
        if str(e) == 'others':
            return redirect("core:board:main_board", url_name=request.user.univ.url_name)

        return HttpResponseBadRequest(content="Bad request: " + str(e))


@login_required
def post_detail(request, url_name, category_name, post_pk):
    univ = get_object_or_404(Univ, url_name=url_name)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    post = get_object_or_404(
        Post.objects.select_related('author')
            .prefetch_related('likes', 'saved', 'comments'),
        ctgy=selected_category, pk=post_pk
    )
    comments = Comment.objects.prefetch_related('comment_likes', 'parent', 'parent__author')\
        .select_related('author', 'parent', 'post', 'post__author')\
        .filter(post=post, parent=None)

    # post.viewed_by.add(request.user)
    # post.views_double_check.add(request.user)
    # if not request.user in post.views_double_check: 
    #     post.views += 1
    # post.save()
    # print(post.viewed_by.all)

    ctx = {
        'univ': univ,
        'post': post,
        'selected_category': selected_category,
        'comments': comments,
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


@login_required
def post_edit(request):
    pass


@login_required
def comment_create(request, url_name, category_name, post_pk):
    if request.method == 'POST':
        is_anonymous = True if request.POST.get('is_anonymous') else False
        comment = Comment.objects.create(
            post_id=post_pk,
            author=request.user,
            content=request.POST.get('content', ''),
            is_anonymous=is_anonymous
        )
        Noti.objects.create(_from=request.user, _to=Post.objects.get(pk=post_pk).author, object_id=post_pk, content_type=ContentType.objects.get(app_label='board', model='post'))
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


@login_required
def comment_nest_create(request, url_name, category_name, post_pk):
    if request.method == 'POST':
        is_anonymous = True if request.POST.get('nested_is_anonymous') else False
        comment = Comment.objects.create(
            post_id=post_pk,
            author=request.user,
            content=request.POST.get('nested_content', ''),
            is_anonymous=is_anonymous,
            parent_id=request.POST.get('parent_id')
        )
        Noti.objects.create(_from=request.user, _to=Comment.objects.get(pk=request.POST.get('parent_id')).author, object_id=request.POST.get('parent_id'), content_type=ContentType.objects.get(app_label='board', model='comment'))

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


def report_send(request, pk, content_type):
    if content_type == 'comment':
        q = get_object_or_404(Comment, pk=pk)
    elif content_type == 'post':
        q = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r = Report(content_object=q)
            r.save()
            return
    else:
        form = ReportForm()

    return
