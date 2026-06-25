from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, Case, When, IntegerField
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
    return render(request, 'dashboard/pacientes.html')

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
    criterio = request.GET.get('q', '').strip()
    if criterio:
        qs = qs.filter(
            models.Q(nombres__icontains=criterio) |
            models.Q(apellidos__icontains=criterio) |
            models.Q(id_paciente__icontains=criterio) |
            models.Q(diagnostico_preliminar__icontains=criterio)
        )
    if request.GET.get('critico') == 'true':
        qs = qs.filter(es_critico=True)
    riesgo = request.GET.get('riesgo')
    if riesgo in ('bajo', 'medio', 'alto', 'critico'):
        qs = qs.filter(riesgo_enfermedad=riesgo)
    sexo = request.GET.get('sexo')
    if sexo in ('M', 'F'):
        qs = qs.filter(sexo=sexo)
    orden = request.GET.get('orden', 'apellidos')
    if orden in ('id_paciente', 'apellidos', 'edad', 'riesgo_enfermedad', 'imc', 'es_critico'):
        if orden == 'riesgo_enfermedad':
            qs = qs.order_by(
                models.Case(
                    models.When(riesgo_enfermedad='critico', then=0),
                    models.When(riesgo_enfermedad='alto', then=1),
                    models.When(riesgo_enfermedad='medio', then=2),
                    models.When(riesgo_enfermedad='bajo', then=3),
                    output_field=models.IntegerField(),
                )
            )
        else:
            qs = qs.order_by(orden)
    try:
        pagina = int(request.GET.get('pagina', 1))
        por_pagina = int(request.GET.get('por_pagina', 50))
    except ValueError:
        pagina, por_pagina = 1, 50
    total = qs.count()
    inicio = (pagina - 1) * por_pagina
    fin = inicio + por_pagina
    resultados = qs[inicio:fin]
    return Response({
        'total': total,
        'pagina': pagina,
        'por_pagina': por_pagina,
        'total_paginas': max(1, -(-total // por_pagina)),
        'resultados': PacienteSerializer(resultados, many=True).data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paciente_detalle_api(request, paciente_id):
    try:
        paciente = Paciente.objects.get(id_paciente=paciente_id)
        return Response(PacienteSerializer(paciente).data)
    except Paciente.DoesNotExist:
        return Response({'error': 'Paciente no encontrado'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuarios_api(request):
    return Response(UsuarioSerializer(Usuario.objects.all().order_by('username'), many=True).data)
