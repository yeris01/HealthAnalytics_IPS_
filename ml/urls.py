from django.urls import path
from . import views
app_name = 'ml'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/ml/entrenar/', views.entrenar, name='api_entrenar'),
    path('api/ml/predecir/', views.predecir, name='api_predecir'),
    path('api/ml/predecir-todos/', views.predecir_todos, name='api_predecir_todos'),
    path('api/ml/segmentar/', views.segmentar, name='api_segmentar'),
    path('api/ml/anomalias/', views.detectar_anomalias, name='api_anomalias'),
]
