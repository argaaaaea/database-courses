from django.urls import path

from . import views

app_name = 'pekerjaan'

urlpatterns = [
    path('read_pekerjaan', views.read_pekerjaan, name='read_pekerjaan'),
    path('read_bekerja', views.read_bekerja, name="read_bekerja"),
    path('create_pekerjaan', views.admin_create_pekerjaan_view, name="create_pekerjaan"),
    path('pemain_create_bekerja', views.pemain_create_bekerja_view, name="create_bekerja"),
    path('admin_update_pekerjaan', views.admin_update_pekerjaan, name="admin_update_pekerjaan"),
]