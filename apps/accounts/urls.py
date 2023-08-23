from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit/<str:user_id>/', views.edit, name="edit"),
    path('export-users/', views.export_users, name='export_users'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),

    path('users/', views.users, name="users"),
    path('user/<int:user_id>/', views.user, name="user"),
    path('add_user/', views.add_user, name="add_user"),
]