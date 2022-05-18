from django.shortcuts import render, redirect, get_object_or_404, reverse
from .decorators import login_required, login_ok
import sys

sys.path.append('..')
from accounts.models import User
from asregister.models import ASsheet
from question.models import question_sheet
from .models import EstimateSheet, UploadFile, Ordersheet, ProductDb, OrderUploadFile
from . import models
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
import datetime
import xlwt
from django.http import HttpResponse
import mimetypes
import shutil
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# Create your views here.

# 메인페이지
def index(request):
    login_session = request.session.get('login_session')

    # 1일 기준 신규 접수 현황
    es_count = EstimateSheet.objects.filter(rg_date=date.today() - datetime.timedelta(days=1)).count()
    es_pcount = EstimateSheet.objects.filter(rg_date=date.today() - datetime.timedelta(days=1),
                                             cname=login_session).count()
    es_fcount = EstimateSheet.objects.filter(rg_date=date.today() - datetime.timedelta(days=1),
                                             finish="종료").count()
    as_count = ASsheet.objects.filter(rg_date=date.today() - datetime.timedelta(days=1)).count()
    as_pcount = ASsheet.objects.filter(rg_date=date.today() - datetime.timedelta(days=1),
                                       cname=login_session).count()
    as_fcount = ASsheet.objects.filter(rp_date=date.today() - datetime.timedelta(days=1), finish="종료").count()
    or_count = Ordersheet.objects.filter(rp_date=date.today() - datetime.timedelta(days=1)).count()
    or_pcount = Ordersheet.objects.filter(rp_date=date.today() - datetime.timedelta(days=1),
                                          cname=login_session).count()
    que_count = question_sheet.objects.filter(rg_date=date.today() - datetime.timedelta(days=1)).count()
    que_pcount = question_sheet.objects.filter(rg_date=date.today() - datetime.timedelta(days=1),
                                               cname=login_session).count()

    # 주간 실적 현황
    es_week1 = EstimateSheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                            user_dept='영업1팀').aggregate(Sum('total_price'))
    es_week2 = EstimateSheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                            user_dept='영업2팀').aggregate(Sum('total_price'))
    or_week1 = Ordersheet.objects.filter(rp_date__gte=date.today() - datetime.timedelta(weeks=1),
                                         user_dept='영업1팀').aggregate(Sum('total_price'))
    or_week2 = Ordersheet.objects.filter(rp_date__gte=date.today() - datetime.timedelta(weeks=1),
                                         user_dept='영업2팀').aggregate(Sum('total_price'))

    # 월간 실적 현황
    es_month1 = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                             user_dept='영업1팀').aggregate(Sum('total_price'))
    es_month2 = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                             user_dept='영업2팀').aggregate(Sum('total_price'))
    or_month1 = Ordersheet.objects.filter(rp_date__gte=date.today() - relativedelta(months=1),
                                          user_dept='영업1팀').aggregate(Sum('total_price'))
    or_month2 = Ordersheet.objects.filter(rp_date__gte=date.today() - relativedelta(months=1),
                                          user_dept='영업2팀').aggregate(Sum('total_price'))

    # 제품별 월간 견적, 발주, AS 개수
    es_num = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'product_name').order_by('product_name').annotate(count=Sum('quantity'))
    es_num_sum = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).aggregate(Sum('quantity'))
    or_num = Ordersheet.objects.filter(rp_date__gte=date.today() - relativedelta(months=1)).values(
        'product_name').order_by('product_name').annotate(count=Sum('quantity'))
    print(or_num)
    or_num_sum = Ordersheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).aggregate(
        Sum('quantity'))
    as_num = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'product_name').order_by('product_name').annotate(count=Sum('quantity'))
    as_num_sum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).aggregate(
        Sum('quantity'))

    # 업체별 월간 견적, 발주, AS 개수
    es_cnum = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'cname').order_by('cname').annotate(count=Count('cname'))
    es_cnum_sum = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'cname').order_by('cname').annotate(count=Count('cname')).aggregate(Sum('count'))
    or_cnum = Ordersheet.objects.filter(rp_date__gte=date.today() - relativedelta(months=1)).values('cname').order_by(
        'cname').annotate(count=Count('cname'))
    or_cnum_sum = Ordersheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'cname').order_by('cname').annotate(count=Count('cname')).aggregate(Sum('count'))
    print(or_cnum_sum)
    as_cnum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values('cname').order_by(
        'cname').annotate(count=Count('cname'))
    as_cnum_sum = ASsheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
        'cname').order_by('cname').annotate(count=Count('cname')).aggregate(Sum('count'))


    context = {'login_session': login_session, 'es_count': es_count, 'as_count': as_count, 'or_count': or_count,
               'que_count': que_count,
               'es_week1': es_week1, 'es_week2': es_week2, 'or_week1': or_week1, 'or_week2': or_week2,
               'es_month1': es_month1, 'es_month2': es_month2, 'or_month1': or_month1, 'or_month2': or_month2,
               'es_num': es_num, 'or_num': or_num, 'as_num': as_num,
               'es_cnum': es_cnum, 'or_cnum': or_cnum, 'as_cnum': as_cnum, 'es_fcount': es_fcount,
               'as_fcount': as_fcount, 'es_pcount': es_pcount,
               'as_pcount': as_pcount, 'or_pcount': or_pcount, 'que_pcount': que_pcount, 'es_num_sum':es_num_sum, 'or_num_sum': or_num_sum,
               'as_num_sum': as_num_sum, 'es_cnum_sum': es_cnum_sum, 'or_cnum_sum': or_cnum_sum, 'as_cnum_sum': as_cnum_sum}
    return render(request, 'isscm/index.html', context)


