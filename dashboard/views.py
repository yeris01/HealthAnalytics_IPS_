from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Count, Avg
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.models import Usuario
from authentication.serializers import UsuarioSerializer
from etl.models import Paciente, LogETL
from etl.serializers import PacienteSerializer

def calcular_kpis():
    distribucion = dict(
        Paciente.objects.values_list('riesgo_enfermedad')
        .annotate(total=Count('id'))
    )

    return {
        'total_pacientes': Paciente.objects.count(),
        'pacientes_criticos': Paciente.objects.filter(es_critico=True).count(),
        'pacientes_hipertensos': Paciente.objects.filter(presion_sistolica__gte=140).count(),
        'pacientes_diabeticos': Paciente.objects.filter(glucosa__gte=126).count(),
        'pacientes_fumadores': Paciente.objects.filter(fumador=True).count(),
        'pacientes_obesidad': Paciente.objects.filter(imc__gte=30).count(),

        # NUEVOS KPI
        'edad_promedio': round(Paciente.objects.aggregate(Avg('edad'))['edad__avg'] or 0, 1),
        'imc_promedio': round(Paciente.objects.aggregate(Avg('imc'))['imc__avg'] or 0, 1),
        'glucosa_promedio': round(Paciente.objects.aggregate(Avg('glucosa'))['glucosa__avg'] or 0, 1),
        'presion_promedio': round(Paciente.objects.aggregate(Avg('presion_sistolica'))['presion_sistolica__avg'] or 0, 1),

        'distribucion_riesgo': distribucion,
    }
@login_required
def index(request):
    return render(request, 'dashboard/index.html', {'kpis': calcular_kpis(), 'logs_recientes': LogETL.objects.all()[:5]})

@login_required
def pacientes(request):
    qs = Paciente.objects.all()
    if request.GET.get('critico') == 'true':
        qs = qs.filter(es_critico=True)
    return render(request, 'dashboard/pacientes.html', {'pacientes': qs[:200]})

@login_required
def usuarios(request):
    return render(request, 'dashboard/usuarios.html', {'usuarios': Usuario.objects.all().order_by('username')})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kpis_api(request):
    return Response(calcular_kpis())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pacientes_api(request):
    qs = Paciente.objects.all()
    if request.GET.get('critico') == 'true':
        qs = qs.filter(es_critico=True)
    return Response(PacienteSerializer(qs[:500], many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuarios_api(request):
    return Response(UsuarioSerializer(Usuario.objects.all().order_by('username'), many=True).data)
