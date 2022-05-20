from django.shortcuts import render, redirect

from .models import User
from .forms import RegisterForm, LoginForm



# Create your views here.


# 회원 가입
def register(request):
    register_form = RegisterForm()
    login_session = request.session.get('login_session')
    context = {'forms': register_form, 'login_session': login_session}

    if request.method == 'GET':
        return render(request, 'accounts/register.html', context)
    elif request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            # 입력한 정보 저장
            user = User(
                user_id=register_form.user_id,
                cname=register_form.cname,
                user_name = register_form.user_name,
                user_pw=register_form.user_pw,
                user_phone=register_form.user_phone,
                user_email=register_form.user_email,
                user_dept=register_form.user_dept
            )
            user.save()
            login_session = request.session.get('login_session')
            context = {'forms': register_form, 'login_session': login_session}
            return render(request, 'isscm/index.html', context)
        else:
            context['forms'] = register_form
            if register_form.errors:
                for value in register_form.errors.values():
                    print(value)
                    context['error'] = value
        return render(request, 'accounts/register.html', context)

# 로그인
def login(request):
    loginform = LoginForm()
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    context = { 'forms': loginform, 'login_session': login_session, 'user_name':user_name }

    if request.method == 'GET':
        print("로그인 시작 겟방식")
        return render(request, 'accounts/login.html', context)
    elif request.method == 'POST':
        loginform = LoginForm(data=request.POST)
            # 로그인 폼 검증
        if loginform.is_valid():
            request.session['login_session']= loginform.login_session
            request.session['user_dept']= loginform.user_dept
            request.session['user_name']= loginform.user_name
            request.session.set_expiry(0)
            context = {}
            login_session = request.session.get('login_session', '')

            if login_session == 'insung':
                context['login_session'] = 'insung'
                context['user_dept'] = request.session.get('user_dept')
                context['user_name'] = request.session.get('user_name')
                print('포스트, 인성로그인')
                return redirect('isscm:index')
            else:
                login_session = request.session.get('login_session')
                user_name = request.session.get('user_name')
                context = {'forms': loginform, 'login_session': login_session, 'user_name': user_name}
                print("포스트, 일반 로그인")
                return redirect('isscm:index')
        else:
            context['forms'] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'accounts/login.html', context)

# 로그아웃
def logout(request):
    request.session.flush()
    return redirect('/index')

