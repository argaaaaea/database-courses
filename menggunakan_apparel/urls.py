from django.urls import path

from . import views

app_name = 'menggunakan_apparel'

urlpatterns = [
    path('', views.login, name='login'),
    path('admin_read_menggunakan_apparel/', views.admin_read_menggunakan_apparel, name='admin_read_menggunakan_apparel'),
    path('pemain_read_menggunakan_apparel/', views.pemain_read_menggunakan_apparel, name='pemain_read_menggunakan_apparel'),
    path('create_menggunakan_apparel/', views.create_menggunakan_apparel_view, name='create_menggunakan_apparel'),
]