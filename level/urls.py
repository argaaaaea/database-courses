from django.urls import path

from . import views

app_name = 'level'

urlpatterns = [
    path('', views.login, name='login'),
    path('read_level/', views.read_level, name='read_level'),
    path('create_level/', views.create_level_view, name='create_level'),
    path('update_level/<level>/<xp>', views.update_level_view, name='update_level'),
]