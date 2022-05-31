from django.shortcuts import render, redirect, get_object_or_404, reverse
from .decorators import login_required, login_ok
import sys

sys.path.append('..')
from accounts.models import User
from asregister.models import ASsheet
from question.models import question_sheet
from .models import EstimateSheet, UploadFile, Ordersheet, ProductDb, OrderUploadFile, main_sheet, sub_sheet
from . import models
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
import datetime
import xlwt
from django.http import HttpResponse
import mimetypes
import shutil
from datetime import date
from dateutil.relativedelta import relativedelta
from functools import reduce


# Create your views here.

# 메인페이지
def index(request):
    login_session = request.session.get('login_session')

    # 1일 기준 신규 접수 현황
    es_count = main_sheet.objects.filter(rg_date__gte=date.today()).count()
    es_pcount = main_sheet.objects.filter(rg_date__gte=date.today() ,
                                          cname=login_session).count()
    es_fcount = main_sheet.objects.filter(rg_date__gte=date.today(),
                                          finish="종료").count()
    es_icount = main_sheet.objects.filter(rg_date__gte=date.today(),
                                          finish="진행 중").count()
    as_count = ASsheet.objects.filter(rg_date__gte=date.today()).count()
    as_pcount = ASsheet.objects.filter(rg_date__gte=date.today(),
                                       cname=login_session).count()
    as_fcount = ASsheet.objects.filter(rp_date__gte=date.today(), finish="종료").count()
    que_count = question_sheet.objects.filter(rg_date__gte=date.today()).count()
    que_pcount = question_sheet.objects.filter(rg_date__gte=date.today(),
                                               cname=login_session).count()

    # 주간 실적 현황
    es_week1 = main_sheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                         user_dept='영업1팀').aggregate(Sum('total_price'))
    es_week2 = main_sheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                         user_dept='영업2팀').aggregate(Sum('total_price'))

    # 월간 실적 현황
    es_month1 = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                          user_dept='영업1팀').aggregate(Sum('total_price'))
    es_month2 = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                          user_dept='영업2팀').aggregate(Sum('total_price'))

    # 제품별 월간 견적, 발주, AS 개수
    es_num = sub_sheet.objects.filter(release_date__gte=date.today() - relativedelta(months=1)).values(
        'product_name').order_by('product_name').annotate(count=Sum('quantity'))
    print('날짜 : ', date.today() - relativedelta(months=1))
    es_num_sum = sub_sheet.objects.filter(release_date__gte=date.today() - relativedelta(months=1)).aggregate(
        Sum('quantity'))
    as_num = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'product_name').order_by('product_name').annotate(count=Sum('quantity'))
    as_num_sum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).aggregate(
        Sum('quantity'))

    # 업체별 월간 견적, 발주, AS 개수
    es_cnum = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'cname').order_by('cname').annotate(count=Count('cname'))
    es_cnum_sum = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'cname').order_by('cname').annotate(count=Count('cname')).aggregate(Sum('count'))
    as_cnum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values('cname').order_by(
        'cname').annotate(count=Count('cname'))
    as_cnum_sum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'cname').order_by('cname').annotate(count=Count('cname')).aggregate(Sum('count'))

    context = {'login_session': login_session, 'es_count': es_count, 'as_count': as_count,
               'que_count': que_count, 'es_icount': es_icount,
               'es_week1': es_week1, 'es_week2': es_week2,
               'es_month1': es_month1, 'es_month2': es_month2,
               'es_num': es_num,  'as_num': as_num,
               'es_cnum': es_cnum, 'as_cnum': as_cnum, 'es_fcount': es_fcount,
               'as_fcount': as_fcount, 'es_pcount': es_pcount,
               'as_pcount': as_pcount,  'que_pcount': que_pcount, 'es_num_sum': es_num_sum,
               'as_num_sum': as_num_sum, 'es_cnum_sum': es_cnum_sum,
               'as_cnum_sum': as_cnum_sum}
    return render(request, 'isscm/index.html', context)


# 제품명 검색 자동완성
def searchData(request):
    if 'term' in request.GET:
        qs = ProductDb.objects.filter(product_name__icontains=request.GET.get('term'))
        pname = list()
        for product in qs:
            pname.append(product.product_name)
        return JsonResponse(pname, safe=False)
    return render(request, 'isscm/index.html')

