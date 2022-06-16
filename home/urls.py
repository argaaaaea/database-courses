from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.landing_page, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('admin_homepage/', views.admin_homepage, name='admin_homepage'),
    path('pemain_homepage/', views.pemain_homepage, name='pemain_homepage'),
]