# 견적 입력
@login_required
def sheet_insert(request):
    print('견적서 입력 도달')
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다

    if request.method == 'GET':
        print('겟 도달')
        # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
        context = {'login_session': login_session, 'user_name': user_name}
        print('겟 끝나 나감')
        return render(request, 'isscm/sheet_insert.html', context)
    elif request.method == 'POST':
        print("입력 시작")
        insert = EstimateSheet()
        insert.estitle = request.POST['estitle']
        insert.product_name = request.POST['product_name']
        print(insert.product_name)
        # qu_str= request.POST.getlist('quantity')
        # #qu_map= map(int, qu_str)
        # insert.quantity = json.dumps(qu_str)
        # print(insert.quantity)
        insert.quantity = request.POST['quantity']
        print(insert.quantity)
        insert.cname = request.POST['cname']
        insert.memo = request.POST['memo']
        insert.user_name = request.POST['user_name']

        insert.save()

        login_session = request.session.get('login_session')
        context = {'login_session': login_session}
        print('입력 끝나 나감')
        return redirect('isscm:sheet_insert')


# 견적 접수건 리스트
@login_required
def sheet_list(request):
    print("견적 리스트 시작")
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')

    if request.method == 'GET':
        if login_session == 'insung':
            sort = request.GET.get('sort', '')
            if sort == 'rg_date':
                company_sheet = EstimateSheet.objects.all().order_by('-rg_date')
            elif sort == 'rp_date':
                company_sheet = EstimateSheet.objects.all().order_by('-rp_date')
            elif sort == 'estitle':
                company_sheet = EstimateSheet.objects.all().order_by('estitle', '-rg_date')
            elif sort == 'new_old':
                company_sheet = EstimateSheet.objects.all().order_by('new_old', '-rg_date',)
            elif sort == 'cname':
                company_sheet = EstimateSheet.objects.all().order_by('cname', '-rg_date')
            elif sort == 'finish':
                company_sheet = EstimateSheet.objects.all().order_by('-finish', '-rg_date')
            elif sort == 'user_dept':
                company_sheet = EstimateSheet.objects.all().order_by('-user_dept', '-rg_date')
            else:
                print("리스트 조회")
                company_sheet = EstimateSheet.objects.all().order_by('-rg_date', 'finish', '-user_dept')

            # 페이징
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("insung GET 페이징 끝")

            # 차트 데이터
            sheet_chart = []
            sheet_chart_data = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1))
            dept_1 = sheet_chart_data.filter(user_dept="영업1팀").count()
            dept_2 = sheet_chart_data.filter(user_dept="영업2팀").count()
            sheet_chart = [dept_1, dept_2]

            # 주간 팀별 실적 현황
            es_week1 = EstimateSheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                                    user_dept='영업1팀').aggregate(Sum('total_price'))
            es_week2 = EstimateSheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                                    user_dept='영업2팀').aggregate(Sum('total_price'))
            es_week3 = EstimateSheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1)).aggregate(Sum('total_price'))
            # 월간 팀별 실적 조회
            es_month1 = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                                     user_dept='영업1팀').aggregate(Sum('total_price'))
            es_month2 = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                                     user_dept='영업2팀').aggregate(Sum('total_price'))
            es_month3 = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).aggregate(Sum('total_price'))

            # 주간 담당자별 실적 현황
            es_cweek1_total = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(weeks=1)).exclude(user_dept=None).values(
                'user_name').order_by('user_name').distinct().annotate(sum=Sum('total_price'))
            print(EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(weeks=1)).distinct().values(
                'user_name').aggregate(Sum('total_price')))
            # 월간 담당자별 실적 현황
            es_cmonth1_total = EstimateSheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).exclude(user_dept=None).values(
                'user_name').order_by('user_name').distinct().annotate(sum=Sum('total_price'))

            context = {'login_session': login_session, 'page_obj': page_obj, 'sheet_chart': sheet_chart, 'sort': sort,
                       'es_month1': es_month1, 'es_month2': es_month2, 'es_week1': es_week1, 'es_week2': es_week2,
                       'es_cweek1_total': es_cweek1_total, 'es_cmonth1_total': es_cmonth1_total, 'es_week3': es_week3, 'es_month3': es_month3}

        else:
            sort = request.GET.get('sort', '')
            if sort == 'rg_date':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('-rg_date')
            elif sort == 'rp_date':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('-rp_date')
            elif sort == 'estitle':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('estitle', '-rg_date')
            elif sort == 'new_old':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('new_old', '-rg_date')
            elif sort == 'cname':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('cname', '-rg_date')
            elif sort == 'finish':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('finish', '-rg_date')
            elif sort == 'all':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('-rg_date', 'finish')
            else:
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('-rg_date', 'finish')

            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("일반 GET 페이징 끝")
            context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort}

        print('끝')
        return render(request, 'isscm/sheet_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        if login_session == 'insung':
            company_sheet = EstimateSheet.objects.all().order_by('user_dept', 'rg_date', 'rp_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        else:
            company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        context = {'company_sheet': company_sheet, 'login_session': login_session, 'page_obj': page_obj}
        print("리스트 끝")
        return render(request, 'isscm/sheet_list.html', context)


# 견적 리스트 검색
def searchResult(request):
    login_session = request.session.get('login_session')
    searchlist = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('get? : ' + query[0])
        searchlist = EstimateSheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                finish__icontains=query) | Q(estitle__icontains=query))
        print("여기 왓나")
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 7)
        page_obj = paginator.get_page(page)
        print("지나갓나")
        return render(request, 'isscm/sheet_list.html',
                      {'query': query, 'page_obj': page_obj, 'login_session': login_session})
    else:
        print('post로 왓나')
        query = request.GET.get('query')
        print(query)
        searchlist = EstimateSheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                finish__icontains=query) | Q(estitle__icontains=query))
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 7)
        page_obj = paginator.get_page(page)
        context = {'query': query, 'page_obj': page_obj, 'login_session': login_session}
        print('포스트 나갓나')
    return render(request, 'isscm/sheet_list.html', context)


