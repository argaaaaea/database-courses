from django.urls import path

from . import views

app_name = 'misi_utama'

urlpatterns = [
    path('', views.login, name='login'),
    path('admin_read_misi_utama/', views.admin_read_misi_utama, name='admin_read_misi_utama'),
    path('admin_detail_misi_utama/<str:nama>', views.admin_detail_misi_utama, name='admin_detail_misi_utama'),
    path('pemain_read_misi_utama/', views.pemain_read_misi_utama, name='pemain_read_misi_utama'),
    path('pemain_detail_misi_utama/<str:nama>', views.pemain_detail_misi_utama, name='pemain_detail_misi_utama'),
    path('admin_create_misi/', views.admin_create_misi_view, name="create_misi"),
    path('admin_delete_misi_utama/<str:nama>', views.admin_delete_misi_utama, name='admin_delete_misi_utama'),

]