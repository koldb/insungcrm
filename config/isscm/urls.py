from django.urls import path
from . import views



app_name = 'isscm'

urlpatterns = [
    path('', views.index, name='index'),
    path('sheet_insert', views.sheet_insert, name='sheet_insert'),
    path('ex_insert', views.ex_insert, name='ex_insert'),
    path('sheet_list', views.sheet_list, name='sheet_list'),
    path('uploadFile/<int:pk>/', views.uploadFile, name='uploadFile'),
    path('sheet_detail/<int:pk>/', views.sheet_detail, name='sheet_detail'),
    path('sheet_modify/<int:pk>/', views.sheet_modify, name='sheet_modify'),
    path('sheet_delete/<int:pk>/', views.sheet_delete, name='sheet_delete'),
    path('searchResult/', views.searchResult, name='searchResult'),
    path('bla', views.bla, name='bla'),

]

