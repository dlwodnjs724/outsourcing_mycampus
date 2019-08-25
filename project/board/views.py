from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
import datetime
from board.forms import PostForm, CommentForm
from board.models import Category, Post, Image, Comment
from core.models import Univ
from .forms import ReportForm


def main_board(request, url_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    state = "hot"
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved', 'viewed_by', 'comments') \
        .filter(ctgy__univ=univ) \
        .annotate(num_likes=Count('likes')) \
        .order_by('-num_likes', '-created_at')

    search = request.GET.get('search', '')
    if search:
        if not request.user.is_authenticated:
            return redirect('core:accounts:login', url_name)
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))

    return render(request, 'board/main_board.html', {
        'univ': univ,
        'categories': categories,
        'posts': posts,
        'state': state,
    })


@login_required
def main_board_new(request, url_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved', 'viewed_by', 'comments') \
        .filter(ctgy__univ=univ)

    search = request.GET.get('search', '')
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
    state = "new"

    return render(request, 'board/main_board.html', {
        'univ': univ,
        'categories': categories,
        'search': search,
        'posts': posts,
        'state': state,
    })


@login_required
def post_like(request, url_name):
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(pk=request.POST.get('pk', None))

        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        context = {
            'pk': post.pk,
            'likes_count': post.total_likes(),
        }
        return JsonResponse(context)
    else:
        return redirect('core:board:main_board', request.user.univ.url_name)


@login_required
def post_bookmark(request, url_name):
    if request.method == 'POST':
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
    else:
        return redirect('core:board:main_board', request.user.univ.url_name)


@login_required
def post_create(request, url_name):
    form = PostForm(request.POST or None, request=request)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            for image in request.FILES.getlist('images'):
                Image.objects.create(post=post, image=image)
            return redirect('core:board:main_board_new', request.user.univ.url_name)
    return render(request, 'board/post_new.html', {
        'form': form,
    })


@login_required
def category_board(request, url_name, category_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved', 'viewed_by', 'comments') \
        .filter(ctgy=selected_category) \
        .annotate(num_likes=Count('likes')) \
        .order_by('-num_likes', '-created_at')

    search = request.GET.get('search', '')
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))

    return render(request, 'board/main_board.html', {
        'univ': univ,
        'categories': categories,
        'selected_category': selected_category,
        'posts': posts,
    })


@login_required
def category_board_new(request, url_name, category_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved', 'viewed_by', 'comments') \
        .filter(ctgy=selected_category)

    search = request.GET.get('search', '')
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))

    return render(request, 'board/category_board.html', {
        'univ': univ,
        'categories': categories,
        'selected_category': selected_category,
        'posts': posts,
    })


@login_required
def post_detail(request, url_name, category_name, post_pk):
    univ = get_object_or_404(Univ, url_name=url_name)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    post = get_object_or_404(Post.objects.prefetch_related('likes'), ctgy=selected_category, pk=post_pk)
    comments = Comment.objects.prefetch_related('comment_likes', 'parent', 'parent__author')\
        .select_related('author', 'parent', 'post')\
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
            response.set_cookie(cookie_name, cookies + f'|{post_pk}', expires =expires)
            post.views += 1
            post.viewed_by.add(request.user)
            post.save()
            return response
    else:
        response.set_cookie(cookie_name, post_pk, expires =expires)
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


@login_required
def comment_like(request, url_name, category_name, post_pk):
    if request.method == 'POST':
        user = request.user
        comment = Comment.objects.get(pk=request.POST.get('pk', None))

        if comment.comment_likes.filter(pk=user.pk).exists():
            comment.comment_likes.remove(user)
        else:
            comment.comment_likes.add(user)
        context = {
            'pk': comment.pk,
            'likes_count': comment.total_likes(),
        }
        return JsonResponse(context)
    else:
        return redirect('core:board:main_board', [request.user.univ.url_name])


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
