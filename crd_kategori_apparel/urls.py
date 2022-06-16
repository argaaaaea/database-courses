from django.urls import path

from . import views

app_name = 'crd_kategori_apparel'

urlpatterns = [
    path('create', views.create_kategori_apparel, name='create_kategori_apparel'),
    path('read', views.read_kategori_apparel, name='read_kategori_apparel'),
    path('delete/<str:category>', views.delete_kategori_apparel, name='delete_kategori_apparel')
]