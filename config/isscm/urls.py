from django.urls import path
from . import views


app_name = 'isscm'

urlpatterns = [
    path('', views.index, name='index'),

]

