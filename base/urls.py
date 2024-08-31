from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('room/', views.room, name='room'),
    path('get_token/', views.get_token, name='get_token'),
    path('create_member/', views.create_user, name='create_member'),
    path('get_member/', views.get_members, name='get_member'),
    path('delete_member/', views.delete_member, name='delete_member'),
]