from django import forms
from .models import Company


# 업체 정보 입력 폼
class Companyform(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('cname', 'cmanager', 'smanager', 'phone', 'email', 'adress', 'homepage')
