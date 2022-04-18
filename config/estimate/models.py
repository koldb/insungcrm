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
    # phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phoneNumberRegex = RegexValidator(regex='\d{2,3}-\d{3,4}-\d{4}')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=11, unique=True)
    # email = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    adress = models.CharField(max_length=800, blank=True, null=True)
    homepage = models.CharField(max_length=800, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)  # 입력시 현재 시간 날짜 삽입


class Meta:
    managed = True
    db_table = 'company'


#견적 등록 모델
