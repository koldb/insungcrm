from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Company
from .pagination import pagination


def index(request):
    return render(request, 'estimate/index.html')


def cinsert(request):
    login_session = request.session.get('login_session')
    # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
    context = {'login_session': login_session}
    if login_session == 'insung':
        if request.method == 'GET':
            login_session = request.session.get('login_session')
            #render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
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
            # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
            context = {'login_session': login_session}
            return render(request, 'estimate/company_insert.html', context)
    return render(request, 'estimate/index.html', context)


def clist(request):
    all_boards = Company.objects.all().order_by("-no")  # 모든 데이터 조회, 내림차순(-표시) 조회
    login_session = request.session.get('login_session')
    context = {
        'company_list': all_boards,
        'login_session': login_session
    }
    return render(request, 'estimate/company_list.html', context)


def board_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    page = pagination(request, clist)
    context.update(page)

    return render(request, 'estimate/company_list.html', context)
