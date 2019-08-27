from django import template

from board.models import Comment

register = template.Library()


@register.filter
def child_comments(parent):
    comments = Comment.objects.prefetch_related('comment_likes')\
        .select_related('author', 'parent', 'post', 'post__author')\
        .filter(parent=parent)
    return comments