# 메인 입력
@login_required
def main_insert(request):
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    user_dept = request.session.get('user_dept')

    if request.method == 'GET':
        print('메인 입력 겟 들어옴')
        context = {'login_session': login_session, 'user_name': user_name, 'user_dept': user_dept}
        print('메인 입력 겟 나감')
        return render(request, 'isscm/main_insert.html', context)
    elif request.method == 'POST':
        print("메인 입력 시작")
        main = main_sheet()
        main.rp_date = request.POST['rp_date']
        main.main_title = request.POST['main_title']
        main.cname = request.POST['cname']
        main.requests = request.POST['requests']
        main.total_price = request.POST.get('total_price')
        main.finish = request.POST.get('finish', '')
        main.user_name = request.POST.get('user_name', '')
        main.user_dept = request.POST.get('user_dept', '')

        main.save()

        context = {'login_session': login_session, 'user_name': user_name, 'user_dept': user_dept}
        print('메인 입력 끝남')
        return redirect('isscm:main_insert')


def main_detail(request, pk):
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    user_dept = request.session.get('user_dept')
    detailView = get_object_or_404(main_sheet, id=pk)
    if request.method == 'GET':
        print('get 메인 디테일 뷰 시작')
        if sub_sheet.objects.filter(m_id_id=pk):
            sub = sub_sheet.objects.filter(m_id_id=pk).order_by('id')
            # 페이징
            page = request.GET.get('page', '1')
            paginator = Paginator(sub, 10)
            page_obj = paginator.get_page(page)
            print("insung GET main 페이징 끝")
            try:
                # upfile = UploadFile.objects.filter(sheet_no_id=pk)
                # 잠시 보류
                print('get 파일 있음')
                upload_file = UploadFile.objects.filter(main_id_id=pk)
                context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name,
                           'user_dept': user_dept, 'sub': sub, 'files': upload_file}
            except:
                print('get 파일 없음')
                context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name,
                           'user_dept': user_dept, 'sub': sub}
        else:
            print('sub 없음')
            context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name,
                       'user_dept': user_dept}
        print("디테일 뷰 끝")
        return render(request, 'isscm/main_detail.html', context)
    else:
        print("post 메인 디테일 뷰 / 수정 시작")
        # esView = get_object_or_404(main_sheet, id=detailView.essheet_pk)
        # 수정 내용 저장
        detailView.rp_date = request.POST['rp_date']
        detailView.main_title = request.POST['main_title']
        detailView.total_price = request.POST.get('total_price').replace(",", "")
        detailView.cname = request.POST['cname']
        detailView.requests = request.POST['requests']
        detailView.finish = request.POST.get('finish', None)
        detailView.user_dept = request.POST.get('user_dept')
        detailView.user_name = request.POST.get('user_name')

        # esView.new_old = request.POST['new_old']
        # print(esView.new_old)
        # esView.save()
        detailView.save()
        detailView = get_object_or_404(main_sheet, id=pk)
        if sub_sheet.objects.filter(m_id_id=pk):
            sub = sub_sheet.objects.filter(m_id_id=pk).order_by('id')
            # 페이징
            page = request.GET.get('page', '1')
            paginator = Paginator(sub, 10)
            page_obj = paginator.get_page(page)
            print("insung GET main 페이징 끝")
        try:
            # upfile = UploadFile.objects.filter(sheet_no_id=pk)
            # 잠시 보류
            print('post 파일 있음')
            upload_file = UploadFile.objects.filter(main_id_id=pk)
            context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name,
                       'user_dept': user_dept, 'sub': sub, 'files': upload_file}
        except:
            print('post 파일 없음')
            context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name,
                       'user_dept': user_dept, 'sub': sub}
        return render(request, 'isscm/main_detail.html', context)


# main 삭제
def main_delete(request, pk):
    detailView = get_object_or_404(main_sheet, id=pk)
    detailView.delete()
    print('삭제완료')
    return redirect('isscm:main_list')


