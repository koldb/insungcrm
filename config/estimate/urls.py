from django.urls import path
from django.conf.urls import include
from . import views
from . import models

app_name = 'company'

urlpatterns = [
    path('', views.index, name='index'),
    path('cinsert/', views.cinsert, name='cinsert'),
    path('clist/', views.clist, name='clist'),
]

