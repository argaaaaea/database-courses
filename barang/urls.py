from django.urls import path

from . import views

app_name = 'barang'

urlpatterns = [
    path('', views.login, name='login'),
    path('admin_read_barang/', views.admin_read_barang, name='admin_read_barang'),
    path('pemain_read_barang/', views.pemain_read_barang, name='pemain_read_barang'),
    path('menggunakan_barang/', views.pemain_menggunakan_barang, name='pemain_menggunakan_barang'),
]