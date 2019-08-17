from django.shortcuts import render, get_object_or_404, get_list_or_404

from board.models import Category, Post
from core.models import Univ


def main_board(request, url_name):
    univ = get_object_or_404(Univ, url_name=url_name)
    categories = get_list_or_404(Category, univ=univ)
    posts = Post.objects.filter(ctgy__univ=univ)
    return render(request, 'board/main_board.html', {
        'univ': univ,
        'categories': categories,
        'posts': posts,
    })
