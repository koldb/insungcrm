"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', include('isscm.urls')),
    path('admin/', admin.site.urls),
    path('estimate/', include('estimate.urls')),
    path('accounts/', include('accounts.urls'), name='accounts'),
    #path('isscm/', include('isscm.urls')),
    path('asregister/', include('asregister.urls')),
    path('question/', include('question.urls')),

]

def protected_file(request, path, document_root=None):
    return redirect('/isscm')

urlpatterns += static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)
