from django.urls import path, re_path
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('home/', views.home, name='home'),
    # r'^market/(\d+)(/\d*)?/$'
    re_path(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # 驗證帳號是否存在
    path('checkuserid/', views.checkuserid, name='checkuserid'),
    path('quit/', views.quit, name='quit'),
    re_path(r'^changeCart/(\d+)/$', views.changeCart, name='changeCart'),
    path('saveOrder/', views.saveOrder, name='saveOrder'),
    path('showMyOrders/', views.showMyOrders, name='showMyOrders'),
    re_path(r'^showOrderDetail/a(\d+)/$', views.showOrderDetail, name='showOrderDetail'),
    path('deleteOrder/', views.deleteOrder, name='deleteOrder'),
]