from django.urls import path

from . import views

app_name = 'crud_koleksi'

urlpatterns = [
    path('create', views.create_koleksi, name='create_koleksi'),
    path('create/rambut', views.create_koleksi_rambut, name='create_koleksi_rambut'),
    path('create/mata', views.create_koleksi_mata, name='create_koleksi_mata'),
    path('create/rumah', views.create_koleksi_rumah, name='create_koleksi_rumah'),
    path('create/barang', views.create_koleksi_barang, name='create_koleksi_barang'),
    path('create/apparel', views.create_koleksi_apparel, name='create_koleksi_apparel'),
    path('read', views.read_koleksi, name='read_koleksi'),
    path('read/rambut', views.read_koleksi_rambut, name='read_koleksi_rambut'),
    path('read/mata', views.read_koleksi_mata, name='read_koleksi_mata'),
    path('read/rumah', views.read_koleksi_rumah, name='read_koleksi_rumah'),
    path('read/barang', views.read_koleksi_barang, name='read_koleksi_barang'),
    path('read/apparel', views.read_koleksi_apparel, name='read_koleksi_apparel'),
]