from django.shortcuts import render, redirect, get_object_or_404
from isscm.decorators import login_required
from .models import question_sheet, question_comment, que_UploadFile
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.

# 임시 메인페이지
def index(request):
    login_session = request.session.get('login_session')
    return render(request, 'isscm/index.html', {'login_session': login_session})


# 문의글 입력
@login_required
def que_insert(request):
    print('as 입력 도달')

    if request.method == 'GET':
        print('겟 도달')
        login_session = request.session.get('login_session')
        context = {'login_session': login_session}
        print('겟 끝나 나감')
        return render(request, 'question/que_insert.html', context)
    elif request.method == 'POST':
        print("입력 시작")
        insert = question_sheet()
        insert.title = request.POST['title']
        insert.cname = request.POST['cname']
        insert.type = request.POST['type']
        insert.content = request.POST['content']

        insert.save()

        login_session = request.session.get('login_session')
        context = {'login_session': login_session}
        print('입력 끝나 나감')
        return render(request, 'question/que_insert.html', context)

# 문의글 상세 뷰
def que_detail(request, pk):
    if request.method == 'GET':
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(question_sheet, no=pk)

        #upfile = get_object_or_404(UploadFile, sheet_no_id=pk)
        try:
            upfile = que_UploadFile.objects.filter(que_no=pk)
            context = {'detailView': detailView, 'login_session': login_session, 'upfile': upfile}
            print("성공")
        except:
            context = {'detailView': detailView, 'login_session': login_session}
            print("실패")

        print("문의글 상세 뷰 들어감")
    else:
        print("설마 포스트")
    return render(request, 'isscm/sheet_detail.html', context)


# 문의글 리스트
@login_required
def sheet_list(request):
    print("문의글 리스트 시작")
    login_session = request.session.get('login_session')

    if request.method == 'GET':
        if login_session == 'insung':
            sort = request.GET.get('sort', '')
            if sort == 'rg_date':
                company_sheet = question_sheet.objects.all().order_by('rg_date')
            elif sort == 'rp_date':
                company_sheet = question_sheet.objects.all().order_by('rp_date')
            elif sort == 'estitle':
                company_sheet = question_sheet.objects.all().order_by('estitle')
            elif sort == 'new_old':
                company_sheet = question_sheet.objects.all().order_by('new_old')
            elif sort == 'cname':
                company_sheet = question_sheet.objects.all().order_by('cname')
            elif sort == 'finish':
                company_sheet = question_sheet.objects.all().order_by('finish')
            elif sort == 'user_dept':
                company_sheet = question_sheet.objects.all().order_by('-user_dept')
            else:
                company_sheet = question_sheet.objects.all().order_by('user_dept', 'rg_date', 'rp_date')

            # 페이징
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("insung GET 페이징 끝")

            context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort}

        else:
            sort = request.GET.get('sort', '')
            if sort == 'rg_date':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('rg_date')
            elif sort == 'rp_date':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('rp_date')
            elif sort == 'estitle':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('estitle')
            elif sort == 'new_old':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('new_old')
            elif sort == 'cname':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('cname')
            elif sort == 'finish':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('finish')
            elif sort == 'all':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date',
                                                                                           'finish')
            else:
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('user_dept', 'rg_date',
                                                                                           'rp_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("일반 GET 페이징 끝")
            context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort}

        print('끝')
        return render(request, 'question/que_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        if login_session == 'insung':
            company_sheet = question_sheet.objects.all().order_by('user_dept', 'rg_date', 'rp_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        else:
            company_sheet = question_sheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        context = {'company_sheet': company_sheet, 'login_session': login_session, 'page_obj': page_obj}
        print("리스트 끝")
        return render(request, 'question/que_list.html', context)


# 문의글 리스트 검색
def searchResult(request):
    login_session = request.session.get('login_session')
    searchlist = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('get?')
        searchlist = question_sheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                finish__icontains=query))
        print("여기 왓나")
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
        page_obj = paginator.get_page(page)
        print("지나갓나")
        return render(request, 'question/que_list.html',
                      {'query': query, 'page_obj': page_obj, 'login_session': login_session})
    else:
        print('post로 왓나')
        query = request.GET.get('query')
        print(query)
        searchlist = question_sheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                finish__icontains=query))
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
        page_obj = paginator.get_page(page)
        context = {'query': query, 'page_obj': page_obj, 'login_session': login_session}
        print('포스트 나갓나')
    return render(request, 'question/que_list.html', context)


