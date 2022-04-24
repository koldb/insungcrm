from django.db import models


# Create your models here.

#견적서 입력 모델
class EstimateSheet(models.Model):
    no = models.AutoField(primary_key=True)
    rg_date = models.DateTimeField(auto_now_add=True)
    rp_date = models.CharField(null=True, blank=True, max_length=50)
    #file_name = models.FileField(max_length=200, verbose_name='파일 이름')
    product_name = models.CharField(max_length=100, verbose_name='제품 이름')
    quantity = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
    per_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
    total_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
    new_old = models.CharField(max_length=25, verbose_name='구분', null=True, default='신규')
    business_number = models.IntegerField(null=True, blank=True)
    cname = models.CharField(max_length=100, verbose_name='업체명', null=True, blank=True)
    memo = models.TextField(verbose_name='비고', null=True, blank=True)
    option = models.TextField(verbose_name='의견', null=True, blank=True)
    finish = models.CharField(max_length=10, null=True, blank=True)
    fileck = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.no

    class Meta:
        managed = True
        db_table = 'estimatesheet'
        verbose_name = '견적'
        verbose_name_plural = '견적'



class UploadFile(models.Model):
    no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200, null=True)
    uploadedFile = models.FileField(upload_to = "Uploaded Files/", blank=True)
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    sheet_no = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'uploadfile'
        verbose_name = '업로드'
        verbose_name_plural = '업로드'



