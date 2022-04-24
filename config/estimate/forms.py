from django import forms
from .models import Company


class Companyform(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('cname', 'cmanager', 'smanager', 'phone', 'email', 'adress', 'homepage')
