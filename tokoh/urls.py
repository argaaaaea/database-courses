from django.urls import path

from . import views

app_name = 'tokoh'

urlpatterns = [
    path('admin_read_tokoh', views.admin_read_tokoh, name='admin_read_tokoh'),
    path('pemain_read_tokoh', views.pemain_read_tokoh, name='pemain_read_tokoh'),
    path('admin_read_warna_kulit', views.admin_read_warna_kulit, name='admin_read_warna_kulit'),
    path('pemain_read_warna_kulit', views.pemain_read_warna_kulit, name='pemain_read_warna_kulit'),
    path('pemain_create_tokoh', views.pemain_create_tokoh, name="pemain_create_tokoh"),
    path('pemain_update_tokoh', views.pemain_update_tokoh, name="pemain_update_tokoh"),
    path('admin_detail_page', views.admin_detail_page, name='admin_detail_tokoh'),
    path('pemain_detail_page', views.pemain_detail_page, name='pemain_detail_tokoh'),
]