# 견적 파일 업로드/다운로드
def uploadFile(request, pk):
    print("오나요")
    login_session = request.session.get('login_session')
    print("여기 오나요")

    if request.method == "POST":
        if request.FILES.get('uploadedFile') is not None:
            if get_object_or_404(EstimateSheet, no=pk):
                print("pk 왓나요")
                # 템플릿에서 데이터 가져오기
                login_session = request.session.get('login_session')
                cname = login_session
                fileTitle = request.POST["fileTitle"]
                uploadedFile = request.FILES.get('uploadedFile')
                sheet_no = EstimateSheet.objects.get(no=pk)
                menu = request.POST["menu"]

                # DB에 저장
                uploadfile = models.UploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    sheet_no=sheet_no,
                    menu=menu
                )
                uploadfile.save()
    else:
        print("get 으로 왓나")
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(EstimateSheet, no=pk)
        uploadfile = models.UploadFile.objects.all()
        print(uploadfile.values())
        no = pk
        context = {'login_session': login_session, 'no': no, 'detailView': detailView, 'files': uploadfile}
        print("겟 다 나갓나")
        return render(request, "isscm/file_upload.html", context)

    uploadfile = models.UploadFile.objects.all()
    detailView = get_object_or_404(EstimateSheet, no=pk)

    return render(request, "isscm/file_upload.html", context={
        "files": uploadfile, "login_session": login_session, 'detailView': detailView})


