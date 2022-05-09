from django.shortcuts import redirect
from django.contrib import messages



# 로그인 여부 데코레이터
def login_required(func):
    def wrapper(request, *args, **kwargs):
        login_session = request.session.get('login_session', '')

        if login_session == '':
            return redirect('/accounts/login/')

        return func(request, *args, **kwargs)
    return wrapper

# 사내 로그인 여부
def login_ok(func):
    def wrapper(request, *args, **kwargs):
        login_session = request.session.get('login_session', '')

        if login_session == '':
            return redirect('/accounts/login/')
        elif login_session == 'insung':
            return func(request, *args, **kwargs)
        else:
            messages.info(request, "접근 권한이 없습니다.")
            return redirect('/isscm/')
        return func(request, *args, **kwargs)
    return wrapper


