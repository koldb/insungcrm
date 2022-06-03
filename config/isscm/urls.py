from django.urls import path
from . import views


app_name = 'isscm'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('main_uploadFile/<int:pk>/', views.main_uploadFile, name='main_uploadFile'),
    path('main_file_delete/<int:pk>/', views.main_file_delete, name='main_file_delete'),
    path('searchData/', views.searchData, name='searchData'),
    path('main_excel/', views.main_excel, name='main_excel'),
    path('sub_excel/', views.sub_excel, name='sub_excel'),
    path('sub_list_excel/', views.sub_list_excel, name='sub_list_excel'),
    path('product_info_excel/', views.product_info_excel, name='product_info_excel'),
    path('main_downloadfile/<int:pk>/', views.main_downloadfile, name='main_downloadfile'),
    path('main_insert', views.main_insert, name='main_insert'),
    path('main_detail/<int:pk>/', views.main_detail, name='main_detail'),
    path('main_delete/<int:pk>/', views.main_delete, name='main_delete'),
    path('sub_delete/<int:pk>/<int:mid>/', views.sub_delete, name='sub_delete'),
    path('main_list/', views.main_list, name='main_list'),
    path('sub_insert/<int:pk>/', views.sub_insert, name='sub_insert'),
    path('sub_modify/<int:pk>/<int:mid>/', views.sub_modify, name='sub_modify'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_modify/<int:pk>/', views.product_modify, name='product_modify'),
    path('product_delete/<int:pk>/<int:sid>/', views.product_delete, name='product_delete'),

]

