from django.urls import path
from . import views


app_name = 'question'

urlpatterns = [
    path('', views.index, name='index'),
    path('que_insert', views.que_insert, name='que_insert'),
    path('que_detail', views.que_detail, name='que_detail'),


]