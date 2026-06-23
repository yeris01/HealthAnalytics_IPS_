from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from etl.models import Paciente
from etl.serializers import PacienteSerializer

@login_required
def index(request):
    return render(request, 'analytics/index.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def edad(request):
    grupos = {'0-17': (0, 17), '18-39': (18, 39), '40-59': (40, 59), '60+': (60, 200)}
    return Response([{'grupo': k, 'total': Paciente.objects.filter(edad__gte=a, edad__lte=b).count()} for k, (a, b) in grupos.items()])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def imc(request):
    data = Paciente.objects.values('clasificacion_imc').annotate(total=Count('id')).order_by('clasificacion_imc')
    return Response([{'clasificacion': d['clasificacion_imc'] or 'Sin clasificar', 'total': d['total']} for d in data])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tendencia(request):
    data = Paciente.objects.annotate(m=TruncMonth('fecha_consulta')).values('m').annotate(total=Count('id')).order_by('m')
    return Response([{'mes': d['m'].strftime('%Y-%m') if d['m'] else 'Sin fecha', 'total': d['total']} for d in data])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sexo(request):
    return Response(list(Paciente.objects.values('sexo').annotate(total=Count('id')).order_by('sexo')))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def criticos(request):
    return Response(PacienteSerializer(Paciente.objects.filter(es_critico=True)[:100], many=True).data)
