from django.shortcuts import render, redirect, get_object_or_404, reverse
from .decorators import login_required, login_ok
import sys
sys.path.append('..')
from accounts.models import User
from .models import EstimateSheet, UploadFile, Ordersheet
from . import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.



# 임시 메인페이지
def index(request):
    login_session = request.session.get('login_session')
    return render(request, 'isscm/index.html', {'login_session': login_session})

# 견적 입력
@login_required
def sheet_insert(request):
    print('견적서 입력 도달')
    login_session = request.session.get('login_session')
    # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다

    if request.method == 'GET':
        print('겟 도달')
        # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
        context = {'login_session': login_session}
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

        insert.save()

        login_session = request.session.get('login_session')
        context = {'login_session': login_session}
        print('입력 끝나 나감')
        return render(request, 'isscm/sheet_insert.html', context)

# 견적 접수건 리스트
@login_required
def sheet_list(request):
    print("견적 리스트 시작")
    login_session = request.session.get('login_session')

    if request.method == 'GET':
        if login_session == 'insung':
            sort = request.GET.get('sort', '')
            if sort == 'rg_date':
                company_sheet = EstimateSheet.objects.all().order_by('rg_date')
            elif sort == 'rp_date':
                company_sheet = EstimateSheet.objects.all().order_by('rp_date')
            elif sort == 'estitle':
                company_sheet = EstimateSheet.objects.all().order_by('estitle')
            elif sort == 'new_old':
                company_sheet = EstimateSheet.objects.all().order_by('new_old')
            elif sort == 'cname':
                company_sheet = EstimateSheet.objects.all().order_by('cname')
            elif sort == 'finish':
                company_sheet = EstimateSheet.objects.all().order_by('finish')
            elif sort == 'user_dept':
                company_sheet = EstimateSheet.objects.all().order_by('-user_dept')
            else:
                company_sheet = EstimateSheet.objects.all().order_by('user_dept', 'rg_date', 'rp_date')

            #페이징
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 7)
            page_obj = paginator.get_page(page)
            print("insung GET 페이징 끝")

            #차트 데이터
            sheet_chart = []
            sheet_chart_data = EstimateSheet.objects.all()
            dept_1 = sheet_chart_data.filter(user_dept="영업1팀", finish="종료").count()
            print(dept_1)
            dept_2 = sheet_chart_data.filter(user_dept="영업2팀", finish="종료").count()
            print(dept_2)
            sheet_chart = [dept_1, dept_2]
            context = {'login_session': login_session, 'page_obj': page_obj, 'sheet_chart': sheet_chart, 'sort': sort}

        else:
            sort = request.GET.get('sort', '')
            if sort == 'rg_date':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date')
            elif sort == 'rp_date':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rp_date')
            elif sort == 'estitle':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('estitle')
            elif sort == 'new_old':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('new_old')
            elif sort == 'cname':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('cname')
            elif sort == 'finish':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('finish')
            elif sort == 'all':
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date', 'finish')
            else:
                company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('user_dept', 'rg_date', 'rp_date')
            #company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date')
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
        print('get?')
        searchlist = EstimateSheet.objects.all().filter(Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(finish__icontains=query))
        print("여기 왓나")
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
        page_obj = paginator.get_page(page)
        print("지나갓나")
        return render(request, 'isscm/sheet_list.html', {'query': query, 'page_obj': page_obj, 'login_session': login_session})
    else:
        print('post로 왓나')
        query = request.GET.get('query')
        print(query)
        searchlist = EstimateSheet.objects.all().filter(Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(finish__icontains=query))
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
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
                # uploadedFile = request.FILES["uploadedFile"]
                sheet_no = pk

                # DB에 저장
                uploadfile = models.UploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    sheet_no=sheet_no
                )
                uploadfile.save()
    else:
        print("get 으로 왓나")
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(EstimateSheet, no=pk)
        uploadfile = models.UploadFile.objects.all()
        no = pk

        context = {'login_session': login_session, 'no': no, 'detailView': detailView, 'files': uploadfile}
        print("겟 다 나갓나")
        return render(request, "isscm/file_upload.html", context)

    uploadfile = models.UploadFile.objects.all()
    detailView = get_object_or_404(EstimateSheet, no=pk)

    return render(request, "isscm/file_upload.html", context={
        "files": uploadfile, "login_session": login_session, 'detailView': detailView})

# 견적서 상세 뷰
def sheet_detail(request, pk):
    if request.method == 'GET':
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(EstimateSheet, no=pk)
        # detailView = EstimateSheet.objects.filter(no=pk)
        context = {'detailView': detailView, 'login_session': login_session}
    else:
        print("설마 포스트")
    return render(request, 'isscm/sheet_detail.html', context)


