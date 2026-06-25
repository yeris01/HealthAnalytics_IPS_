from django.conf import settings
from django.db import models

class Paciente(models.Model):
    RIESGO_CHOICES = [('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto'), ('critico', 'Crítico')]
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]
    id_paciente = models.IntegerField(unique=True, db_index=True)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    edad = models.PositiveSmallIntegerField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    peso = models.FloatField()
    altura = models.FloatField()
    imc = models.FloatField()
    clasificacion_imc = models.CharField(max_length=50, blank=True)
    presion_sistolica = models.PositiveSmallIntegerField()
    presion_diastolica = models.PositiveSmallIntegerField()
    frecuencia_cardiaca = models.PositiveSmallIntegerField()
    glucosa = models.FloatField()
    colesterol = models.FloatField()
    saturacion_oxigeno = models.FloatField()
    temperatura = models.FloatField()
    antecedentes_familiares = models.BooleanField(default=False)
    fumador = models.BooleanField(default=False)
    consumo_alcohol = models.BooleanField(default=False)
    actividad_fisica = models.CharField(max_length=50, blank=True)
    diagnostico_preliminar = models.CharField(max_length=120, blank=True)
    riesgo_enfermedad = models.CharField(max_length=20, choices=RIESGO_CHOICES, default='bajo')
    fecha_consulta = models.DateField()
    es_critico = models.BooleanField(default=False, db_index=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-es_critico', 'apellidos', 'nombres']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.id_paciente} - {self.nombres} {self.apellidos}'

    def evaluar_criticidad(self):
        self.es_critico = (
            self.riesgo_enfermedad in ['alto', 'critico'] or
            self.presion_sistolica >= 160 or self.presion_diastolica >= 100 or
            self.glucosa >= 180 or self.saturacion_oxigeno < 92 or
            self.temperatura >= 39 or self.imc >= 35
        )
        return self.es_critico

    def save(self, *args, **kwargs):
        self.evaluar_criticidad()
        super().save(*args, **kwargs)

class LogETL(models.Model):
    ESTADOS = [('en_proceso', 'En proceso'), ('exitoso', 'Exitoso'), ('error', 'Error')]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_proceso')
    archivo_fuente = models.CharField(max_length=255, blank=True)
    registros_extraidos = models.IntegerField(default=0)
    registros_duplicados = models.IntegerField(default=0)
    registros_nulos_corregidos = models.IntegerField(default=0)
    registros_invalidos = models.IntegerField(default=0)
    registros_cargados = models.IntegerField(default=0)
    tiempo_ejecucion = models.FloatField(default=0)
    mensaje = models.TextField(blank=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Log ETL'
        verbose_name_plural = 'Logs ETL'

    def __str__(self):
        return f'ETL {self.estado} - {self.fecha_inicio:%Y-%m-%d %H:%M}'
