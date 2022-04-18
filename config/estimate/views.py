from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Company
import re
from django.views.generic import ListView
from .pagination import pagination


def index(request):
    return render(request, 'estimate/index.html')


def cinsert(request):
    if request.method == 'GET':
        return render(request, 'estimate/company_insert.html')
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
    # 아직 목록페이지 없어서 보류
    return render(request, 'estimate/index.html')


def clist(request):
    all_boards = Company.objects.all().order_by("-no")  # 모든 데이터 조회, 내림차순(-표시) 조회
    context = {
        'company_list': all_boards
    }
    return render(request, 'estimate/company_list.html', context)


def board_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    page = pagination(request, clist)
    context.update(page)

    return render(request, 'estimate/company_list.html', context)
