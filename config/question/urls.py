from django.urls import path
from . import views


app_name = 'question'

urlpatterns = [
    path('', views.index, name='index'),
    path('que_insert', views.que_insert, name='que_insert'),
    path('comment_create/<int:pk>/', views.comment_create, name='comment_create'),
    path('comment_modify/', views.comment_modify, name='comment_modify'),
    path('que_detail/<int:pk>/', views.que_detail, name='que_detail'),
    path('que_list', views.que_list, name='que_list'),
    path('que_modify/<int:pk>/', views.que_modify, name='que_modify'),
    path('que_delete/<int:pk>/', views.que_delete, name='que_delete'),
    path('que_uploadFile/<int:pk>/', views.que_uploadFile, name='que_uploadFile'),
    path('que_downloadfile/<int:pk>/', views.que_downloadfile, name='que_downloadfile'),
    path('que_file_delete/<int:pk>/', views.que_file_delete, name='que_file_delete'),
    path('com_delete/<int:no>/<int:qno>/', views.com_delete, name='com_delete'),


]