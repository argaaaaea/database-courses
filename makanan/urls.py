from django.urls import path

from . import views

app_name = 'makanan'

urlpatterns = [
    path('', views.login, name='login'),
    path('admin_read_makanan/', views.admin_read_makanan, name='admin_read_makanan'),
    path('pemain_read_makanan/', views.pemain_read_makanan, name='pemain_read_makanan'),
    path('admin_create_makanan/', views.admin_create_makanan_view, name="create_makanan"),
    path('admin_delete_makanan/<str:nama>', views.admin_delete_makanan, name='admin_delete_makanan'),
     path('admin_update_makanan_view/<str:nama>', views.admin_update_makanan_view, name='admin_update_makanan_view'),

]