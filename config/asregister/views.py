from django.shortcuts import render, redirect, get_object_or_404, reverse
import sys

sys.path.append('..')
from isscm.decorators import login_required
from . import models
from .models import ASsheet, ASUploadFile
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
import datetime
import xlwt
from django.http import HttpResponse
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# Create your views here.

# 임시 메인페이지
def index(request):
    login_session = request.session.get('login_session')
    return render(request, 'isscm/index.html', {'login_session': login_session})


# AS 입력
@login_required
def as_insert(request):
    print('as 입력 도달')
    login_session = request.session.get('login_session')
    # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
    context = {'login_session': login_session}

    if request.method == 'GET':
        print('겟 도달')
        login_session = request.session.get('login_session')
        # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
        context = {'login_session': login_session}
        print('겟 끝나 나감')
        return render(request, 'assheet/as_insert.html', context)
    elif request.method == 'POST':
        print("입력 시작")
        insert = ASsheet()
        insert.cname = request.POST['cname']
        insert.product_name = request.POST['product_name']
        insert.quantity = request.POST['quantity']
        insert.memo = request.POST['memo']

        insert.save()

        login_session = request.session.get('login_session')
        context = {'login_session': login_session}
        print('입력 끝나 나감')
        return render(request, 'assheet/as_insert.html', context)


