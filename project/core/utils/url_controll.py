from django.shortcuts import redirect
from django.urls import reverse


def redirect_with_next(to, next, params):
    """
    :param to: redirect 할 곳 (namespace)
    :param permanent:
    :param next: 처리 이후 이동할 url namespace
    :param kwargs: to, next의 args를 담을 것
    {to: [string], next: [string]}
    :return:
    """

    url = reverse(to, args=[*params['to']]) + "?next=" + reverse(next, args=[*params['next']])
    return redirect(url)