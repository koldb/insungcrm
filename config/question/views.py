from django.shortcuts import render, redirect, get_object_or_404
from isscm.decorators import login_required
from .models import question_sheet, question_comment, que_UploadFile
from django.core.paginator import Paginator
from django.db.models import Q
from . import models
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import mimetypes
import shutil
import json
from django.urls import reverse
import datetime

# Create your views here.

# 임시 메인페이지
def index(request):
    login_session = request.session.get('login_session')
    return render(request, 'isscm/index.html', {'login_session': login_session})


# 문의글 입력
@login_required
def que_insert(request):
    print('as 입력 도달')
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        print('겟 도달')
        login_session = request.session.get('login_session')
        context = {'login_session': login_session, 'user_name':user_name}
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
        context = {'login_session': login_session, 'user_name': user_name}
        print('입력 끝나 나감')
        return redirect('question:que_list')


# 문의글 상세 뷰
def que_detail(request, pk):
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    detailView = get_object_or_404(question_sheet, no=pk)
    comments = question_comment.objects.filter(que_no_id=pk).order_by('rg_date')

    sort = request.GET.get('sort', '')
    query = request.GET.get('q', '')
    search_sort = request.GET.get('search_sort', '')
    if request.GET.get('sdate', '') is not None:
        startdate = request.GET.get('sdate', '')
    if request.GET.get('edate', '') is not None:
        enddate = request.GET.get('edate', '')
    page = request.GET.get('page', '')

    if request.method == 'GET':
        try:
            upfile = que_UploadFile.objects.filter(que_no=pk)
            context = {'detailView': detailView, 'login_session': login_session, 'upfile': upfile, 'comments': comments,
                       'user_name': user_name, 'sort': sort, 'query': query, 'search_sort': search_sort, 'sdate': startdate,
                       'edate': enddate, 'page': page}
            print("get 성공")
        except:
            context = {'detailView': detailView, 'login_session': login_session, 'comments': comments, 'user_name': user_name,
                       'sort': sort, 'query': query, 'search_sort': search_sort, 'sdate': startdate, 'edate': enddate, 'page': page
                       }
            print("실패")

        print("문의글 상세 뷰 들어감")
    else:
        print("설마 포스트")
        # upfile = get_object_or_404(UploadFile, sheet_no_id=pk)
        try:
            upfile = que_UploadFile.objects.filter(que_no=pk)
            context = {'detailView': detailView, 'login_session': login_session, 'upfile': upfile, 'user_name': user_name,
                       'comments': comments, 'sort': sort, 'query': query, 'search_sort': search_sort, 'sdate': startdate, 'edate': enddate, 'page': page}
            print("post 성공")
        except:
            context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name, 'comments': comments,
                       'sort': sort, 'query': query, 'search_sort': search_sort, 'sdate': startdate, 'edate': enddate, 'page': page}
            print("실패")
    return render(request, 'question/que_detail.html', context)