# main 리스트
@login_required
def main_list(request):
    print("main 리스트 시작")
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    user_dept = request.session.get('user_dept')

    if request.method == 'GET':
        if login_session == 'insung':
            print('get insung 리스트 시작')
            sort = request.GET.get('sort', '')
            query = request.GET.get('q', '')
            if sort == 'rg_date':
                m_sheet = main_sheet.objects.all().order_by('-rg_date')
            elif sort == 'rp_date':
                m_sheet = main_sheet.objects.all().order_by('-rp_date')
            elif sort == 'main_title':
                m_sheet = main_sheet.objects.all().order_by('-main_title', '-rg_date')
            elif sort == 'requests':
                m_sheet = main_sheet.objects.all().order_by('-requests', '-rg_date', )
            elif sort == 'cname':
                m_sheet = main_sheet.objects.all().order_by('-cname', '-rg_date')
            elif sort == 'finish':
                m_sheet = main_sheet.objects.all().order_by('-finish', '-rg_date')
            elif sort == 'total_price':
                m_sheet = main_sheet.objects.all().order_by('-total_price', '-rg_date')
            elif sort == 'user_dept':
                m_sheet = main_sheet.objects.all().order_by('-user_dept', '-rg_date')
            elif sort == 'user_name':
                m_sheet = main_sheet.objects.all().order_by('-user_name', '-rg_date')
            elif sort == 'all':
                m_sheet = main_sheet.objects.all().order_by('-rg_date', 'finish', '-user_dept')
            else:
                print("리스트 조회 겸 목록 조회")
                search_sort = request.GET.get('search_sort', '')
                if search_sort == 'main_title':
                    m_sheet = main_sheet.objects.all().filter(Q(main_title__icontains=query)).order_by('-rg_date',
                                                                                                       'finish',
                                                                                                       '-user_dept')
                elif search_sort == 'requests':
                    m_sheet = main_sheet.objects.all().filter(Q(requests__icontains=query)).order_by('-rg_date',
                                                                                                     'finish',
                                                                                                     '-user_dept')
                elif search_sort == 'cname':
                    m_sheet = main_sheet.objects.all().filter(Q(cname__icontains=query)).order_by('-rg_date', 'finish',
                                                                                                  '-user_dept')
                elif search_sort == 'finish':
                    m_sheet = main_sheet.objects.all().filter(Q(finish__icontains=query)).order_by('-rg_date', 'finish',
                                                                                                   '-user_dept')
                elif search_sort == 'user_dept':
                    m_sheet = main_sheet.objects.all().filter(Q(user_dept__icontains=query)).order_by('-rg_date',
                                                                                                      'finish',
                                                                                                      '-user_dept')
                elif search_sort == 'user_name':
                    m_sheet = main_sheet.objects.all().filter(Q(user_name__icontains=query)).order_by('-rg_date',
                                                                                                      'finish',
                                                                                                      '-user_dept')
                elif search_sort == 'user_name':
                    m_sheet = main_sheet.objects.all().filter(Q(user_name__icontains=query)).order_by('-rg_date',
                                                                                                      'finish',
                                                                                                      '-user_dept')
                elif search_sort == 'serial':
                    s_sheet = sub_sheet.objects.all().filter(Q(serial__icontains=query)).order_by('id')
                    v = []
                    for i in s_sheet:
                        sm = i.m_id_id
                        ms = main_sheet.objects.filter(id__icontains=sm)
                        #리스트 추가(앞에 추가함)
                        v = list(ms) + v
                    #중복 제거
                    m_sheet = reduce(lambda acc, cur: acc if cur in acc else acc + [cur], v, [])


                else:
                    m_sheet = main_sheet.objects.all().order_by('-rg_date', 'finish', '-user_dept')

            # 한달이상 미처리건 조회
            over_date = main_sheet.objects.filter(rg_date__lte=date.today() - relativedelta(months=1)).exclude(
                finish='종료').order_by('-rg_date')

            # 페이징f
            page = request.GET.get('page', '1')
            paginator = Paginator(m_sheet, 10)
            page_obj = paginator.get_page(page)
            print("insung GET main 페이징 끝")

            # 차트 데이터
            # sheet_chart = []
            # sheet_chart_data = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(weeks=1))
            # dept_1 = sheet_chart_data.filter(user_dept="영업1팀").count()
            # dept_2 = sheet_chart_data.filter(user_dept="영업2팀").count()
            # sheet_chart = [dept_1, dept_2]

            # 주간 팀별 실적 현황
            # es_week1 = main_sheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
            #                                      user_dept='영업1팀').aggregate(Sum('total_price'))
            # es_week2 = main_sheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
            #                                      user_dept='영업2팀').aggregate(Sum('total_price'))
            # es_week3 = main_sheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1)).aggregate(
            #     Sum('total_price'))
            # # 월간 팀별 실적 조회
            # es_month1 = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
            #                                       user_dept='영업1팀').aggregate(Sum('total_price'))
            # es_month2 = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
            #                                       user_dept='영업2팀').aggregate(Sum('total_price'))
            # es_month3 = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).aggregate(
            #     Sum('total_price'))

            # 주간 담당자별 실적 현황
            # es_cweek1_total = main_sheet.objects.filter(rg_date__gte=date.today() - relativedelta(weeks=1)).exclude(
            #     user_dept=None).values(
            #     'user_name').order_by('user_name').distinct().annotate(sum=Sum('total_price'))
            # es_cweek1_sum = main_sheet.objects.filter(
            #     rg_date__gte=date.today() - relativedelta(weeks=1)).distinct().values(
            #     'user_name').aggregate(Sum('total_price'))
            # # 월간 담당자별 실적 현황
            # es_cmonth1_total = main_sheet.objects.filter(
            #     rg_date__gte=date.today() - relativedelta(months=1)).exclude(user_dept=None).values(
            #     'user_name').order_by('user_name').distinct().annotate(sum=Sum('total_price'))
            # es_cmonth1_sum = main_sheet.objects.filter(
            #     rg_date__gte=date.today() - relativedelta(months=1)).distinct().values('user_name').aggregate(
            #     Sum('total_price'))

            # context = {'login_session': login_session, 'page_obj': page_obj, 'sheet_chart': sheet_chart, 'sort': sort,
            #            'es_month1': es_month1, 'es_month2': es_month2, 'es_week1': es_week1, 'es_week2': es_week2,
            #            'es_cweek1_total': es_cweek1_total, 'es_cmonth1_total': es_cmonth1_total, 'es_week3': es_week3,
            #            'es_month3': es_month3, 'over_date': over_date, 'query': query, 'search_sort': search_sort,
            #            'es_cweek1_sum': es_cweek1_sum, 'es_cmonth1_sum': es_cmonth1_sum}
            context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort, 'over_date': over_date,
                       'query': query, 'search_sort': search_sort}

        else:
            sort = request.GET.get('sort', '')
            query = request.GET.get('q', '')
            if sort == 'rg_date':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('-rg_date')
            elif sort == 'rp_date':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('-rp_date')
            elif sort == 'main_title':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('-main_title', '-rg_date')
            elif sort == 'requests':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('-requests', '-rg_date')
            elif sort == 'cname':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('cname', '-rg_date')
            elif sort == 'total_price':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('total_price', '-rg_date')
            elif sort == 'finish':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('finish', '-rg_date')
            elif sort == 'all':
                m_sheet = main_sheet.objects.filter(cname=login_session).order_by('-rg_date', 'finish')
            else:
                print("리스트 조회 겸 목록 조회")
                search_sort = request.GET.get('search_sort', '')
                if search_sort == 'main_title':
                    m_sheet = main_sheet.objects.all().filter(Q(main_title__icontains=query),
                                                              cname=login_session).order_by('-rg_date',
                                                                                            'finish',
                                                                                            '-user_dept')
                elif search_sort == 'requests':
                    m_sheet = main_sheet.objects.all().filter(Q(requests__icontains=query),
                                                              cname=login_session).order_by('-rg_date',
                                                                                            'finish',
                                                                                            '-user_dept')
                elif search_sort == 'finish':
                    m_sheet = main_sheet.objects.all().filter(Q(finish__icontains=query), cname=login_session).order_by(
                        '-rg_date',
                        'finish',
                        '-user_dept')
                elif search_sort == 'all':
                    m_sheet = main_sheet.objects.filter(Q(requests__icontains=query) | Q(finish__icontains=query) |
                                                        Q(main_title__icontains=query), cname=login_session).order_by(
                        '-rg_date', 'finish')
                else:
                    m_sheet = main_sheet.objects.filter(cname=login_session).order_by('-rg_date', 'finish')

            page = request.GET.get('page', '1')
            paginator = Paginator(m_sheet, 10)
            page_obj = paginator.get_page(page)
            print("일반 GET main 페이징 끝")
            context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort, 'query': query,
                       'search_sort': search_sort,
                       'user_name': user_name, 'user_dept': user_dept}

        print('메인 리스트 끝')
        return render(request, 'isscm/main_list.html', context)
    elif request.method == 'POST':
        print('post 확인 필요')
        return redirect('isscm/main_list')


