from django.shortcuts import render


def main(request, url_name):
    return render(request, 'core/main.html')
