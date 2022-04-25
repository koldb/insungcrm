from django import forms
from .models import EstimateSheet

from django_summernote.widgets import SummernoteWidget

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')