from django.db import models
from .utils import rename_file_to_uuid
from config import settings
import os


# Create your models here.

# 제품명 db
class ProductDb(models.Model):
    no = models.AutoField(auto_created=True, primary_key=True)
    center_code = models.TextField(blank=True, null=True)
    center = models.TextField(blank=True, null=True)
    warehouse_code = models.TextField(blank=True, null=True)
    warehouse_name = models.TextField(blank=True, null=True)
    product_code = models.TextField(blank=True, null=True)
    product_num = models.TextField(blank=True, null=True)
    scan_code = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    account_code = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product_db'


# 메인 DB
class main_sheet(models.Model):
    id = models.AutoField(primary_key=True)
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    rp_date = models.DateField(null=True, blank=True, max_length=50, verbose_name='마감 요청일자')
    end_date = models.DateField(null=True, blank=True, max_length=50, verbose_name='종료일자')
    main_title = models.CharField(null=True, blank=True, max_length=50, verbose_name='견적명')
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    requests = models.TextField(verbose_name='요청사항', null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True, default=0, verbose_name='총금액')
    finish = models.CharField(max_length=10, null=True, blank=True, verbose_name='완료여부')
    user_dept = models.CharField(null=True, blank=True, max_length=20, verbose_name='부서명')
    user_name = models.CharField(max_length=20, verbose_name='담당자', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'MainSheet'
        verbose_name = '메인'
        verbose_name_plural = '메인'


# 서브 DB
class sub_sheet(models.Model):
    id = models.AutoField(primary_key=True)
    m_id = models.ForeignKey(main_sheet, on_delete=models.CASCADE, null=True, db_column="m_id", related_name='m_id')
    m_title = models.CharField(max_length=100, verbose_name='메인 title', null=True, blank=True)
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    product_name = models.CharField(max_length=100, verbose_name='제품 이름')
    quantity = models.IntegerField(null=True, blank=True, default=0, verbose_name='수량')
    enter_quantity = models.IntegerField(null=True, blank=True, default=0, verbose_name='입력 수량')
    per_price = models.IntegerField(null=True, blank=True, default=0, verbose_name='단가')
    tax = models.IntegerField(null=True, blank=True, default=0, verbose_name='부가세')
    total_price = models.IntegerField(null=True, blank=True, default=0, verbose_name='총금액')
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    user_name = models.CharField(max_length=20, verbose_name='담당자', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'SubSheet'
        verbose_name = '서브'
        verbose_name_plural = '서브'


class product_info(models.Model):
    id = models.AutoField(primary_key=True)
    s_id = models.ForeignKey(sub_sheet, on_delete=models.CASCADE, null=True, db_column="s_id", related_name='s_id')
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    product_name = models.CharField(max_length=100, verbose_name='제품 이름')
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    serial = models.CharField(null=True, blank=True, max_length=20, verbose_name='시리얼')
    production_date = models.DateField(null=True, blank=True, verbose_name='생산일자')
    release_date = models.DateField(null=True, blank=True, verbose_name='출고일자')
    warranty = models.DateField(null=True, blank=True, verbose_name='보증만료일')
    user_name = models.CharField(max_length=20, verbose_name='담당자', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'product_info'
        verbose_name = '제품정보'
        verbose_name_plural = '제품정보'


# 파일 업로드, 다운로드 모델
class UploadFile(models.Model):
    no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200, null=True)
    uploadedFile = models.FileField(upload_to=rename_file_to_uuid, blank=True)
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    main_id = models.ForeignKey(main_sheet, on_delete=models.CASCADE, null=True, db_column="main_id")
    menu = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'uploadfile'
        verbose_name = '업로드'
        verbose_name_plural = '업로드'


# 공지사항
class notice(models.Model):
    no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='제목')
    user_dept = models.CharField(null=True, blank=True, max_length=10, verbose_name='부서명')
    user_name = models.CharField(null=True, blank=True, max_length=10, verbose_name='작성자')
    start_date = models.DateField(null=True, blank=True, max_length=50, verbose_name='시작일자')
    end_date = models.DateField(null=True, blank=True, max_length=50, verbose_name='종료일자')
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    content = models.TextField(verbose_name='내용', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'notice'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'


# 제품 DB
class Product_Management(models.Model):
    no = models.AutoField(primary_key=True)
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    update_date = models.DateTimeField(auto_now=True, verbose_name='수정일자', null=True, blank=True)
    product_name = models.CharField(null=True, blank=True, max_length=300, verbose_name='제품명')
    serial = models.CharField(null=True, blank=True, max_length=300, verbose_name='시리얼')
    current_location = models.CharField(null=True, blank=True, max_length=200, verbose_name='현재 위치')
    status = models.CharField(null=True, blank=True, max_length=200, verbose_name='상태')

    class Meta:
        managed = True
        db_table = 'product_management'
        verbose_name = '제품관리'
        verbose_name_plural = '제품관리'