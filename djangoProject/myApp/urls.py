from django.urls import path, re_path
from . import views

urlpatterns = (
    path('getUsers/', views.getUsers),
    path('addUsers/', views.addUsers),
    path('delUsers/', views.delUsers),
    path('updateUser/', views.updateUser),
    path('getDepts/', views.getDept),
    # name屬性 : 反向解析url，參考 getDepts.html
    re_path(r'^getDepts/(\d+)/$', views.getDeptUser, name='deptUsers'),
    re_path(r'^registerPage/$', views.registerPage),
    re_path(r'^registerPage/registUser/$', views.registUser),
    path('profile/', views.profilePage),
    path('profile/saveProfile/', views.saveProfilePage),
)