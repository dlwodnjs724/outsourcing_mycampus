class UnivCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path.split('/')[1]
        exception_list= [ 
            'admin',
            'auth',
            '',
        ]
        if str(request.user) != "AnonymousUser" and (path not in exception_list):
            user = request.user.univ.url_name
            if (user != path):
                raise Exception("학교가 다름!!! ")

        return response