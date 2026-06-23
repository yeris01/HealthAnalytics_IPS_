from django.contrib import admin
from .models import Paciente, LogETL

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id_paciente', 'nombres', 'apellidos', 'edad', 'sexo', 'riesgo_enfermedad', 'es_critico')
    list_filter = ('sexo', 'riesgo_enfermedad', 'es_critico', 'fumador')
    search_fields = ('id_paciente', 'nombres', 'apellidos', 'diagnostico_preliminar')

@admin.register(LogETL)
class LogETLAdmin(admin.ModelAdmin):
    list_display = ('estado', 'archivo_fuente', 'registros_extraidos', 'registros_cargados', 'tiempo_ejecucion', 'fecha_inicio')
    list_filter = ('estado',)