# 견적 접수건 응대 / 업데이트
def sheet_modify(request, pk):
    login_session = request.session.get('login_session')
    user_dept = request.session.get('user_dept')
    detailView = get_object_or_404(EstimateSheet, no=pk)

    if request.method == 'GET':
        # get으로 오면 다시 수정페이지로 넘김
        detailView = get_object_or_404(EstimateSheet, no=pk)
        context = {'detailView': detailView, 'login_session': login_session, 'user_dept': user_dept}
        print("겟으로 들어왓다 나감")
        return render(request, 'isscm/sheet_modify.html', context)
    elif request.method == 'POST':
        print('POST 들어옴')
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
        detailView.user_dept = request.POST.get('user_dept')

        if detailView.finish == '종료':
            try:
                orfilter = get_object_or_404(Ordersheet, essheet_pk=pk)
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
                orfilter.user_dept = request.POST.get('user_dept')
                orfilter.essheet_pk = pk
                orfilter.save()
                print("발주건 업데이트 저장")
            except:
                orderinsert = Ordersheet()
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
                orderinsert.user_dept = request.POST.get('user_dept')
                orderinsert.essheet_pk = pk
                orderinsert.save()
                print("견적과 발주 저장")

        print("바로 저장으로")
        detailView.save()

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
    print(user_dept)
    if request.method == 'GET':
        print('겟 도달')
        context = {'login_session': login_session, 'user_dept': user_dept}
        print('겟 끝나 나감')
        return render(request, 'isscm/order_insert.html', context)
    elif request.method == 'POST':
        print("입력 시작")
        insert = Ordersheet()
        insert.rp_date = request.POST['rp_date']
        insert.odtitle = request.POST['odtitle']
        insert.product_name = request.POST['product_name']
        insert.quantity = request.POST['quantity']
        insert.per_price = request.POST['per_price']
        insert.total_price = request.POST['total_price']
        insert.new_old = request.POST['new_old']
        insert.cname = request.POST['cname']
        insert.option = request.POST['option']
        insert.user_dept = request.POST['user_dept']

        insert.save()

        login_session = request.session.get('login_session')
        context = {'login_session': login_session}
        print('입력 끝나 나감')
        return render(request, 'isscm/order_insert.html', context)

# 발주건 리스트
@login_ok
def order_list(request):
    print("발주 리스트 시작")
    login_session = request.session.get('login_session')

    if request.method == 'GET':
        sort = request.GET.get('sort', '')
        if sort == 'rp_date':
            ordersheet = Ordersheet.objects.all().order_by('rp_date')
        elif sort == 'odtitle':
            ordersheet = Ordersheet.objects.all().order_by('odtitle')
        elif sort == 'product_name':
            ordersheet = Ordersheet.objects.all().order_by('product_name')
        elif sort == 'new_old':
            ordersheet = Ordersheet.objects.all().order_by('new_old')
        elif sort == 'cname':
            ordersheet = Ordersheet.objects.all().order_by('cname')
        elif sort == 'user_dept':
            ordersheet = Ordersheet.objects.all().order_by('user_dept')
        else:
            ordersheet = Ordersheet.objects.all().order_by('user_dept', 'rp_date')

        #페이징
        page = request.GET.get('page', '1')
        paginator = Paginator(ordersheet, 7)
        page_obj = paginator.get_page(page)
        print("insung GET 페이징 끝")
        context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort}
        # 일반 업체는 못 들어오도록
        # else:
        #     sort = request.GET.get('sort', '')
        #     if sort == 'rg_date':
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date')
        #     elif sort == 'rp_date':
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rp_date')
        #     elif sort == 'estitle':
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('estitle')
        #     elif sort == 'new_old':
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('new_old')
        #     elif sort == 'cname':
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('cname')
        #     elif sort == 'finish':
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('finish')
        #     elif sort == 'all':
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date', 'finish')
        #     else:
        #         company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('user_dept', 'rg_date', 'rp_date')
        #     #company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date')
        #     page = request.GET.get('page', '1')
        #     paginator = Paginator(company_sheet, 7)
        #     page_obj = paginator.get_page(page)
        #     print("일반 GET 페이징 끝")
        #     context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort}

        print('끝')
        return render(request, 'isscm/order_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        if login_session == 'insung':
            ordersheet = Ordersheet.objects.all().order_by('user_dept', 'rp_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(ordersheet, 7)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        # else:
        #     company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date', 'rp_date')
        #     page = request.GET.get('page', '1')
        #     paginator = Paginator(company_sheet, 7)
        #     page_obj = paginator.get_page(page)
        #     print("페이징 끝")
        context = {'login_session': login_session, 'page_obj': page_obj}
    print("리스트 끝")
    return render(request, 'isscm/order_list.html', context)


# 발주 리스트 검색
def ordersearchResult(request):
    login_session = request.session.get('login_session')
    searchlist = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('get?')
        searchlist = EstimateSheet.objects.all().filter(Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(finish__icontains=query))
        print("여기 왓나")
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
        page_obj = paginator.get_page(page)
        print("지나갓나")
        return render(request, 'isscm/sheet_list.html', {'query': query, 'page_obj': page_obj, 'login_session': login_session})
    else:
        print('post로 왓나')
        query = request.GET.get('query')
        print(query)
        searchlist = EstimateSheet.objects.all().filter(Q(product_name__icontains=query) | Q(new_old__icontains=query) | Q(cname__icontains=query) | Q(finish__icontains=query))
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
        page_obj = paginator.get_page(page)
        context = {'query': query, 'page_obj': page_obj, 'login_session': login_session}
        print('포스트 나갓나')
    return render(request, 'isscm/sheet_list.html', context)

# 발주건 수정/저장 한번에
def order_modify(request, pk):
    login_session = request.session.get('login_session')
    user_dept = request.session.get('user_dept')
    detailView = get_object_or_404(Ordersheet, no=pk)

    if request.method == 'GET':
        # get으로 오면 다시 수정페이지로 넘김
        detailView = get_object_or_404(Ordersheet, no=pk)
        context = {'detailView': detailView, 'login_session': login_session, 'user_dept': user_dept}
        print("겟으로 들어왓다 나감")
        return render(request, 'isscm/order_modify.html', context)
    elif request.method == 'POST':
        print('POST 들어옴')
        # 수정 내용 저장
        detailView.rp_date = request.POST['rp_date']
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
        print("바로 저장으로")
        detailView.save()

    login_session = request.session.get('login_session')
    context = {'detailView': detailView, 'login_session': login_session}
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

# 견적 파일 업로드/다운로드
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
                sheet_no = pk

                # DB에 저장
                uploadfile = models.OrderUploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    sheet_no=sheet_no
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