# 파일 다운로드
def es_downloadfile(request, pk):
    upload_file = get_object_or_404(UploadFile, no=pk)
    file = upload_file.uploadedFile
    name = file.name
    response = HttpResponse(content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={name}'
    shutil.copyfileobj(file, response)
    return response


# 견적 엑셀 다운로드
def es_excel(request):
    login_session = request.session.get('login_session')

    print("다운로드 시작")
    # 데이터 db에서 불러옴
    # data = EstimateSheet.objects.all()
    response = HttpResponse(content_type="application/vnd.ms-excel")
    # 다운로드 받을 때 생성될 파일명 설정
    response["Content-Disposition"] = 'attachment; filename=' \
                                      + str(datetime.date.today()) + '_estimate.xls'
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
    col_names = ['NO', '고객 접수 일자', '회신 완료 일자', '견적명', '제품명', '수량', '개당 단가', '총 금액', '구분', '사업자코드', '업체명', '비고', '의견',
                 '종료 여부', '담당 팀', '담당자']
    col_names_c = ['NO', '고객 접수 일자', '회신 완료 일자', '견적명', '제품명', '수량', '개당 단가', '총 금액', '구분', '사업자코드', '업체명', '비고', '의견',
                   '종료 여부', '담당 팀']

    query = request.GET.get('query')
    if query:
        print('pk 성공')
        if login_session == 'insung':
            rows = EstimateSheet.objects.all().filter(
                Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                    finish__icontains=query) | Q(estitle__icontains=query)).values_list('no', 'rg_date', 'rp_date',
                                                                                        'estitle', 'product_name',
                                                                                        'quantity',
                                                                                        'per_price', 'total_price',
                                                                                        'new_old', 'business_number',
                                                                                        'cname', 'memo', 'option',
                                                                                        'finish', 'user_dept',
                                                                                        'user_name')
        else:
            rows = EstimateSheet.objects.filter(
                Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(
                    cname__icontains=query) | Q(
                    finish__icontains=query) | Q(estitle__icontains=query), cname=login_session).values_list('no',
                                                                                                             'rg_date',
                                                                                                             'rp_date',
                                                                                                             'estitle',
                                                                                                             'product_name',
                                                                                                             'quantity',
                                                                                                             'per_price',
                                                                                                             'total_price',
                                                                                                             'new_old',
                                                                                                             'business_number',
                                                                                                             'cname',
                                                                                                             'memo',
                                                                                                             'option',
                                                                                                             'finish',
                                                                                                             'user_dept')
    else:
        if login_session == 'insung':
            rows = EstimateSheet.objects.all().values_list('no', 'rg_date', 'rp_date', 'estitle', 'product_name',
                                                           'quantity',
                                                           'per_price', 'total_price', 'new_old', 'business_number',
                                                           'cname', 'memo', 'option', 'finish', 'user_dept',
                                                           'user_name')
        else:
            rows = EstimateSheet.objects.all().filter(cname=login_session).values_list('no', 'rg_date', 'rp_date',
                                                                                       'estitle', 'product_name',
                                                                                       'quantity',
                                                                                       'per_price', 'total_price',
                                                                                       'new_old', 'business_number',
                                                                                       'cname', 'memo', 'option',
                                                                                       'finish', 'user_dept')

    # 첫번째 열: 설정한 컬럼명 순서대로 스타일 적용하여 생성
    print("다운 중간2")
    row_num = 0
    if login_session == 'insung':
        for idx, col_name in enumerate(col_names):
            ws.write(row_num, idx, col_name, title_style)
    else:
        for idx, col_names_c in enumerate(col_names_c):
            ws.write(row_num, idx, col_names_c, title_style)

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


# 견적 파일 삭제
def sheetfile_delete(request, pk):
    login_session = request.session.get('login_session')
    sheetfile = get_object_or_404(UploadFile, no=pk)
    page_no = sheetfile.sheet_no_id
    if sheetfile.cname == login_session or login_session == 'insung':
        sheetfile.delete()
        print('삭제완료')
        return redirect(f'/isscm/uploadFile/{page_no}')
    else:
        print("삭제 됨?")
        return redirect(f'/isscm/sheet_detail/{pk}')


