from django import template

from board.models import Comment

register = template.Library()


@register.filter
def child_comments(parent):
    comments = Comment.objects.filter(parent=parent)
    return comments
