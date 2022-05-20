from django.urls import path
from . import views


app_name = 'isscm'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('sheet_insert', views.sheet_insert, name='sheet_insert'),
    path('order_insert', views.order_insert, name='order_insert'),
    path('sheet_list', views.sheet_list, name='sheet_list'),
    path('order_list', views.order_list, name='order_list'),
    path('order_history_list', views.order_history_list, name='order_history_list'),
    path('uploadFile/<int:pk>/', views.uploadFile, name='uploadFile'),
    path('sheetfile_delete/<int:pk>/', views.sheetfile_delete, name='sheetfile_delete'),
    path('order_uploadFile/<int:pk>/', views.order_uploadFile, name='order_uploadFile'),
    path('orderfile_delete/<int:pk>/', views.orderfile_delete, name='orderfile_delete'),
    path('sheet_detail/<int:pk>/', views.sheet_detail, name='sheet_detail'),
    path('order_delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('order_modify/<int:pk>/', views.order_modify, name='order_modify'),
    path('sheet_modify/<int:pk>/', views.sheet_modify, name='sheet_modify'),
    path('sheet_delete/<int:pk>/', views.sheet_delete, name='sheet_delete'),
    path('searchData/', views.searchData, name='searchData'),
    path('es_excel/', views.es_excel, name='es_excel'),
    path('order_excel/', views.order_excel, name='order_excel'),
    path('es_downloadfile/<int:pk>/', views.es_downloadfile, name='es_downloadfile'),
    path('order_downloadfile/<int:pk>/', views.order_downloadfile, name='order_downloadfile'),

]

