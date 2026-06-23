from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from etl.models import Paciente

@login_required
def index(request):
    return render(request, 'ml/index.html')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def entrenar(request):
    from ml_engine import entrenar_modelo
    tipo = request.data.get('tipo_modelo', 'random_forest')
    return Response(entrenar_modelo(tipo_modelo=tipo))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predecir(request):
    from ml_engine import predecir_paciente
    return Response(predecir_paciente(request.data))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predecir_todos(request):
    from ml_engine import predecir_todos_pacientes
    return Response({'actualizados': predecir_todos_pacientes(), 'total_pacientes': Paciente.objects.count()})