# sub 입력
def sub_insert(request, pk):
    print('sub 입력 시작')
    login_session = request.session.get('login_session')
    user_dept = request.session.get('user_dept')
    user_name = request.session.get('user_name')
    detailView = get_object_or_404(main_sheet, id=pk)

    if request.method == 'GET':
        print('sub 겟 들어옴')
        context = {'login_session': login_session, 'user_dept': user_dept, 'user_name': user_name,
                   'detailView': detailView}
        print('겟 끝나 나감')
        return render(request, 'isscm/sub_insert.html', context)
    elif request.method == 'POST':
        print("sub post 입력 시작")
        s_sheet = sub_sheet()
        s_sheet.product_name = request.POST['product_name']
        s_sheet.quantity = request.POST['quantity'].replace(",", "")
        s_sheet.per_price = request.POST.get('per_price').replace(",", "")
        s_sheet.tax = request.POST.get('tax').replace(",", "")
        s_sheet.total_price = request.POST.get('total_price').replace(",", "")
        if request.POST['production_date'] == "" or request.POST['release_date'] == "":
            print("날짜 미입력")
        else:
            print('날짜 입력')
            s_sheet.production_date = request.POST['production_date']
            s_sheet.release_date = request.POST['release_date']
        s_sheet.cname = request.POST['cname']
        if request.POST['release_date'] != "":
            re_date = request.POST['release_date']
            warranty = datetime.datetime.strptime(re_date, '%Y-%m-%d') + relativedelta(years=3)
            s_sheet.warranty = warranty
        elif request.POST['release_date'] == "":
            print('서브 출고일 입력안됨')

        s_sheet.serial = request.POST['serial']
        s_sheet.user_dept = request.POST['user_dept']
        s_sheet.user_name = request.POST['user_name']
        s_sheet.m_id = main_sheet.objects.get(id=pk)
        s_sheet.m_title = request.POST['main_title']

        s_sheet.save()

    if sub_sheet.objects.filter(m_id_id=pk):
        sub = sub_sheet.objects.filter(m_id_id=pk).order_by('id')
        # 페이징
        page = request.GET.get('page', '1')
        paginator = Paginator(sub, 10)
        page_obj = paginator.get_page(page)
        print("insung GET main 페이징 끝")

    sub_total = sub_sheet.objects.filter(m_id_id=pk).distinct().values(
        'm_id_id').aggregate(Sum('total_price'))
    detailView.total_price = sub_total['total_price__sum']
    detailView.save()

    context = {'login_session': login_session, 'user_name': user_name, 'user_dept': user_dept, 'detailView': detailView,
               'sub': sub}
    print('sub post 입력 종료')
    return render(request, 'isscm/main_detail.html', context)


