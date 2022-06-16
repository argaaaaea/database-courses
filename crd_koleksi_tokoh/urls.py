from django.urls import path

from . import views

app_name = 'crd_koleksi_tokoh'

urlpatterns = [
    path('create', views.create_koleksi_tokoh, name='create_koleksi_tokoh'),
    path('read', views.read_koleksi_tokoh, name='read_koleksi_tokoh'),
    path('delete/<str:id_koleksi>', views.delete_koleksi_tokoh, name='delete_koleksi_tokoh')
]