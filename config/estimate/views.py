from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Company
from .pagination import pagination

# 임시 메인 페이지
def index(request):
    # 현재 미사용
    return render(request, 'estimate/index.html')

# 업체 정보 등록
def cinsert(request):
    login_session = request.session.get('login_session')
    context = {'login_session': login_session}
    if login_session == 'insung':
        if request.method == 'GET':
            login_session = request.session.get('login_session')
            context = {'login_session': login_session}
            return render(request, 'estimate/company_insert.html', context)
        elif request.method == 'POST':

            insert = Company()
            insert.cname = request.POST['cname']
            insert.cmanager = request.POST['cmanager']
            insert.smanager = request.POST['smanager']
            insert.phone = request.POST['phone']
            insert.email = request.POST['email']
            insert.adress = request.POST['adress']
            insert.homepage = request.POST['homepage']

            insert.save()

            login_session = request.session.get('login_session')
            context = {'login_session': login_session}
            return render(request, 'estimate/company_insert.html', context)
    return render(request, 'estimate/index.html', context)

# 업체 정보 리스트
def clist(request):
    all_boards = Company.objects.all().order_by("-no")
    login_session = request.session.get('login_session')
    context = {
        'company_list': all_boards,
        'login_session': login_session
    }
    return render(request, 'estimate/company_list.html', context)