def sub_modify(request, pk, mid):
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    user_dept = request.session.get('user_dept')
    detailView = get_object_or_404(main_sheet, id=mid)
    sub_detailView = get_object_or_404(sub_sheet, id=pk)
    if request.method == 'GET':
        print('get sub detail 뷰 시작')
        try:
            # upfile = UploadFile.objects.filter(sheet_no_id=pk)
            # 잠시 보류
            context = {'sub_detailView': sub_detailView, 'login_session': login_session, 'user_name': user_name,
                       'user_dept': user_dept}
        except:
            context = {'sub_detailView': sub_detailView, 'login_session': login_session, 'user_name': user_name,
                       'user_dept': user_dept}
        print("디테일 뷰 끝")
        return render(request, 'isscm/sub_modify.html', context)
    else:
        print("post sub detail 뷰 / 수정 시작")
        # 수정 내용 저장
        sub_detailView.product_name = request.POST['product_name']
        sub_detailView.per_price = request.POST.get('per_price').replace(",", "")
        sub_detailView.quantity = request.POST.get('quantity').replace(",", "")
        sub_detailView.tax = request.POST.get('tax').replace(",", "")
        sub_detailView.total_price = request.POST.get('total_price').replace(",", "")

        if request.POST['production_date'] == "" or request.POST['release_date'] == "":
            print("날짜 미입력")
        else:
            print('날짜 입력')
            sub_detailView.production_date = request.POST['production_date']
            sub_detailView.release_date = request.POST['release_date']
        sub_detailView.cname = request.POST['cname']
        if request.POST['release_date'] != "":
            re_date = request.POST['release_date']
            warranty = datetime.datetime.strptime(re_date, '%Y-%m-%d') + relativedelta(years=3)
            print(warranty)
            sub_detailView.warranty = warranty
        elif request.POST['release_date'] == "":
            print('서브 출고일 입력안됨')

        sub_detailView.serial = request.POST['serial']
        sub_detailView.user_dept = request.POST['user_dept']
        sub_detailView.user_name = request.POST['user_name']
        print("수정 저장완료")
        sub_detailView.save()

        sub_total = sub_sheet.objects.filter(m_id_id=mid).distinct().values(
            'm_id_id').aggregate(Sum('total_price'))
        detailView.total_price = sub_total['total_price__sum']
        detailView.save()



    global page_obj
    sub = sub_sheet.objects.all().filter(m_id_id=mid).order_by('id')
    # 페이징
    page = request.GET.get('page', '1')
    paginator = Paginator(sub, 10)
    page_obj = paginator.get_page(page)

    detailView = get_object_or_404(main_sheet, id=mid)
    print('detailView : ', detailView.id)

    print("insung GET main 페이징 끝")
    context = {'sub_detailView': sub_detailView, 'login_session': login_session, 'user_name': user_name,
               'user_dept': user_dept, 'sub': sub, 'detailView': detailView}
    return render(request, 'isscm/main_detail.html', context)


