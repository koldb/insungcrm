from django.db import models
from .utils import rename_file_to_uuid
from config import settings
import os


# Create your models here.

# 견적서 입력 모델
class EstimateSheet(models.Model):
    no = models.AutoField(primary_key=True)
    rg_date = models.DateTimeField(auto_now_add=True)
    rp_date = models.CharField(null=True, blank=True, max_length=50)
    estitle = models.CharField(null=True, blank=True, max_length=50)
    product_name = models.CharField(max_length=100, verbose_name='제품 이름')
    quantity = models.IntegerField(null=True, blank=True, default=0)
    per_price = models.IntegerField(null=True, blank=True, default=0)
    total_price = models.IntegerField(null=True, blank=True, default=0)
    new_old = models.CharField(max_length=25, verbose_name='구분', null=True, default='신규')
    business_number = models.IntegerField(null=True, blank=True)
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    memo = models.TextField(verbose_name='비고', null=True, blank=True)
    option = models.TextField(verbose_name='의견', null=True, blank=True)
    finish = models.CharField(max_length=10, null=True, blank=True)
    user_dept = models.CharField(null=True, blank=True, max_length=20, verbose_name='부서명')
    user_name = models.CharField(max_length=20, verbose_name='성함', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'estimatesheet'
        verbose_name = '견적'
        verbose_name_plural = '견적'


# 발주 모델
class Ordersheet(models.Model):
    no = models.AutoField(primary_key=True)
    rg_date = models.CharField(null=True, blank=True, max_length=20)
    rp_date = models.CharField(null=True, blank=True, max_length=50)
    odtitle = models.CharField(null=True, blank=True, max_length=50, verbose_name='발주명')
    product_name = models.CharField(max_length=100, verbose_name='제품 이름')
    quantity = models.IntegerField(null=True, blank=True, default=0, verbose_name='수량')
    per_price = models.IntegerField(null=True, blank=True, default=0)
    total_price = models.IntegerField(null=True, blank=True, default=0)
    new_old = models.CharField(max_length=25, verbose_name='구분', null=True, default='신규')
    business_number = models.IntegerField(null=True, blank=True)
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    memo = models.TextField(verbose_name='비고', null=True, blank=True)
    option = models.TextField(verbose_name='의견', null=True, blank=True)
    user_dept = models.CharField(null=True, blank=True, max_length=20, verbose_name='부서명')
    user_name = models.CharField(max_length=20, verbose_name='성함', null=True, blank=True)
    essheet_pk = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'ordersheet'
        verbose_name = '발주 입력'
        verbose_name_plural = '발주 입력'


# 발주 파일 업로드, 다운로드 모델
class OrderUploadFile(models.Model):
    no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200, null=True)
    uploadedFile = models.FileField(upload_to=rename_file_to_uuid, blank=True, null=True)
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    sheet_no = models.ForeignKey(Ordersheet, on_delete=models.CASCADE, null=True, db_column="sheet_no")
    menu = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'Orderuploadfile'
        verbose_name = 'Order file 업로드'
        verbose_name_plural = 'Order file 업로드'


# 제품명 db 테스트
class ProductDb(models.Model):
    no = models.IntegerField(auto_created=True, primary_key=True)
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
    rp_date = models.DateField(null=True, blank=True, max_length=50, verbose_name='마감일자')
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
    product_name = models.CharField(max_length=100, verbose_name='제품 이름')
    quantity = models.IntegerField(null=True, blank=True, default=0, verbose_name='수량')
    per_price = models.IntegerField(null=True, blank=True, default=0, verbose_name='단가')
    tax = models.IntegerField(null=True, blank=True, default=0, verbose_name='부가세')
    total_price = models.IntegerField(null=True, blank=True, default=0, verbose_name='총금액')
    production_date = models.DateField(null=True, blank=True, verbose_name='생산일자')
    release_date = models.DateField(null=True, blank=True, verbose_name='출고일자')
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    serial = models.CharField(null=True, blank=True, max_length=20, verbose_name='시리얼')
    warranty = models.DateField(null=True, blank=True, verbose_name='보증만료일')

    class Meta:
        managed = True
        db_table = 'SubSheet'
        verbose_name = '서브'
        verbose_name_plural = '서브'




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
