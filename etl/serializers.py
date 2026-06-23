from rest_framework import serializers
from .models import Paciente, LogETL

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class LogETLSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = LogETL
        fields = '__all__'
