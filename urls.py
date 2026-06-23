from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'authentication'

urlpatterns = [
    # HTML views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # API endpoints
    path('api/auth/login/', views.CustomTokenObtainPairView.as_view(), name='api_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('api/auth/registro/', views.registro_usuario, name='api_registro'),
    path('api/auth/perfil/', views.perfil_usuario, name='api_perfil'),
    path('api/auth/usuarios/', views.listar_usuarios, name='api_usuarios'),
    path('api/auth/logout/', views.logout_api, name='api_logout'),
]