# 견적서 상세 뷰
def sheet_detail(request, pk):
    if request.method == 'GET':
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(EstimateSheet, no=pk)

        # upfile = get_object_or_404(UploadFile, sheet_no_id=pk)
        try:
            upfile = UploadFile.objects.filter(sheet_no_id=pk)
            context = {'detailView': detailView, 'login_session': login_session, 'upfile': upfile}
            print("성공")
        except:
            context = {'detailView': detailView, 'login_session': login_session}
            print("실패")

        print("견적 상세 뷰 들어감")
    else:
        print("설마 포스트")
    return render(request, 'isscm/sheet_detail.html', context)


# 견적 접수건 응대 / 업데이트
def sheet_modify(request, pk):
    login_session = request.session.get('login_session')
    user_dept = request.session.get('user_dept')
    user_name = request.session.get('user_name')
    detailView = get_object_or_404(EstimateSheet, no=pk)

    if request.method == 'GET':
        # get으로 오면 다시 수정페이지로 넘김
        detailView = get_object_or_404(EstimateSheet, no=pk)
        context = {'detailView': detailView, 'login_session': login_session, 'user_dept': user_dept,
                   'user_name': user_name}
        print("겟으로 들어왓다 나감")
        return render(request, 'isscm/sheet_modify.html', context)
    else :
        print('POST 들어옴')
        if login_session == 'insung':
            # 수정 내용 저장
            detailView.rp_date = request.POST['rp_date']
            detailView.estitle = request.POST['estitle']
            detailView.product_name = request.POST['product_name']
            detailView.quantity = request.POST['quantity'].replace(",", "")
            detailView.per_price = request.POST.get('per_price', None).replace(",", "")
            detailView.total_price = request.POST.get('total_price', None).replace(",", "")
            detailView.new_old = request.POST['new_old']
            detailView.cname = request.POST['cname']
            detailView.memo = request.POST['memo']
            detailView.option = request.POST['option']
            detailView.finish = request.POST['finish']
            detailView.user_name = request.POST['user_name']
            detailView.user_dept = request.POST.get('user_dept')
            if detailView.finish == '종료':
                try:
                    orfilter = get_object_or_404(Ordersheet, essheet_pk=pk)
                    orfilter.rg_date = request.POST['rg_date']
                    orfilter.rp_date = request.POST['rp_date']
                    orfilter.odtitle = request.POST['estitle']
                    orfilter.product_name = request.POST['product_name']
                    orfilter.quantity = request.POST['quantity'].replace(",", "")
                    orfilter.per_price = request.POST.get('per_price', None).replace(",", "")
                    orfilter.total_price = request.POST.get('total_price', None).replace(",", "")
                    orfilter.new_old = request.POST['new_old']
                    orfilter.cname = request.POST['cname']
                    orfilter.memo = request.POST['memo']
                    orfilter.option = request.POST['option']
                    orfilter.user_name = request.POST['user_name']
                    orfilter.user_dept = request.POST.get('user_dept')
                    orfilter.essheet_pk = pk
                    orfilter.save()
                    print("발주건 업데이트 저장")
                except:
                    orderinsert = Ordersheet()
                    orderinsert.rg_date = request.POST['rg_date']
                    orderinsert.rp_date = request.POST['rp_date']
                    orderinsert.odtitle = request.POST['estitle']
                    orderinsert.product_name = request.POST['product_name']
                    orderinsert.quantity = request.POST['quantity'].replace(",", "")
                    orderinsert.per_price = request.POST.get('per_price', None).replace(",", "")
                    orderinsert.total_price = request.POST.get('total_price', None).replace(",", "")
                    orderinsert.new_old = request.POST['new_old']
                    orderinsert.cname = request.POST['cname']
                    orderinsert.memo = request.POST['memo']
                    orderinsert.option = request.POST['option']
                    orderinsert.user_name = request.POST['user_name']
                    orderinsert.user_dept = request.POST.get('user_dept')
                    orderinsert.essheet_pk = pk
                    orderinsert.save()
                    print("견적과 발주 저장")
                    print("바로 저장으로")
                    detailView.save()
            detailView.save()
        else:
            detailView.estitle = request.POST['estitle']
            detailView.product_name = request.POST['product_name']
            detailView.quantity = request.POST['quantity'].replace(",", "")
            detailView.per_price = request.POST.get('per_price', None).replace(",", "")
            detailView.total_price = request.POST.get('total_price', None).replace(",", "")
            detailView.cname = request.POST['cname']
            detailView.memo = request.POST['memo']
            detailView.option = request.POST['option']
            detailView.finish = request.POST['finish']
            detailView.user_name = request.POST['user_name']
            detailView.user_dept = request.POST.get('user_dept')
            print("바로 저장으로")
            detailView.save()

            context = {'detailView': detailView, 'login_session': login_session, 'user_dept': user_dept,
                       'user_name': user_name}
            return render(request, 'isscm/sheet_detail.html', context)

    login_session = request.session.get('login_session')
    detailView = get_object_or_404(EstimateSheet, no=pk)
    context = {'detailView': detailView, 'login_session': login_session}
    print("저장하고 나감")
    return render(request, 'isscm/sheet_detail.html', context)