# sub 삭제
def sub_delete(request, pk, mid):
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    user_dept = request.session.get('user_dept')
    sub = sub_sheet.objects.all().filter(m_id_id=mid).order_by('id')

    detailView = get_object_or_404(sub_sheet, id=pk)
    detailView.delete()
    print('삭제완료')

    detailView = get_object_or_404(main_sheet, id=mid)

    context = {'login_session': login_session, 'user_name': user_name,
               'user_dept': user_dept, 'sub': sub, 'detailView': detailView}
    return render(request, 'isscm/main_detail.html', context)


# main 엑셀 다운로드
def main_excel(request):
    login_session = request.session.get('login_session')

    print("main 다운로드 시작")
    # 데이터 db에서 불러옴
    # data = EstimateSheet.objects.all()
    response = HttpResponse(content_type="application/vnd.ms-excel")
    # 다운로드 받을 때 생성될 파일명 설정
    response["Content-Disposition"] = 'attachment; filename=' \
                                      + str(datetime.date.today()) + '_mainsheet.xls'
    print("다운 중간")
    # 인코딩 설정
    wb = xlwt.Workbook(encoding='utf-8')
    # 생성될 시트명 설정
    ws = wb.add_sheet('main')

    # 엑셀 스타일: 첫번째 열(=title)과 나머지 열(=data) 구분 위한 설정
    title_style = xlwt.easyxf(
        'pattern: pattern solid, fore_color indigo; align: horizontal center; font: color_index white;')
    data_style = xlwt.easyxf('align: horizontal right')
    # 날짜 서식 결정
    styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
              'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
              'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
              'default': xlwt.Style.default_style}
    # 첫번째 열에 들어갈 컬럼명 설정
    col_names = ['등록 일자', '마감 요청 일자', '견적명', '업체명', '요청 사항', '총 금액', '종료 여부', '담당 팀', '담당자']

    query = request.GET.get('q')
    print('que : ', query)
    search_sort = request.GET.get('search_sort', '')
    print('search : ', search_sort)
    if search_sort:
        print('검색으로 다운로드')
        if login_session == 'insung':
            print('insung search 다운')
            if search_sort == 'main_title':
                rows = main_sheet.objects.all().filter(Q(main_title__icontains=query)).values_list('rg_date',
                                                                                                   'rp_date',
                                                                                                   'main_title',
                                                                                                   'cname', 'requests',
                                                                                                   'total_price',
                                                                                                   'finish',
                                                                                                   'user_dept',
                                                                                                   'user_name')
            elif search_sort == 'requests':
                rows = main_sheet.objects.all().filter(Q(requests__icontains=query)).values_list('rg_date',
                                                                                                 'rp_date',
                                                                                                 'main_title', 'cname',
                                                                                                 'requests',
                                                                                                 'total_price',
                                                                                                 'finish', 'user_dept',
                                                                                                 'user_name')
            elif search_sort == 'cname':
                rows = main_sheet.objects.all().filter(Q(cname__icontains=query)).values_list('rg_date',
                                                                                              'rp_date',
                                                                                              'main_title', 'cname',
                                                                                              'requests', 'total_price',
                                                                                              'finish', 'user_dept',
                                                                                              'user_name')
            elif search_sort == 'finish':
                rows = main_sheet.objects.all().filter(Q(finish__icontains=query)).values_list('rg_date',
                                                                                               'rp_date',
                                                                                               'main_title', 'cname',
                                                                                               'requests',
                                                                                               'total_price',
                                                                                               'finish', 'user_dept',
                                                                                               'user_name')
            elif search_sort == 'user_dept':
                rows = main_sheet.objects.all().filter(Q(user_dept__icontains=query)).values_list('rg_date',
                                                                                                  'rp_date',
                                                                                                  'main_title', 'cname',
                                                                                                  'requests',
                                                                                                  'total_price',
                                                                                                  'finish', 'user_dept',
                                                                                                  'user_name')
            elif search_sort == 'user_name':
                rows = main_sheet.objects.all().filter(Q(user_name__icontains=query)).values_list('rg_date',
                                                                                                  'rp_date',
                                                                                                  'main_title', 'cname',
                                                                                                  'requests',
                                                                                                  'total_price',
                                                                                                  'finish', 'user_dept',
                                                                                                  'user_name')
            elif search_sort == 'all':
                rows = main_sheet.objects.all().filter(
                    Q(requests__icontains=query) | Q(cname__icontains=query) | Q(finish__icontains=query) |
                    Q(main_title__icontains=query) | Q(user_dept__icontains=query) |
                    Q(user_name__icontains=query)).values_list('rg_date', 'rp_date',
                                                               'main_title', 'cname', 'requests', 'total_price',
                                                               'finish', 'user_dept', 'user_name')
        else:
            print('일반 search 다운')
            if search_sort == 'main_title':
                rows = main_sheet.objects.all().filter(Q(main_title__icontains=query),
                                                       cname=login_session).values_list('rg_date', 'rp_date',
                                                                                        'main_title', 'cname', 'requests', 'total_price',
                                                                                        'finish', 'user_dept', 'user_name')
            elif search_sort == 'requests':
                rows = main_sheet.objects.all().filter(Q(requests__icontains=query),
                                                       cname=login_session).values_list('rg_date', 'rp_date',
                                                                                        'main_title', 'cname', 'requests', 'total_price',
                                                                                        'finish', 'user_dept', 'user_name')
            elif search_sort == 'finish':
                rows = main_sheet.objects.all().filter(Q(finish__icontains=query), cname=login_session).values_list('rg_date', 'rp_date',
                                                                                                                    'main_title', 'cname', 'requests', 'total_price',
                                                                                                                    'finish', 'user_dept', 'user_name')
            elif search_sort == 'all':
                rows = main_sheet.objects.filter(Q(requests__icontains=query) | Q(finish__icontains=query) |
                                                 Q(main_title__icontains=query), cname=login_session).values_list('rg_date', 'rp_date',
                                                                                                                  'main_title', 'cname', 'requests', 'total_price',
                                                                                                                  'finish', 'user_dept', 'user_name')
    else:
        print('전체 다운로드')
        if login_session == 'insung':
            rows = main_sheet.objects.all().values_list('rg_date', 'rp_date',
                                                        'main_title', 'cname', 'requests', 'total_price',
                                                        'finish', 'user_dept', 'user_name')
        else:
            rows = main_sheet.objects.all().filter(cname=login_session).values_list('rg_date', 'rp_date',
                                                                                    'main_title', 'cname', 'requests', 'total_price',
                                                                                    'finish', 'user_dept', 'user_name')

    # 첫번째 열: 설정한 컬럼명 순서대로 스타일 적용하여 생성
    print("다운 중간2")
    row_num = 0
    ix = 0
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name, title_style)

    # 두번째 이후 열: 설정한 컬럼명에 맞춘 데이터 순서대로 스타일 적용하여 생성
    for row in rows:
        row_num += 1
        for col_num, attr in enumerate(row):
            if isinstance(attr, datetime.datetime) or isinstance(attr, date):
                cell_style = styles['date']
            else:
                cell_style = styles['default']
            ws.write(row_num, col_num, attr, cell_style)

    wb.save(response)
    print("다운로드 끝")
    return response


