from django.db import models
from .utils import rename_file_to_uuid

# Create your models here.

class question_sheet(models.Model):
    no = models.AutoField(primary_key=True)
    title = models.CharField(null=True, blank=True, max_length=50, verbose_name='제목')
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    type = models.CharField(max_length=30, verbose_name='유형')
    content = models.TextField(verbose_name='내용', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'questionsheet'
        verbose_name = '문의글'
        verbose_name_plural = '문의글'


class question_comment(models.Model):
    no = models.AutoField(primary_key=True)
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    register = models.CharField(max_length=30, verbose_name='등록자', null=True, blank=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, db_column="parent_comment")
    content = models.TextField(verbose_name='내용', null=True, blank=True)
    que_no = models.ForeignKey(question_sheet, on_delete=models.CASCADE, null=True, db_column="que_no")

    class Meta:
        managed = True
        db_table = 'quecomment'
        verbose_name = '문의댓글'
        verbose_name_plural = '문의댓글'


# 파일 업로드, 다운로드 모델
class que_UploadFile(models.Model):
    no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=70, null=True)
    title = models.CharField(max_length=50, null=True)
    uploadedFile = models.FileField(upload_to = rename_file_to_uuid, blank=True)
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    que_no = models.ForeignKey(question_sheet, on_delete=models.CASCADE, null=True, db_column="que_no")
    menu = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'que_uploadfile'
        verbose_name = '문의글 첨부파일'
        verbose_name_plural = '문의글 첨부파일'