# 견적 접수건 삭제
def sheet_delete(request, pk):
    login_session = request.session.get('login_session')
    detailView = get_object_or_404(EstimateSheet, no=pk)
    if detailView.cname == login_session or login_session == 'insung':
        detailView.delete()
        print('삭제완료')
        return redirect('isscm:sheet_list')
    else:
        print("삭제 됨?")
        return redirect(f'/isscm/sheet_detail/{pk}')


# 발주 입력
@login_ok
def order_insert(request):
    print('발주 입력 도달')
    login_session = request.session.get('login_session')
    user_dept = request.session.get('user_dept')
    user_name = request.session.get('user_name')
    print(user_dept)
    if request.method == 'GET':
        print('겟 도달')
        context = {'login_session': login_session, 'user_dept': user_dept, 'user_name': user_name}
        print('겟 끝나 나감')
        return render(request, 'isscm/order_insert.html', context)
    elif request.method == 'POST':
        print("입력 시작")
        insert = Ordersheet()
        insert.rp_date = request.POST['rp_date']
        insert.rg_date = request.POST['rg_date']
        insert.odtitle = request.POST['odtitle']
        insert.product_name = request.POST['product_name']
        insert.quantity = request.POST['quantity'].replace(",", "")
        insert.per_price = request.POST.get('per_price', None).replace(",", "")
        insert.total_price = request.POST.get('total_price', None).replace(",", "")
        insert.new_old = request.POST['new_old']
        insert.cname = request.POST['cname']
        insert.option = request.POST['option']
        insert.user_dept = request.POST['user_dept']
        insert.user_name = request.POST['user_name']

        insert.save()

        login_session = request.session.get('login_session')
        user_name = request.session.get('user_name')
        context = {'login_session': login_session, 'user_name': user_name}
        print('입력 끝나 나감')
        return render(request, 'isscm/order_insert.html', context)


