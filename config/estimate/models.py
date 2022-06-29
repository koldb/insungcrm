from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator


# Create your models here.


#업체 등록 모델
class Company(models.Model):
    no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100)
    cmanager = models.CharField(max_length=100)
    smanager = models.CharField(max_length=100, blank=True, null=True)
    phoneNumberRegex = RegexValidator(regex='\d{2,3}-\d{3,4}-\d{4}')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=11, unique=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    adress = models.CharField(max_length=800, blank=True, null=True)
    homepage = models.CharField(max_length=800, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)  # 입력시 현재 시간 날짜 삽입


class Meta:
    managed = True
    db_table = 'company'



#회사 정보 DB
class CompanyDb(models.Model):
    no = models.AutoField(primary_key=True)
    ccode = models.IntegerField()
    cname = models.CharField(max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)
    owner = models.CharField(max_length=25, db_collation='utf8mb4_general_ci', blank=True, null=True)
    cphone = models.CharField(max_length=25, db_collation='utf8mb4_general_ci', blank=True, null=True)
    cemail = models.CharField(max_length=30, db_collation='utf8mb4_general_ci', blank=True, null=True)
    smanager = models.CharField(max_length=25, db_collation='utf8mb4_general_ci', blank=True, null=True)
    rg_date = models.DateField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'company_db'
        unique_together = (('no', 'ccode'),)