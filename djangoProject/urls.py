"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include

import jian.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('multiply', include('mutiply.urls')),
    path('jian', include('jian.urls')),
    path('plus', include('plus.urls')),
    path('division', include('divide.urls')),
    path('testdemo', jian.views.testdemo),
    path('list/', include('list.urls')),
    path('result', include('result.urls'))
]
