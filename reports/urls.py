from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/reports/resumen/', views.resumen, name='api_resumen'),

    # Exportaciones
    path('exportar/pacientes.csv', views.exportar_csv, name='exportar_csv'),
    path('exportar/pacientes.pdf', views.exportar_pdf, name='exportar_pdf'),
]