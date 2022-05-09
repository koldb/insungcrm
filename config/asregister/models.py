from django.db import models
from isscm.utils import rename_file_to_uuid

# Create your models here.

#AS 입력 모델
class ASsheet(models.Model):
    no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='고객 접수일')
    rp_date = models.CharField(null=True, blank=True, max_length=50, verbose_name='처리 완료일')
    product_name = models.CharField(max_length=100, verbose_name='제품 이름')
    memo = models.TextField(verbose_name='비고', null=True, blank=True)
    option = models.TextField(verbose_name='의견', null=True, blank=True)
    finish = models.CharField(max_length=10, null=True, blank=True, verbose_name='완료 여부')

    def __str__(self):
        return self.no

    class Meta:
        managed = True
        db_table = 'assheet'
        verbose_name = 'AS접수'
        verbose_name_plural = 'AS접수'



# 파일 업로드, 다운로드 모델
class ASUploadFile(models.Model):
    no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200, null=True)
    uploadedFile = models.FileField(upload_to =rename_file_to_uuid, blank=True)
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    sheet_no = models.ForeignKey(ASsheet, on_delete=models.CASCADE, null=True, db_column="sheet_no")
    menu = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'ASuploadfile'
        verbose_name = 'AS file 업로드'
        verbose_name_plural = 'AS file 업로드'

