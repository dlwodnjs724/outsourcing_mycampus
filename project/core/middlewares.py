from django.shortcuts import redirect, reverse


class UnivCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path.split('/')[1]
        exception_list = [
            'admin',
            'auth',
            '',
            'api',

        ]

        if request.user.is_authenticated and path not in exception_list:
            user = request.user.univ.url_name
            if user != path:
<<<<<<< HEAD
                return redirect('/')
=======
                return redirect('core:board:main_board', request.user.univ.url_name)
>>>>>>> board-jw

        return response
