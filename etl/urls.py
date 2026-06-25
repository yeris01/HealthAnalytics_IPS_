from django.urls import path
from . import views
app_name = 'etl'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/etl/ejecutar/', views.ejecutar_etl, name='api_ejecutar'),
    path('api/etl/subir/', views.subir_dataset, name='api_subir'),
    path('api/etl/logs/', views.logs_etl, name='api_logs'),
    path('api/etl/resumen/', views.resumen_etl, name='api_resumen'),
    path('api/etl/calidad/', views.calidad_datos, name='api_calidad'),
]
