from django.db import models
from django.core.validators import RegexValidator


# Create your models here.

#유저 정보 모델
class User(models.Model):
    no = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True, verbose_name='아이디')
    cname = models.CharField(max_length=100, verbose_name='업체명')
    user_pw = models.CharField(max_length=100, verbose_name='비밀번호')
    phoneNumberRegex = RegexValidator(regex='\d{2,3}-\d{3,4}-\d{4}')
    user_phone = models.CharField(validators=[phoneNumberRegex], max_length=30, unique=True, verbose_name='연락처')
    user_email = models.EmailField(max_length=100, blank=True, null=True, unique=True, verbose_name='이메일')
    user_date = models.DateTimeField(auto_now_add=True)  # 입력시 현재 시간 날짜 삽입
    user_status = models.IntegerField(default=1)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'accounts'
        verbose_name = '유저'
        verbose_name_plural = '유저'





