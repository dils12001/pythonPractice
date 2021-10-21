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
from django.urls import path, include, re_path

from myApp import views

urlpatterns = (
    path('admin/', admin.site.urls),
    # 反向解析url : include(('url路徑', '應用名稱'), namespace='為此路徑命名')
    path('myApp/', include(('myApp.urls', 'myApp'), namespace='toApp')),
    path('a<int:num>', views.num),
    # 使用正則表達式時，用 re_path 方法
    # ^b b開頭
    # (\d+) 至少一個數字，並且會被當成變數傳入views.num，因為有加()
    # /$ 以 / 結尾
    path('', views.home),
    path('login/', views.login),
    path('login/verify/', views.verify),
    path('logout/', views.log_out),
    re_path(r'^b(\d+)/$', views.num),
    re_path(r'^get/$', views.get),

)
