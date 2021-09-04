from django.urls import path, re_path

from myApp import views

urlpatterns = (
    path('getUsers/', views.getUsers),
    path('addUsers/', views.addUsers),
    path('delUsers/', views.delUsers),
    path('updateUser/', views.updateUser),
    path('getDepts/', views.getDept),
    re_path(r'getDepts/(\d+)/$', views.getDeptUser),
)