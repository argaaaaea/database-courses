from django.urls import path

from . import views

app_name = 'menjalankan_misi_utama'

urlpatterns = [
    path('', views.login, name='login'),
    path('admin_read_menjalankan_misi_utama/', views.admin_read_menjalankan_misi_utama, name='admin_read_menjalankan_misi_utama'),
    path('pemain_read_menjalankan_misi_utama/', views.pemain_read_menjalankan_misi_utama, name='pemain_read_menjalankan_misi_utama'),
    path('pemain_menjalankan_misi_utama/', views.pemain_menjalankan_misi_utama, name='pemain_menjalankan_misi_utama'),
    path('pemain_update_menjalankan_misi_view/<str:namaTokoh>/<str:namaMisi>', views.pemain_update_menjalankan_misi_view, name='pemain_update_menjalankan_misi_view'),
]