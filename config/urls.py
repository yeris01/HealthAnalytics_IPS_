from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from dashboard import views as dashboard_views
from analytics import views as analytics_views
from etl import views as etl_views
from ml import views as ml_views
from reports import views as reports_views

urlpatterns = [
    path('', lambda request: redirect('dashboard:index') if request.user.is_authenticated else redirect('authentication:login'), name='home'),
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('etl/', include('etl.urls')),
    path('analytics/', include('analytics.urls')),
    path('ml/', include('ml.urls')),
    path('reports/', include('reports.urls')),

    # API global usada por las plantillas y clientes externos.
    path('api/dashboard/kpis/', dashboard_views.kpis_api, name='api_dashboard_kpis_global'),
    path('api/pacientes/', dashboard_views.pacientes_api, name='api_pacientes_global'),
    path('api/pacientes/<int:paciente_id>/', dashboard_views.paciente_detalle_api, name='api_paciente_detalle_global'),
    path('api/dashboard/usuarios/', dashboard_views.usuarios_api, name='api_dashboard_usuarios_global'),
    path('api/analytics/edad/', analytics_views.edad, name='api_analytics_edad_global'),
    path('api/analytics/imc/', analytics_views.imc, name='api_analytics_imc_global'),
    path('api/analytics/tendencia/', analytics_views.tendencia, name='api_analytics_tendencia_global'),
    path('api/analytics/sexo/', analytics_views.sexo, name='api_analytics_sexo_global'),
    path('api/analytics/criticos/', analytics_views.criticos, name='api_analytics_criticos_global'),
    path('api/etl/ejecutar/', etl_views.ejecutar_etl, name='api_etl_ejecutar_global'),
    path('api/etl/subir/', etl_views.subir_dataset, name='api_etl_subir_global'),
    path('api/etl/logs/', etl_views.logs_etl, name='api_etl_logs_global'),
    path('api/etl/resumen/', etl_views.resumen_etl, name='api_etl_resumen_global'),
    path('api/etl/calidad/', etl_views.calidad_datos, name='api_etl_calidad_global'),
    path('api/ml/entrenar/', ml_views.entrenar, name='api_ml_entrenar_global'),
    path('api/ml/predecir/', ml_views.predecir, name='api_ml_predecir_global'),
    path('api/ml/predecir-todos/', ml_views.predecir_todos, name='api_ml_predecir_todos_global'),
    path('api/ml/segmentar/', ml_views.segmentar, name='api_ml_segmentar_global'),
    path('api/ml/anomalias/', ml_views.detectar_anomalias, name='api_ml_anomalias_global'),
    path('api/reports/resumen/', reports_views.resumen, name='api_reports_resumen_global'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API Docs (Swagger/OpenAPI)
urlpatterns += [
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
