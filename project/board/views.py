from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from board.models import Category, Post, Comment
from core.models import Univ
from .forms import ReportForm

def main_board(request, url_name):
    if request.user.is_authenticated and url_name != request.user.univ.url_name:
        return redirect('board:main_board', request.user.univ.url_name)

    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    posts = Post.objects.filter(ctgy__univ=univ)
    return render(request, 'board/main_board.html', {
        'univ': univ,
        'categories': categories,
        'posts': posts,
    })


@login_required
def category_board(request, url_name, category_name):
    if request.user.univ.url_name != url_name:
        return redirect('board:main_board', [request.user.univ.url_name])

    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    posts = Post.objects.filter(ctgy=selected_category)
    return render(request, 'board/category_board.html', {
        'univ': univ,
        'categories': categories,
        'selected_category': selected_category,
        'posts': posts,
    })


@login_required
def post_detail(request, url_name, category_name, post_pk):
    if request.user.univ.url_name != url_name:
        return redirect('board:main_board', [request.user.univ.url_name])

    univ = get_object_or_404(Univ, url_name=url_name)
    selected_category = get_object_or_404(Category, univ=univ, name=category_name)
    post = get_object_or_404(Post, ctgy=selected_category, pk=post_pk)

    return render(request, 'board/post_detail.html', {
        'univ': univ,
        'post': post,
    })


@login_required
def post_like(request, url_name):
    if request.user.univ.url_name != url_name:
        return redirect('board:main_board', [request.user.univ.url_name])

    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(request.POST.get('pk', None))

        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        context = {
            'likes_count': post.total_likes,
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