# sub 엑셀 다운로드
def sub_excel(request):
    login_session = request.session.get('login_session')

    print("sub 다운로드 시작")
    # 데이터 db에서 불러옴
    # data = EstimateSheet.objects.all()
    response = HttpResponse(content_type="application/vnd.ms-excel")
    # 다운로드 받을 때 생성될 파일명 설정
    response["Content-Disposition"] = 'attachment; filename=' \
                                      + str(datetime.date.today()) + '_subsheet.xls'
    print("다운 중간")
    # 인코딩 설정
    wb = xlwt.Workbook(encoding='utf-8')
    # 생성될 시트명 설정
    ws = wb.add_sheet('sub')

    # 엑셀 스타일: 첫번째 열(=title)과 나머지 열(=data) 구분 위한 설정
    title_style = xlwt.easyxf(
        'pattern: pattern solid, fore_color indigo; align: horizontal center; font: color_index white;')
    data_style = xlwt.easyxf('align: horizontal right')
    # 날짜 서식 결정
    styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
              'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
              'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
              'default': xlwt.Style.default_style}
    # 첫번째 열에 들어갈 컬럼명 설정
    col_names = ['제품명', '수량', '개당 단가', '부가세', '총 금액', '생산 일자', '출고 일자', '업체명', '시리얼', '보증 기간', '메인 번호', '메인 Title']

    m_id = request.GET.get('id')
    print("이건 뭘까", login_session)
    rows = sub_sheet.objects.filter(m_id_id=m_id).values_list('product_name', 'quantity','per_price', 'tax', 'total_price', 'production_date',
                                                              'release_date', 'cname', 'serial', 'warranty', 'm_id', 'm_title')

    # 첫번째 열: 설정한 컬럼명 순서대로 스타일 적용하여 생성
    print("다운 중간2")
    row_num = 0
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name, title_style)

    # 두번째 이후 열: 설정한 컬럼명에 맞춘 데이터 순서대로 스타일 적용하여 생성
    for row in rows:
        row_num += 1
        for col_num, attr in enumerate(row):
            if isinstance(attr, datetime.datetime) or isinstance(attr, date):
                cell_style = styles['date']
            else:
                cell_style = styles['default']
            ws.write(row_num, col_num, attr, cell_style)

    wb.save(response)
    print("다운로드 끝")
    return response


