import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LogETL, Paciente
from .serializers import LogETLSerializer

EXTENSIONES_VALIDAS = ('.csv', '.xlsx', '.xls')


@login_required
def index(request):
    return render(request, 'etl/index.html', {'logs': LogETL.objects.all()[:10]})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ejecutar_etl(request):
    from etl_engine import ejecutar_etl_completo
    log = ejecutar_etl_completo(usuario=request.user)
    return Response(LogETLSerializer(log).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def subir_dataset(request):
    """Carga manual de un dataset (CSV/Excel) y ejecuta el ETL automáticamente."""
    from etl_engine import ejecutar_etl_completo

    archivo = request.FILES.get('archivo')
    if not archivo:
        return Response({'error': 'No se envió ningún archivo (campo "archivo").'}, status=400)

    ext = os.path.splitext(archivo.name)[1].lower()
    if ext not in EXTENSIONES_VALIDAS:
        return Response(
            {'error': f'Formato no válido ({ext}). Use CSV o Excel (.csv, .xlsx, .xls).'},
            status=400,
        )

    carpeta = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, archivo.name)
    with open(ruta, 'wb+') as destino:
        for chunk in archivo.chunks():
            destino.write(chunk)

    log = ejecutar_etl_completo(usuario=request.user, archivo_csv=ruta)
    return Response(LogETLSerializer(log).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logs_etl(request):
    return Response(LogETLSerializer(LogETL.objects.all()[:50], many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resumen_etl(request):
    ultimo = LogETL.objects.first()
    return Response({
        'pacientes': Paciente.objects.count(),
        'criticos': Paciente.objects.filter(es_critico=True).count(),
        'ultimo_etl': LogETLSerializer(ultimo).data if ultimo else None,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calidad_datos(request):
    """Devuelve métricas de calidad de datos de los pacientes."""
    from django.db.models import Avg, StdDev, Min, Max, Count, Q
    from etl.models import Paciente
    total = Paciente.objects.count()
    if total == 0:
        return Response({'error': 'No hay datos. Ejecute el ETL primero.'})
    stats = {}
    for campo in ['edad', 'peso', 'altura', 'imc', 'presion_sistolica', 'glucosa', 'colesterol', 'saturacion_oxigeno', 'temperatura']:
        agg = Paciente.objects.aggregate(
            media=Avg(campo), min=Min(campo), max=Max(campo),
            desv_std=StdDev(campo), nulos=Count('id') - Count(campo)
        )
        stats[campo] = {
            'media': round(float(agg['media'] or 0), 2),
            'min': round(float(agg['min'] or 0), 2),
            'max': round(float(agg['max'] or 0), 2),
            'desv_std': round(float(agg['desv_std'] or 0), 2),
            'nulos': int(agg['nulos'] or 0),
        }
    return Response({
        'total_pacientes': total,
        'criticos': Paciente.objects.filter(es_critico=True).count(),
        'distribucion_riesgo': dict(Paciente.objects.values_list('riesgo_enfermedad').annotate(total=Count('id'))),
        'distribucion_sexo': dict(Paciente.objects.values_list('sexo').annotate(total=Count('id'))),
        'distribucion_imc': dict(Paciente.objects.values_list('clasificacion_imc').annotate(total=Count('id'))),
        'fumadores': Paciente.objects.filter(fumador=True).count(),
        'diabeticos': Paciente.objects.filter(glucosa__gte=126).count(),
        'hipertensos': Paciente.objects.filter(presion_sistolica__gte=140).count(),
        'estadisticas': stats,
    })