# AS 접수건 리스트
@login_required
def as_list(request):
    print("리스트 시작")
    login_session = request.session.get('login_session')

    if request.method == 'GET':
        if login_session == 'insung':
            sort = request.GET.get('sort', '')
            query = request.GET.get('q', '')
            if sort == 'rg_date':
                company_sheet = ASsheet.objects.all().order_by('-rg_date')
            elif sort == 'rp_date':
                company_sheet = ASsheet.objects.all().order_by('-rp_date')
            elif sort == 'product_name':
                company_sheet = ASsheet.objects.all().order_by('-product_name', '-rg_date')
            elif sort == 'finish':
                company_sheet = ASsheet.objects.all().order_by('-finish', '-rg_date')
            elif sort == 'cname':
                company_sheet = ASsheet.objects.all().order_by('-cname', '-rg_date')
            elif sort == 'all':
                company_sheet = ASsheet.objects.all().order_by('-rg_date', 'finish')
            else:
                print("리스트 조회 겸 목록 조회")
                search_sort = request.GET.get('search_sort', '')
                if search_sort == 'cname':
                    company_sheet = ASsheet.objects.all().filter(Q(cname__icontains=query)).order_by('-rg_date',
                                                                                                     'finish')
                elif search_sort == 'product_name':
                    company_sheet = ASsheet.objects.all().filter(Q(product_name__icontains=query)).order_by('-rg_date',
                                                                                                            'finish')
                elif search_sort == 'finish':
                    company_sheet = ASsheet.objects.all().filter(Q(finish__icontains=query)).order_by('-rg_date',
                                                                                                      'finish')
                elif search_sort == 'memo':
                    company_sheet = ASsheet.objects.all().filter(Q(memo__icontains=query)).order_by('-rg_date',
                                                                                                    'finish')
                elif search_sort == 'all':
                    company_sheet = ASsheet.objects.all().filter(
                        Q(product_name__icontains=query) | Q(memo__icontains=query) | Q(cname__icontains=query) | Q(
                            finish__icontains=query) | Q(option__icontains=query)).order_by('-rg_date', 'finish')
                else:
                    company_sheet = ASsheet.objects.all().order_by('-rg_date', 'finish')

            # 한달이상 미처리건 조회
            over_as = ASsheet.objects.filter(rg_date__lte=date.today() - relativedelta(months=1)).exclude(
                finish='종료').order_by('-rg_date')

            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            upfile = ASUploadFile.objects.all()

            # 주간 월간 제품별 AS 현황
            as_wnum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(weeks=1)).values(
                'product_name').order_by('product_name').annotate(count=Sum('quantity'))
            as_wnum_sum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(weeks=1)).aggregate(
                Sum('quantity'))
            as_mnum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
                'product_name').order_by('product_name').annotate(count=Sum('quantity'))
            as_mnum_sum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).aggregate(
                Sum('quantity'))
            context = {'login_session': login_session, 'company_sheet': company_sheet, 'page_obj': page_obj,
                       'sort': sort, 'as_wnum': as_wnum, 'as_mnum': as_mnum, 'as_wnum_sum': as_wnum_sum,
                       'as_mnum_sum': as_mnum_sum,
                       'over_as': over_as, 'query': query}

        else:
            sort = request.GET.get('sort', '')
            query = request.GET.get('q', '')
            if sort == 'rg_date':
                company_sheet = ASsheet.objects.filter(cname=login_session).order_by('-rg_date')
            elif sort == 'rp_date':
                company_sheet = ASsheet.objects.filter(cname=login_session).order_by('-rp_date')
            elif sort == 'product_name':
                company_sheet = ASsheet.objects.filter(cname=login_session).order_by('-product_name', '-rg_date')
            elif sort == 'finish':
                company_sheet = ASsheet.objects.filter(cname=login_session).order_by('-finish', '-rg_date')
            elif sort == 'all':
                company_sheet = ASsheet.objects.filter(cname=login_session).order_by('-rg_date', 'finish')
            else:
                print("리스트 조회 겸 목록 조회")
                search_sort = request.GET.get('search_sort', '')
                if search_sort == 'product_name':
                    company_sheet = ASsheet.objects.all().filter(Q(product_name__icontains=query), cname=login_session).order_by('-rg_date',
                                                                                                            'finish')
                elif search_sort == 'finish':
                    company_sheet = ASsheet.objects.all().filter(Q(finish__icontains=query), cname=login_session).order_by('-rg_date',
                                                                                                      'finish')
                elif search_sort == 'memo':
                    company_sheet = ASsheet.objects.all().filter(Q(memo__icontains=query), cname=login_session).order_by('-rg_date',
                                                                                                    'finish')
                elif search_sort == 'all':
                    company_sheet = ASsheet.objects.all().filter(
                        Q(product_name__icontains=query) | Q(memo__icontains=query) | Q(cname__icontains=query) | Q(
                            finish__icontains=query) | Q(option__icontains=query), cname=login_session).order_by('-rg_date', 'finish')
                else:
                    company_sheet = ASsheet.objects.filter(cname=login_session).order_by('-rg_date', 'finish')

            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("GET 페이징 끝")
            context = {'login_session': login_session, 'company_sheet': company_sheet, 'page_obj': page_obj,
                       'sort': sort, 'search_sort': search_sort, 'query': query}
        print('끝')
        return render(request, 'assheet/as_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        print("리스트 끝")
        return redirect('asregister:as_list')


# AS 파일 업로드/다운로드
def AsUploadFile(request, pk):
    login_session = request.session.get('login_session')

    if request.method == "POST":
        if request.FILES.get('uploadedFile') is not None:
            if get_object_or_404(ASsheet, no=pk):
                # 템플릿에서 데이터 가져오기
                login_session = request.session.get('login_session')
                cname = login_session
                fileTitle = request.POST["fileTitle"]
                uploadedFile = request.FILES.get('uploadedFile')
                sheet_no = ASsheet.objects.get(no=pk)
                menu = request.POST["menu"]

                # DB에 저장
                uploadfile = models.ASUploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    sheet_no=sheet_no,
                    menu=menu
                )
                uploadfile.save()
    else:
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(ASsheet, no=pk)
        uploadfile = models.ASUploadFile.objects.all()
        no = pk

        context = {'login_session': login_session, 'no': no, 'detailView': detailView, 'files': uploadfile}
        return render(request, "assheet/asfile_upload.html", context)

    uploadfile = models.ASUploadFile.objects.all()
    detailView = get_object_or_404(ASsheet, no=pk)

    return render(request, "assheet/asfile_upload.html", context={
        "files": uploadfile, "login_session": login_session, 'detailView': detailView})


