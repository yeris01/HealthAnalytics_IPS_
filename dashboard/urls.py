from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('api/dashboard/kpis/', views.kpis_api, name='api_kpis'),
    path('api/pacientes/', views.pacientes_api, name='api_pacientes'),
    path('api/dashboard/usuarios/', views.usuarios_api, name='api_usuarios'),
]