# 발주건 리스트
@login_ok
def order_list(request):
    print("발주 리스트 시작")
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')

    if request.method == 'GET':
        sort = request.GET.get('sort', '')
        if sort == 'rp_date':
            ordersheet = Ordersheet.objects.all().order_by('-rp_date')
        elif sort == 'rg_date':
            ordersheet = Ordersheet.objects.all().order_by('-rg_date')
        elif sort == 'odtitle':
            ordersheet = Ordersheet.objects.all().order_by('-odtitle', '-rp_date')
        elif sort == 'product_name':
            ordersheet = Ordersheet.objects.all().order_by('-product_name', '-rp_date')
        elif sort == 'cname':
            ordersheet = Ordersheet.objects.all().order_by('-cname', '-rp_date')
        elif sort == 'user_dept':
            ordersheet = Ordersheet.objects.all().order_by('-user_dept', '-rp_date')
        else:
            ordersheet = Ordersheet.objects.all().order_by('-user_dept', '-rp_date')

        # 페이징
        page = request.GET.get('page', '1')
        paginator = Paginator(ordersheet, 7)
        page_obj = paginator.get_page(page)
        print("insung GET 페이징 끝")

        # 차트 데이터
        sheet_chart = []
        sheet_chart_data = Ordersheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1))
        dept_1 = sheet_chart_data.filter(user_dept="영업1팀").count()
        dept_2 = sheet_chart_data.filter(user_dept="영업2팀").count()
        sheet_chart = [dept_1, dept_2]

        # 주간 팀별 실적 현황
        es_week1 = Ordersheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                             user_dept='영업1팀').aggregate(Sum('total_price'))
        es_week2 = Ordersheet.objects.filter(rg_date__gte=date.today() - datetime.timedelta(weeks=1),
                                             user_dept='영업2팀').aggregate(Sum('total_price'))
        # 월간 팀별 실적 조회
        es_month1 = Ordersheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                              user_dept='영업1팀').aggregate(Sum('total_price'))
        es_month2 = Ordersheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1),
                                              user_dept='영업2팀').aggregate(Sum('total_price'))

        # 주간 담당자별 실적 현황
        es_cweek1_total = Ordersheet.objects.filter(rg_date__gte=date.today() - relativedelta(weeks=1)).values(
            'user_name').order_by('user_name').distinct().annotate(sum=Sum('total_price'))
        # 월간 담당자별 실적 현황
        es_cmonth1_total = Ordersheet.objects.filter(rg_date__gte=date.today() - relativedelta(months=1)).values(
            'user_name').order_by('user_name').distinct().annotate(sum=Sum('total_price'))


        context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort, 'user_name': user_name, 'es_week1': es_week1,
                   'es_week2': es_week2, 'es_month1': es_month1, 'es_month2':es_month2, 'es_cweek1_total': es_cweek1_total,
                   'es_cmonth1_total': es_cmonth1_total, 'sheet_chart': sheet_chart}
        print('끝')
        return render(request, 'isscm/order_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        if login_session == 'insung':
            ordersheet = Ordersheet.objects.all().order_by('-rp_date', '-user_dept')
            page = request.GET.get('page', '1')
            paginator = Paginator(ordersheet, 7)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        context = {'login_session': login_session, 'page_obj': page_obj, 'user_name': user_name}
    print("리스트 끝")
    return render(request, 'isscm/order_list.html', context)


# 발주 리스트 검색
def ordersearchResult(request):
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    searchlist = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('quer? : ' + query)
        searchlist = Ordersheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                odtitle__icontains=query) |
            Q(user_dept__icontains=query))
        print("여기 왓나")
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 7)
        page_obj = paginator.get_page(page)
        print("지나갓나")
        return render(request, 'isscm/order_list.html',
                      {'query': query, 'page_obj': page_obj, 'login_session': login_session, 'user_name': user_name})
    else:
        print('post로 왓나')
        query = request.GET.get('query')
        print(query)
        searchlist = Ordersheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                odtitle__icontains=query) |
            Q(user_dept__icontains=query))
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 7)
        page_obj = paginator.get_page(page)
        context = {'query': query, 'page_obj': page_obj, 'login_session': login_session, 'user_name': user_name}
        print('포스트 나갓나')
    return render(request, 'isscm/order_list.html', context)


# 발주건 수정/저장 한번에
def order_modify(request, pk):
    login_session = request.session.get('login_session')
    user_dept = request.session.get('user_dept')
    user_name = request.session.get('user_name')
    detailView = get_object_or_404(Ordersheet, no=pk)

    if request.method == 'GET':
        # get으로 오면 다시 수정페이지로 넘김
        detailView = get_object_or_404(Ordersheet, no=pk)

        try:
            upfile = OrderUploadFile.objects.filter(sheet_no_id=pk)
            context = {'detailView': detailView, 'login_session': login_session, 'user_dept': user_dept,
                       'upfile': upfile, 'user_name': user_name}
            print("성공")
        except:
            context = {'detailView': detailView, 'login_session': login_session, 'user_dept': user_dept, 'user_name': user_name}
            print("실패")

        print("겟으로 들어왓다 나감")
        return render(request, 'isscm/order_modify.html', context)
    elif request.method == 'POST':
        print('POST 들어옴')
        # 수정 내용 저장
        detailView.rp_date = request.POST['rp_date']
        detailView.rg_date = request.POST['rg_date']
        detailView.odtitle = request.POST['odtitle']
        detailView.product_name = request.POST['product_name']
        detailView.quantity = request.POST['quantity'].replace(",", "")
        detailView.per_price = request.POST.get('per_price', None).replace(",", "")
        detailView.total_price = request.POST.get('total_price', None).replace(",", "")
        detailView.new_old = request.POST['new_old']
        detailView.cname = request.POST['cname']
        detailView.memo = request.POST['memo']
        detailView.option = request.POST['option']
        detailView.user_dept = request.POST.get('user_dept')
        detailView.user_name = request.POST.get('user_name')
        print("바로 저장으로")
        detailView.save()

    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name}
    print("저장하고 나감")
    return render(request, 'isscm/order_modify.html', context)


