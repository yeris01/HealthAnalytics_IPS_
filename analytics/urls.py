from django.urls import path
from . import views
app_name = 'analytics'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/analytics/edad/', views.edad, name='api_edad'),
    path('api/analytics/imc/', views.imc, name='api_imc'),
    path('api/analytics/tendencia/', views.tendencia, name='api_tendencia'),
    path('api/analytics/sexo/', views.sexo, name='api_sexo'),
    path('api/analytics/criticos/', views.criticos, name='api_criticos'),
]
