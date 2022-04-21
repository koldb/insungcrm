from django.urls import path
from . import views



app_name = 'isscm'

urlpatterns = [
    path('', views.index, name='index'),
    path('sheet_insert', views.sheet_insert, name='sheet_insert'),
    path('sheet_list', views.sheet_list, name='sheet_list'),
    path('uploadFile/<int:pk>/', views.uploadFile, name='uploadFile'),
    path('sheet_detail/<int:pk>/', views.sheet_detail, name='sheet_detail'),
    path('sheet_modify/<int:pk>/', views.sheet_modify, name='sheet_modify'),

]

