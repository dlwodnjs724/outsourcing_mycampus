from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from board.forms import PostForm, CommentForm
from board.models import Category, Post, Image, Comment
from core.models import Univ
from .forms import ReportForm


def main_board(request, url_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved') \
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
    })


@login_required
def main_board_new(request, url_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved') \
        .filter(ctgy__univ=univ)

    search = request.GET.get('search', '')
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))

    return render(request, 'board/main_board.html', {
        'univ': univ,
        'categories': categories,
        'search': search,
        'posts': posts,
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
            return redirect('core:board:main_board', request.user.univ.url_name)
    return render(request, 'board/post_new.html', {
        'form': form,
    })


@login_required
def category_board(request, url_name, category_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved') \
        .filter(ctgy=selected_category) \
        .annotate(num_likes=Count('likes')) \
        .order_by('-num_likes', '-created_at')

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
def category_board_new(request, url_name, category_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    posts = Post.objects.select_related('ctgy', 'author').prefetch_related('likes', 'saved') \
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
    post = get_object_or_404(Post, ctgy=selected_category, pk=post_pk)
    comments = Comment.objects.prefetch_related('comment_likes').select_related('author').filter(post=post)

    return render(request, 'board/post_detail.html', {
        'univ': univ,
        'post': post,
        'selected_category': selected_category,
        'comments': comments,
        'comment_form': CommentForm(request=request),
    })


@login_required
def post_edit(request):
    pass


@login_required
def comment_new(request, url_name, category_name, post_pk):
    if request.method == 'POST':
        is_anonymous = True if request.POST.get('comment_is_anonymous', '') == 'true' else False
        comment = Comment.objects.create(
            post=Post.objects.get(pk=post_pk),
            author=request.user,
            content=request.POST.get('comment_content', ''),
            is_anonymous=is_anonymous
        )
        context = {
            'comments': serialize('json', Comment.objects.filter(post=post_pk))
        }
        return JsonResponse(context)
    return redirect('core:board:post_detail', url_name, category_name, post_pk)


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
