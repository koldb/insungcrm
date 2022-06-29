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
            user = User(
                user_id=register_form.user_id,
                cname=register_form.cname,
                user_name = register_form.user_name,
                user_pw=register_form.user_pw,
                user_phone=register_form.user_phone,
                user_email=register_form.user_email,
                user_dept=register_form.user_dept
            )
            # 입력한 정보 저장
            user.save()
            login_session = request.session.get('login_session')
            context = {'forms': register_form, 'login_session': login_session}
            #return render(request, 'accounts/login.html', context) 데이터 넘길 필요없기에 redirect로 수정
            return redirect('accounts:login')
        else:
            #에러 메세지 전달
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
    user_phone = request.session.get('user_phone')
    user_dept = request.session.get('user_dept')
    context = { 'forms': loginform, 'login_session': login_session, 'user_name':user_name, 'user_phone': user_phone, 'user_dept': user_dept }

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
            request.session['user_phone']= loginform.user_phone
            #session 유지시간 / 0 이면 창 닫힐때까지 유지
            request.session.set_expiry(0)
            context = {}
            login_session = request.session.get('login_session', '')

            if login_session == 'insung':
                context['login_session'] = 'insung'
                context['user_dept'] = request.session.get('user_dept')
                context['user_name'] = request.session.get('user_name')
                context['user_phone'] = request.session.get('user_phone')
                print('포스트, 인성로그인')
                return redirect('isscm:index')
                #return render(request, 'isscm/index.html', context)
            else:
                login_session = request.session.get('login_session')
                user_name = request.session.get('user_name')
                user_phone = request.session.get('user_phone')
                context = {'forms': loginform, 'login_session': login_session, 'user_name': user_name, 'user_phone': user_phone}
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
    #session data 삭제
    request.session.flush()
    return redirect('/index')