# 문의글 리스트
@login_required
def que_list(request):
    print("문의글 리스트 시작")
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        if login_session == 'insung':
            sort = request.GET.get('sort', '')
            query = request.GET.get('q', '')
            if sort == 'rg_date':
                company_sheet = question_sheet.objects.all().order_by('rg_date', '-rg_date')
            elif sort == 'type':
                company_sheet = question_sheet.objects.all().order_by('-type', '-rg_date')
            elif sort == 'cname':
                company_sheet = question_sheet.objects.all().order_by('-cname', '-rg_date')
            elif sort == 'all':
                company_sheet = question_sheet.objects.all().order_by('-rg_date', '-cname')
            else:
                print("리스트 조회 겸 목록 조회")
                search_sort = request.GET.get('search_sort', '')
                startdate = request.GET.get('sdate', '')
                enddate = request.GET.get('edate', '')
                if search_sort == 'cname':
                    company_sheet = question_sheet.objects.all().filter(Q(cname__icontains=query)).order_by('-rg_date', '-cname')
                elif search_sort == 'type':
                    company_sheet = question_sheet.objects.all().filter(Q(type__icontains=query)).order_by('-rg_date', '-cname')
                elif search_sort == 'title':
                    company_sheet = question_sheet.objects.all().filter(Q(title__icontains=query)).order_by('-rg_date', '-cname')
                elif search_sort == 'content':
                    company_sheet = question_sheet.objects.all().filter(Q(content__icontains=query)).order_by('-rg_date', '-cname')
                elif search_sort == 'all':
                    company_sheet = question_sheet.objects.all().filter(
                        Q(title__icontains=query) | Q(type__icontains=query) | Q(cname__icontains=query) | Q(
                            content__icontains=query)).order_by('-rg_date', '-cname')
                elif search_sort == 'rg_date':
                    e_date = datetime.datetime.strptime(enddate, '%Y-%m-%d') + datetime.timedelta(hours=23, minutes=59,
                                                                                                  seconds=59)
                    company_sheet = question_sheet.objects.all().filter(rg_date__gte=startdate, rg_date__lte=e_date).order_by(
                        '-rg_date')
                else:
                    company_sheet = question_sheet.objects.all().order_by('-rg_date', '-cname')

            # 페이징
            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 10)
            page_obj = paginator.get_page(page)
            print("insung GET 페이징 끝")

            context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort, 'query': query, 'search_sort': search_sort,
                       'user_name': user_name, 'sdate': startdate, 'edate': enddate}

        else:
            sort = request.GET.get('sort', '')
            query = request.GET.get('q', '')
            if sort == 'rg_date':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('rg_date', '-rg_date')
            elif sort == 'type':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('-type', '-rg_date')
            elif sort == 'cname':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('-cname', '-rg_date')
            elif sort == 'all':
                company_sheet = question_sheet.objects.filter(cname=login_session).order_by('-rg_date', '-cname')
            else:
                print("리스트 조회 겸 목록 조회")
                search_sort = request.GET.get('search_sort', '')
                startdate = request.GET.get('sdate', '')
                enddate = request.GET.get('edate', '')
                if search_sort == 'type':
                    company_sheet = question_sheet.objects.all().filter(Q(type__icontains=query), cname=login_session).order_by('-rg_date',
                                                                                                           '-cname')
                elif search_sort == 'title':
                    company_sheet = question_sheet.objects.all().filter(Q(title__icontains=query), cname=login_session).order_by('-rg_date',
                                                                                                            '-cname')
                elif search_sort == 'content':
                    company_sheet = question_sheet.objects.all().filter(Q(content__icontains=query), cname=login_session).order_by('-rg_date',
                                                                                                      '-cname')
                elif search_sort == 'all':
                    company_sheet = question_sheet.objects.all().filter(
                        Q(title__icontains=query) | Q(type__icontains=query) | Q(cname__icontains=query) | Q(
                            content__icontains=query), cname=login_session).order_by('-rg_date', '-cname')
                elif search_sort == 'rg_date':
                    e_date = datetime.datetime.strptime(enddate, '%Y-%m-%d') + datetime.timedelta(hours=23, minutes=59,
                                                                                                  seconds=59)
                    company_sheet = question_sheet.objects.all().filter(rg_date__gte=startdate,
                                                                        rg_date__lte=e_date, cname=login_session).order_by(
                        '-rg_date')
                else:
                    company_sheet = question_sheet.objects.filter(cname=login_session).order_by('-rg_date', '-cname')

            page = request.GET.get('page', '1')
            paginator = Paginator(company_sheet, 10)
            page_obj = paginator.get_page(page)
            print("일반 GET 페이징 끝")
            context = {'login_session': login_session, 'page_obj': page_obj, 'sort': sort, 'query': query, 'user_name': user_name}

        print('끝')
        return render(request, 'question/que_list.html', context)
    elif request.method == 'POST':
        print('포스트인가')
        return redirect('question:que_list')


# 문의글 리스트 검색
def searchResult(request):
    login_session = request.session.get('login_session')
    searchlist = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('get?')
        searchlist = question_sheet.objects.all().filter(
            Q(title__icontains=query) | Q(type__icontains=query) | Q(cname__icontains=query) | Q(
                content__icontains=query))
        print("여기 왓나")
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 10)
        page_obj = paginator.get_page(page)
        print("지나갓나")
        return render(request, 'question/que_list.html',
                      {'query': query, 'page_obj': page_obj, 'login_session': login_session})
    else:
        print('post로 왓나')
        query = request.GET.get('query')
        print(query)
        searchlist = question_sheet.objects.all().filter(
            Q(title__icontains=query) | Q(type__icontains=query) | Q(cname__icontains=query) | Q(
                content__icontains=query))
        page = request.GET.get('page', '1')
        paginator = Paginator(searchlist, 10)
        page_obj = paginator.get_page(page)
        context = {'query': query, 'page_obj': page_obj, 'login_session': login_session}
        print('포스트 나갓나')
    return render(request, 'question/que_list.html', context)


# 문의글 수정
def que_modify(request, pk):
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    detailView = get_object_or_404(question_sheet, no=pk)

    if request.method == 'GET':
        # get으로 오면 다시 수정페이지로 넘김
        detailView = get_object_or_404(question_sheet, no=pk)

        context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name}

        print("겟으로 들어왓다 나감")
        return render(request, 'question/que_modify.html', context)
    elif request.method == 'POST':
        print('POST 들어옴')
        # 수정 내용 저장
        detailView.title = request.POST['title']
        detailView.cname = request.POST['cname']
        detailView.type = request.POST['type']
        detailView.content = request.POST['content']
        print("바로 저장으로")
        detailView.save()

    context = {'detailView': detailView, 'login_session': login_session, 'user_name': user_name}
    print("저장하고 나감")
    return render(request, 'question/que_detail.html', context)