# 발주건 삭제
def order_delete(request, pk):
    login_session = request.session.get('login_session')
    detailView = get_object_or_404(Ordersheet, no=pk)
    if login_session == 'insung':
        detailView.delete()
        print('삭제완료')
        return redirect('isscm:order_list')
    else:
        print("삭제 됨?")
        return redirect(f'/isscm/order_modify/{pk}')


# 발주 파일 업로드/다운로드
def order_uploadFile(request, pk):
    print("오나요")
    login_session = request.session.get('login_session')
    print("여기 오나요")

    if request.method == "POST":
        if request.FILES.get('uploadedFile') is not None:
            if get_object_or_404(Ordersheet, no=pk):
                print("pk 왓나요")
                # 템플릿에서 데이터 가져오기
                cname = request.POST["cname"]
                fileTitle = request.POST["fileTitle"]
                uploadedFile = request.FILES.get('uploadedFile')
                sheet_no = Ordersheet.objects.get(no=pk)
                menu = request.POST["menu"]

                # DB에 저장
                uploadfile = models.OrderUploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    sheet_no=sheet_no,
                    menu=menu

                )
                uploadfile.save()
    else:
        print("get 으로 왓나")
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(Ordersheet, no=pk)
        uploadfile = models.OrderUploadFile.objects.all()
        no = pk

        context = {'login_session': login_session, 'no': no, 'detailView': detailView, 'files': uploadfile}
        print("겟 다 나갓나")
        return render(request, "isscm/orderfile_upload.html", context)

    uploadfile = models.OrderUploadFile.objects.all()
    detailView = get_object_or_404(Ordersheet, no=pk)

    return render(request, "isscm/orderfile_upload.html", context={
        "files": uploadfile, "login_session": login_session, 'detailView': detailView})


# 발주 파일 다운로드
def order_downloadfile(request, pk):
    upload_file = get_object_or_404(OrderUploadFile, no=pk)
    file = upload_file.uploadedFile
    name = file.name
    response = HttpResponse(content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={name}'
    shutil.copyfileobj(file, response)
    return response


# 발주 엑셀 다운로드
def order_excel(request):
    print("다운로드 시작")
    # 데이터 db에서 불러옴
    data = EstimateSheet.objects.all()
    response = HttpResponse(content_type="application/vnd.ms-excel")
    # 다운로드 받을 때 생성될 파일명 설정
    response["Content-Disposition"] = 'attachment; filename=' \
                                      + str(datetime.date.today()) + '_order.xls'
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
    col_names = ['NO', '완료 일자', '발주명', '제품명', '수량', '개당 단가', '총 금액', '구분', '사업자코드', '업체명', '비고', '의견', '담당 팀', '담당자']



    query = request.GET.get('query')
    print('query인가 : ' + str(query))
    if query:
        print('pk 성공')

        rows = Ordersheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(
                odtitle__icontains=query) | Q(user_dept__icontains=query)).values_list('no', 'rp_date', 'odtitle',
                                                                                       'product_name', 'quantity',
                                                                                       'per_price', 'total_price',
                                                                                       'new_old', 'business_number',
                                                                                       'cname', 'memo', 'option',
                                                                                       'user_dept', 'user_name')
    else:
        print('pk 실패')
        ##엑셀에 쓸 데이터 리스트화
        rows = Ordersheet.objects.all().values_list('no', 'rp_date', 'odtitle', 'product_name', 'quantity',
                                                    'per_price', 'total_price', 'new_old', 'business_number', 'cname',
                                                    'memo', 'option', 'user_dept', 'user_name')

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


# 발주 파일 삭제
def orderfile_delete(request, pk):
    orderfile = get_object_or_404(OrderUploadFile, no=pk)
    page_no = orderfile.sheet_no_id
    if request.method == 'GET':
        orderfile.delete()
        print('삭제완료')
        return redirect(f'/isscm/order_uploadFile/{page_no}')
    else:
        print("삭제 됨?")
        return redirect(f'/isscm/order_modify/{pk}')


# 제품명 검색 자동완성
def searchData(request):
    if 'term' in request.GET:
        qs = ProductDb.objects.filter(product_name__icontains=request.GET.get('term'))
        pname = list()
        for product in qs:
            pname.append(product.product_name)
        return JsonResponse(pname, safe=False)
    return render(request, 'isscm/index.html')
