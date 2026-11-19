from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/', views.settings, name='settings'),
    path('roles/', views.roles, name='roles'),
    path('audit-logs/', views.audit_logs, name='audit-logs'),
]
