from django.urls import path
from . import views


app_name = 'isscm'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('main_insert', views.main_insert, name='main_insert'),
    path('main_list/', views.main_list, name='main_list'),
    path('main_detail/<int:pk>/', views.main_detail, name='main_detail'),
    path('main_delete/<int:pk>/', views.main_delete, name='main_delete'),
    path('main_uploadFile/<int:pk>/', views.main_uploadFile, name='main_uploadFile'),
    path('main_file_delete/<int:pk>/', views.main_file_delete, name='main_file_delete'),
    path('main_excel_openpyxl/', views.main_excel_openpyxl, name='main_excel_openpyxl'),
    path('main_downloadfile/<int:pk>/', views.main_downloadfile, name='main_downloadfile'),
    path('sub_delete/<int:pk>/<int:mid>/', views.sub_delete, name='sub_delete'),
    path('sub_insert/<int:pk>/', views.sub_insert, name='sub_insert'),
    path('sub_modify/<int:pk>/<int:mid>/', views.sub_modify, name='sub_modify'),
    path('sub_excel/', views.sub_excel, name='sub_excel'),
    path('sub_list_excel_openpyxl/', views.sub_list_excel_openpyxl, name='sub_list_excel_openpyxl'),
    path('searchData/', views.searchData, name='searchData'),
    path('searchPM/', views.searchPM, name='searchPM'),
    path('searchPM_serial/', views.searchPM_serial, name='searchPM_serial'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_modify/<int:pk>/', views.product_modify, name='product_modify'),
    path('product_delete/<int:pk>/<int:sid>/', views.product_delete, name='product_delete'),
    path('product_db_insert/', views.product_db_insert, name='product_db_insert'),
    path('product_db_modify/<int:pk>/', views.product_db_modify, name='product_db_modify'),
    path('product_db_list/', views.product_db_list, name='product_db_list'),
    path('product_db_delete/<int:pk>/', views.product_db_delete, name='product_db_delete'),
    path('product_info_excel/', views.product_info_excel, name='product_info_excel'),
    path('notice_insert/', views.notice_insert, name='notice_insert'),
    path('notice_view/<int:pk>/', views.notice_view, name='notice_view'),
    path('notice_delete/<int:pk>/', views.notice_delete, name='notice_delete'),
    path('pm_insert/', views.pm_insert, name='pm_insert'),
    path('pm_list/', views.pm_list, name='pm_list'),
    path('pm_modify/<int:pk>/', views.pm_modify, name='pm_modify'),
    path('pm_delete/<int:pk>/', views.pm_delete, name='pm_delete'),
    path('pm_excel_openpyxl/', views.pm_excel_openpyxl, name='pm_excel_openpyxl'),
    path('pm_excel_upload/', views.pm_excel_upload, name='pm_excel_upload'),

]

