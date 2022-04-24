from django.shortcuts import redirect


def login_required(func):
    def wrapper(request, *args, **kwargs):
        login_session = request.session.get('login_session', '')

        if login_session == '':
            return redirect('/accounts/login/')

        return func(request, *args, **kwargs)
    return wrapper