# AS 엑셀 다운로드
def AS_excel(request):
    login_session = request.session.get('login_session')

    print("다운로드 시작")
    # 데이터 db에서 불러옴
    data = ASsheet.objects.all()
    response = HttpResponse(content_type="application/vnd.ms-excel")
    # 다운로드 받을 때 생성될 파일명 설정
    response["Content-Disposition"] = 'attachment; filename=' \
                                      + str(datetime.date.today()) + '_AS.xls'
    print("다운 중간")
    # 인코딩 설정
    wb = xlwt.Workbook(encoding='utf-8')
    # 생성될 시트명 설정
    ws = wb.add_sheet('견적 내역')

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
    col_names = ['NO', '업체명', '고객 접수 일자', '회신 완료 일자', '제품명', '비고', '의견', '완료 여부']

    query = request.GET.get('query')
    if query:
        if login_session == 'insung':
            # 엑셀에 쓸 데이터 리스트화
            rows = ASsheet.objects.all().filter(
                Q(product_name__icontains=query) | Q(memo__icontains=query) | Q(cname__icontains=query) | Q(
                    finish__icontains=query) | Q(option__icontains=query)).values_list('no', 'cname', 'rg_date',
                                                                                       'rp_date', 'product_name',
                                                                                       'memo', 'option', 'finish')
        else:
            rows = ASsheet.objects.filter(
                Q(product_name__icontains=query) | Q(memo__icontains=query) | Q(cname__icontains=query) | Q(
                    finish__icontains=query) | Q(option__icontains=query), cname=login_session).values_list('no',
                                                                                                            'cname',
                                                                                                            'rg_date',
                                                                                                            'rp_date',
                                                                                                            'product_name',
                                                                                                            'memo',
                                                                                                            'option',
                                                                                                            'finish')
    else:
        if login_session == 'insung':
            # 엑셀에 쓸 데이터 리스트화
            rows = ASsheet.objects.all().values_list('no', 'cname', 'rg_date', 'rp_date', 'product_name', 'memo',
                                                     'option', 'finish')
        else:
            rows = ASsheet.objects.filter(cname=login_session).values_list('no', 'cname', 'rg_date', 'rp_date',
                                                                           'product_name', 'memo', 'option', 'finish')

    # 첫번째 열: 설정한 컬럼명 순서대로 스타일 적용하여 생성
    print("다운 중간2")
    row_num = 0
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name, title_style)

    # 두번째 이후 열: 설정한 컬럼명에 맞춘 데이터 순서대로 스타일 적용하여 생성
    for row in rows:
        row_num += 1
        for col_num, attr in enumerate(row):
            if isinstance(attr, datetime.datetime):
                cell_style = styles['date']
            else:
                cell_style = styles['default']
            ws.write(row_num, col_num, attr, cell_style)

    wb.save(response)
    print("다운로드 끝")
    return response


# as 파일 삭제
def ASfile_delete(request, pk):
    login_session = request.session.get('login_session')
    if request.method == 'GET':
        print("get 으로 옴")
        as_file = get_object_or_404(ASUploadFile, no=pk)
        page_no = as_file.sheet_no_id
        if as_file.cname == login_session or login_session == 'insung':
            as_file.delete()
            print('삭제완료')
            return redirect(f'/asregister/AsUploadFile/{page_no}')
        else:
            print("삭제 됨?")
            return redirect('/asregister/as_list/')
    else:
        print('post로 옴')


# AS 접수서 상세 뷰
def as_detail(request, pk):
    if request.method == 'GET':
        login_session = request.session.get('login_session')
        user_name = request.session.get('user_name')
        detailView = get_object_or_404(ASsheet, no=pk)

        try:
            upfile = ASUploadFile.objects.filter(sheet_no_id=pk)
            context = {'detailView': detailView, 'login_session': login_session, 'upfile': upfile,
                       'user_name': user_name}
            print("성공")
        except:
            context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name}
            print("실패")

    else:
        print("설마 포스트")
    return render(request, 'assheet/as_detail.html', context)


# AS 접수건 응대 / 업데이트
def as_modify(request, pk):
    login_session = request.session.get('login_session')
    # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다

    detailView = get_object_or_404(ASsheet, no=pk)
    context = {'detailView': detailView, 'login_session': login_session}

    if request.method == 'GET':
        # get으로 오면 다시 수정페이지로 넘김
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(ASsheet, no=pk)

        context = {'detailView': detailView, 'login_session': login_session}
        return render(request, 'assheet/as_modify.html', context)
    elif request.method == 'POST':

        # 수정 내용 저장
        detailView.rp_date = request.POST['rp_date']
        detailView.rg_date = request.POST['rg_date']
        detailView.product_name = request.POST['product_name']
        detailView.quantity = request.POST['quantity']
        detailView.cname = request.POST['cname']
        detailView.memo = request.POST['memo']
        detailView.option = request.POST['option']
        detailView.finish = request.POST['finish']
        detailView.save()

        login_session = request.session.get('login_session')
        detailView = get_object_or_404(ASsheet, no=pk)
        context = {'detailView': detailView, 'login_session': login_session}
        return render(request, 'assheet/as_detail.html', context)


# AS 접수건 삭제
def as_delete(request, pk):
    login_session = request.session.get('login_session')
    detailView = get_object_or_404(ASsheet, no=pk)
    if detailView.cname == login_session or login_session == 'insung':
        detailView.delete()
        print('삭제완료')
        return redirect('asregister:as_list')
    else:
        return redirect(f'/asregister/as_detail/{pk}')
