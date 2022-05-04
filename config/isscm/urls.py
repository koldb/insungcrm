from django.urls import path
from . import views

app_name = 'isscm'

urlpatterns = [
    path('', views.index, name='index'),
    path('sheet_insert', views.sheet_insert, name='sheet_insert'),
    path('order_insert', views.order_insert, name='order_insert'),
    path('sheet_list', views.sheet_list, name='sheet_list'),
    path('order_list', views.order_list, name='order_list'),
    path('uploadFile/<int:pk>/', views.uploadFile, name='uploadFile'),
    path('order_uploadFile/<int:pk>/', views.order_uploadFile, name='order_uploadFile'),
    path('sheet_detail/<int:pk>/', views.sheet_detail, name='sheet_detail'),
    path('order_delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('order_modify/<int:pk>/', views.order_modify, name='order_modify'),
    path('sheet_modify/<int:pk>/', views.sheet_modify, name='sheet_modify'),
    path('sheet_delete/<int:pk>/', views.sheet_delete, name='sheet_delete'),
    path('searchResult/', views.searchResult, name='searchResult'),
    path('ordersearchResult/', views.ordersearchResult, name='ordersearchResult'),

]