# 견적 파일 업로드/다운로드
def main_uploadFile(request, pk):
    print("오나요")
    login_session = request.session.get('login_session')
    print("여기 오나요")

    if request.method == "POST":
        if request.FILES.get('uploadedFile') is not None:
            if get_object_or_404(main_sheet, id=pk):
                print("pk 왓나요", pk)
                # 템플릿에서 데이터 가져오기
                cname = login_session
                fileTitle = request.POST["fileTitle"]
                uploadedFile = request.FILES.get('uploadedFile')
                main_id = main_sheet.objects.get(id=pk)
                menu = request.POST["menu"]

                # DB에 저장
                uploadfile = models.UploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    main_id=main_id,
                    menu=menu
                )
                uploadfile.save()
    else:
        print("get 으로 왓나", pk)
        detailView = get_object_or_404(main_sheet, id=pk)
        uploadfile = UploadFile.objects.filter(main_id=pk)
        no = pk
        context = {'login_session': login_session, 'no': no, 'detailView': detailView, 'files': uploadfile}
        print("겟 다 나갓나")
        return render(request, "isscm/file_upload.html", context)

    uploadfile = UploadFile.objects.filter(main_id=pk)
    detailView = get_object_or_404(main_sheet, id=pk)

    return render(request, "isscm/file_upload.html", context={
        "files": uploadfile, "login_session": login_session, 'detailView': detailView})


# 파일 다운로드
def main_downloadfile(request, pk):
    upload_file = get_object_or_404(UploadFile, no=pk)
    file = upload_file.uploadedFile
    name = file.name
    response = HttpResponse(content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={name}'
    shutil.copyfileobj(file, response)
    return response



# 견적 파일 삭제
def main_file_delete(request, pk):
    login_session = request.session.get('login_session')
    sheetfile = get_object_or_404(UploadFile, no=pk)
    page_no = sheetfile.main_id_id
    print(page_no)
    if sheetfile.cname == login_session or login_session == 'insung':
        sheetfile.delete()
        print('삭제완료')
        return redirect(f'/main_uploadFile/{page_no}')
    else:
        print("삭제 됨?")
        return redirect(f'/main_detail/{pk}')