from django.shortcuts import render, redirect, get_object_or_404, reverse
import sys
sys.path.append('..')

from isscm.decorators import login_required
from . import models
from .models import ASsheet, AsUploadFile
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

# 임시 메인페이지
def index(request):
    return render(request, 'isscm/index.html')


# 견적 입력
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
        insert.memo = request.POST['memo']

        insert.save()

        login_session = request.session.get('login_session')
        context = {'login_session': login_session}
        print('입력 끝나 나감')
        return render(request, 'assheet/as_insert.html', context)


# 견적 접수건 리스트
@login_required
def as_list(request):
    print("리스트 시작")
    login_session = request.session.get('login_session')

    if request.method == 'GET':
        if login_session == 'insung':
            company_sheet = ASsheet.objects.all().order_by('rg_date')

            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")

        else:
            company_sheet = ASsheet.objects.filter(cname=login_session).order_by('rg_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")

        context = {'login_session': login_session, 'company_sheet': company_sheet, 'page_obj': page_obj}
        print('끝')
        return render(request, 'assheet/as_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        if login_session == 'insung':
            company_sheet = ASsheet.objects.all().order_by('rg_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        else:
            company_sheet = ASsheet.objects.filter(cname=login_session).order_by('rg_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        context = {'company_sheet': company_sheet, 'login_session': login_session, 'page_obj': page_obj}
        print("리스트 끝")
        return render(request, 'assheet/as_list.html', context)


# 리스트 검색2
def assearchResult(request):
    login_session = request.session.get('login_session')
    searchlist = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('get?')
        searchlist = ASsheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(memo__icontains=query) | Q(cname__icontains=query) | Q(
                finish__icontains=query) | Q(option__icontains=query))
        print("여기 왓나")
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
        page_obj = paginator.get_page(page)
        print("지나갓나")
        return render(request, 'assheet/as_list.html',
                      {'query': query, 'page_obj': page_obj, 'login_session': login_session})
    else:
        print('post로 왓나')
        query = request.GET.get('query')
        print(query)
        searchlist = ASsheet.objects.all().filter(
            Q(product_name__icontains=query) | Q(memo__icontains=query) | Q(cname__icontains=query) | Q(
                finish__icontains=query) | Q(option__icontains=query))
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 5)
        page_obj = paginator.get_page(page)
        context = {'query': query, 'page_obj': page_obj, 'login_session': login_session}
        print('포스트 나갓나')
    return render(request, 'assheet/as_list.html', context)


# 파일 업로드/다운로드
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
                sheet_no = pk

                # DB에 저장
                uploadfile = models.AsUploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    sheet_no=sheet_no
                )
                uploadfile.save()
    else:
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(ASsheet, no=pk)
        uploadfile = models.AsUploadFile.objects.all()
        no = pk

        context = {'login_session': login_session, 'no': no, 'detailView': detailView, 'files': uploadfile}
        return render(request, "assheet/asfile_upload.html", context)

    uploadfile = models.AsUploadFile.objects.all()
    detailView = get_object_or_404(ASsheet, no=pk)

    return render(request, "assheet/asfile_upload.html", context={
        "files": uploadfile, "login_session": login_session, 'detailView': detailView})


# 견적서 상세 뷰
def as_detail(request, pk):
    if request.method == 'GET':
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(ASsheet, no=pk)
        context = {'detailView': detailView, 'login_session': login_session}
    else:
        print("설마 포스트")
    return render(request, 'assheet/as_detail.html', context)


# 견적 접수건 응대 / 업데이트
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
        detailView.product_name = request.POST['product_name']
        detailView.cname = request.POST['cname']
        detailView.memo = request.POST['memo']
        detailView.option = request.POST['option']
        detailView.finish = request.POST['finish']
        detailView.save()

        login_session = request.session.get('login_session')
        detailView = get_object_or_404(ASsheet, no=pk)
        context = {'detailView': detailView, 'login_session': login_session}
        return render(request, 'assheet/as_detail.html', context)


# 견적 접수건 삭제
def as_delete(request, pk):
    login_session = request.session.get('login_session')
    detailView = get_object_or_404(ASsheet, no=pk)
    context = {'login_session': login_session}
    if detailView.cname == login_session:
        detailView.delete()
        print('삭제완료')
        return redirect('asregister:as_list')
    else:
        return redirect(f'/asregister/as_detail/{pk}')
