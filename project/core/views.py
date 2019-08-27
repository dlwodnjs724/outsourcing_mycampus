from django.shortcuts import render, redirect

from core.forms import UnivRegisterForm
from core.models import Univ


def main(request):
    univs = Univ.objects.all()

    if request.method == 'POST':
        univ_url_name = request.POST.get('univ')
        if univ_url_name == 'none':
            return redirect('main_register')
        if univ_url_name:
            return redirect('core:board:main_board', univ_url_name)

    return render(request, 'core/main.html', {
        'univs': univs,
    })


def main_register(request):
    form = UnivRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            univ = form.save()
            return render(request, 'core/success.html', {
                'univ_name': univ.full_name,
            })

    return render(request, 'core/register.html', {
        'form': form,
    })
