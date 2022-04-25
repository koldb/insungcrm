from django.shortcuts import render, redirect, get_object_or_404, reverse
from .decorators import login_required
from .models import EstimateSheet, UploadFile
from . import models
from django.core.paginator import Paginator
from .forms import PostSearchForm
from django.views.generic import FormView
from django.db.models import Q

# Create your views here.

# 임시 메인페이지
def index(request):
    return render(request, 'isscm/index.html')


# 견적 입력
@login_required
def sheet_insert(request):
    print('견적서 입력 도달')
    login_session = request.session.get('login_session')
    # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
    context = {'login_session': login_session}

    if request.method == 'GET':
        print('겟 도달')
        login_session = request.session.get('login_session')
        # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다
        context = {'login_session': login_session}
        print('겟 끝나 나감')
        return render(request, 'isscm/sheet_insert.html', context)
    elif request.method == 'POST':
        print("입력 시작")
        insert = EstimateSheet()
        insert.product_name = request.POST['product_name']
        insert.quantity = request.POST['quantity']
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
    print("리스트 시작")
    login_session = request.session.get('login_session')
    
    if request.method == 'GET':
        if login_session == 'insung':
            company_sheet = EstimateSheet.objects.all().order_by('rg_date')

            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")

        else:
            company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")

        context = {'login_session': login_session, 'company_sheet': company_sheet, 'page_obj': page_obj}
        print('끝')
        return render(request, 'isscm/sheet_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        if login_session == 'insung':
            company_sheet = EstimateSheet.objects.all().order_by('rg_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        else:
            company_sheet = EstimateSheet.objects.filter(cname=login_session).order_by('rg_date')
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 5)
            page_obj = paginator.get_page(page)
            print("페이징 끝")
        context = {'company_sheet': company_sheet, 'login_session': login_session, 'page_obj': page_obj}
        print("리스트 끝")
        return render(request, 'isscm/sheet_list.html', context)


# 리스트 검색2
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






# 리스트 검색
# class SearchFormView(FormView):
#     form_class = PostSearchForm
#     template_name = 'isscm/sheet_list.html'
#
#     def form_valid(self, form):
#         searchword = form.cleaned_data['search_word']
#         sheet_list = EstimateSheet.objects.filter(Q(rg_date__icontains=searchword) | Q(rp_date__icontains=searchword) | Q(product_name__icontains=searchword) | Q(new_old__icontains=searchword) | Q(cname__icontains=searchword) | Q(finish__icontains=searchword)).distinct()
#
#         print("검색 여까지?")
#         context = {}
#         context['form'] = form
#         context['search_term'] = searchword
#         context['object_list'] = sheet_list
#         print("검색 끝까지?")
#         return render(self.request, self.template_name, context)


# 파일 업로드/다운로드
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
    # render context로 넘길때 key:value 로 넘겨야 넘어가고 받아진다

    detailView = get_object_or_404(EstimateSheet, no=pk)
    context = {'detailView': detailView, 'login_session': login_session}

    # if detailView.cname != login_session:
    #     #견적건 업체명과 로그인한 업체명이 맞는지 비교
    #     print('업체명 틀려서 나감')
    #     return redirect('/sheet_detail/{pk}/')

    if request.method == 'GET':
        # get으로 오면 다시 수정페이지로 넘김
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(EstimateSheet, no=pk)

        context = {'detailView': detailView, 'login_session': login_session}
        print("겟으로 들어왓다 나감")
        return render(request, 'isscm/sheet_modify.html', context)
    elif request.method == 'POST':
        print('post 들어옴')

        # 수정 내용 저장
        detailView.rp_date = request.POST['rp_date']
        print(detailView.rp_date)
        detailView.product_name = request.POST['product_name']
        detailView.quantity = request.POST['quantity']
        detailView.per_price = request.POST.get('per_price', None)
        detailView.total_price = request.POST.get('total_price', None)
        detailView.new_old = request.POST['new_old']
        detailView.cname = request.POST['cname']
        detailView.memo = request.POST['memo']
        detailView.option = request.POST['option']
        detailView.finish = request.POST['finish']
        print("저장 코앞")
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
    context = {'login_session': login_session}
    if detailView.cname == login_session:
        detailView.delete()
        print('삭제완료')
        return redirect('isscm:sheet_list')
    else:
        return redirect(f'/isscm/sheet_detail/{pk}')


# # 리스트 페이징
# def page(request):
#     page = request.GET.get('page', '1')  # 1 페이지
#     list = EstimateSheet.objects.order_by('-rg_date')
#     paginator = Paginator(list, 5)  # 페이지당 10개씩
#     page_obj = paginator.get_page(page)
#     context = {'list_page': page_obj}
#     return render(request, 'isscm/sheet_list.html', context)