# 문의글 삭제
def que_delete(request, pk):
    login_session = request.session.get('login_session')
    detailView = get_object_or_404(question_sheet, no=pk)
    if login_session == 'insung':
        detailView.delete()
        print('삭제완료')
        return redirect('question:que_list')
    else:
        print("삭제 됨?")
        return redirect(f'/question/que_modify/{pk}')


# 문의글 파일 업로드
def que_uploadFile(request, pk):
    print("오나요")
    login_session = request.session.get('login_session')
    user_name = request.session.get('user_name')
    print("여기 오나요")

    if request.method == "POST":
        if request.FILES.get('uploadedFile') is not None:
            if get_object_or_404(question_sheet, no=pk):
                print("pk 왓나요")
                # 템플릿에서 데이터 가져오기
                cname = request.POST["cname"]
                fileTitle = request.POST["fileTitle"]
                uploadedFile = request.FILES.get('uploadedFile')
                que_no = question_sheet.objects.get(no=pk)
                menu = request.POST["menu"]

                # DB에 저장
                uploadfile = models.que_UploadFile(
                    cname=cname,
                    title=fileTitle,
                    uploadedFile=uploadedFile,
                    que_no=que_no,
                    menu=menu
                )
                uploadfile.save()
    else:
        print("get 으로 왓나")
        login_session = request.session.get('login_session')
        detailView = get_object_or_404(question_sheet, no=pk)
        uploadfile = models.que_UploadFile.objects.all()
        no = pk

        context = {'login_session': login_session, 'no': no, 'detailView': detailView, 'files': uploadfile, 'user_name': user_name}
        print("겟 다 나갓나")
        return render(request, "question/que_file_upload.html", context)

    uploadfile = models.que_UploadFile.objects.all()
    detailView = get_object_or_404(question_sheet, no=pk)

    return render(request, "question/que_file_upload.html", context={'user_name': user_name,
        "files": uploadfile, "login_session": login_session, 'detailView': detailView})


# 문의글 파일 다운로드
def que_downloadfile(request, pk):
    upload_file = get_object_or_404(que_UploadFile, no=pk)
    file = upload_file.uploadedFile
    name = file.name
    response = HttpResponse(content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={name}'
    shutil.copyfileobj(file, response)
    return response


# 문의글 파일 삭제
def que_file_delete(request, pk):
    orderfile = get_object_or_404(que_UploadFile, no=pk)
    page_no = orderfile.que_no_id
    if request.method == 'GET':
        orderfile.delete()
        print('삭제완료')
        return redirect(f'/question/que_uploadFile/{page_no}')
    else:
        print("삭제 안함")
        return redirect(f'/question/que_modify/{pk}')

# 문의글 댓글/대댓글
def comment_create(request, pk):
    comment_count = question_comment.objects.filter(que_no_id=pk).count()+1
    quecom = get_object_or_404(question_sheet, no=pk)
    print("댓글 시작")
    if request.method == 'POST':
        print("댓글 저장")
        comment = question_comment()
        comment.register = request.POST.get('register')
        comment.content = request.POST.get('content')
        comment.que_no_id = pk
        comment.parent_comment = request.POST.get('no', None)
        comment.save()
        
        print('댓글수 저장')
        quecom.comm = comment_count
        quecom.save()
        #return render(request, 'question/que_detail.html', {'detailView': que_sheet, 'comments': comments, 'login_session': login_session})
        return HttpResponseRedirect(reverse('question:que_detail', args=[pk]))
    else:
        print('GET 들어옴 / 댓글 조회')



# 문의글 댓글 삭제
def com_delete(request, no, qno):
    print("댓글 삭제 시작")
    login_session = request.session.get('login_session')
    que_sheet = get_object_or_404(question_sheet, no=no)
    comments = question_comment.objects.filter(no=qno)
    comments.delete()

    comment_count = question_comment.objects.filter(que_no_id=no).count()
    quecom = get_object_or_404(question_sheet, no=no)
    quecom.comm = comment_count
    print(quecom.comm)
    quecom.save()

    print('댓글 삭제 완료')
    return redirect('question:que_detail', no)


# 댓글 수정
def comment_modify(request):
    print('댓글 수정 시작')
    jsonObject = json.loads(request.body)
    comment = question_comment.objects.filter(no=jsonObject.get('no'))
    context = {
        'result': 'no'
    }
    if comment is not None:
        print('업데이트 시작')
        comment.update(content=jsonObject.get('content'))
        context = {
            'result': 'ok'
        }
        print('댓글 수정 성공')
        return JsonResponse(context);
    return JsonResponse(context)