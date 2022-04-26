from django.urls import path
from . import views



app_name = 'asregister'

urlpatterns = [
    path('', views.index, name='index'),
    path('as_insert', views.as_insert, name='as_insert'),
    path('as_list', views.as_list, name='as_list'),
    path('AsUploadFile/<int:pk>/', views.AsUploadFile, name='AsUploadFile'),
    path('as_detail/<int:pk>/', views.as_detail, name='as_detail'),
    path('as_modify/<int:pk>/', views.as_modify, name='as_modify'),
    path('as_delete/<int:pk>/', views.as_delete, name='as_delete'),
    path('assearchResult/', views.assearchResult, name='assearchResult'),
]
