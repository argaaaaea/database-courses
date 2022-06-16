from django.urls import path

from . import views

app_name = 'warna_kulit'

urlpatterns = [
    path('', views.login, name='login'),
    path('read_warna_kulit/', views.read_warna_kulit, name='read_warna_kulit'),
    path('create_warna_kulit/', views.create_warna_kulit_view, name='create_warna_kulit'),
]