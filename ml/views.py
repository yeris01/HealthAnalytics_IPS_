from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from etl.models import Paciente


@login_required
def index(request):

    paciente_id = request.GET.get('paciente')

    paciente = None

    if paciente_id:
        paciente = Paciente.objects.filter(
            id_paciente=paciente_id
        ).first()

    return render(
        request,
        'ml/index.html',
        {
            'paciente': paciente
        }
    )


# ==========================
# ENTRENAR MODELO
# ==========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def entrenar(request):

    from ml_engine import entrenar_modelo

    tipo = request.data.get("tipo_modelo", "random_forest")

    try:

        resultado = entrenar_modelo(
            tipo_modelo=tipo
        )

        return Response(resultado)

    except Exception as e:

        return Response(
            {
                "error": True,
                "mensaje": str(e)
            },
            status=500
        )


# ==========================
# PREDECIR UN PACIENTE
# ==========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predecir(request):

    from ml_engine import predecir_paciente

    try:

        resultado = predecir_paciente(
            request.data
        )

        return Response(resultado)

    except Exception as e:

        return Response(
            {
                "error": True,
                "mensaje": str(e)
            },
            status=500
        )


# ==========================
# PREDECIR TODOS
# ==========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predecir_todos(request):

    from ml_engine import predecir_todos_pacientes

    try:

        actualizados = predecir_todos_pacientes()

        total = Paciente.objects.count()

        return Response({

            "mensaje": "Predicciones realizadas correctamente.",

            "pacientes_procesados": total,

            "predicciones_guardadas": actualizados

        })

    except Exception as e:

        return Response({

            "error": True,

            "mensaje": str(e)

        }, status=500)
    
# ==========================
# DIAGNÓSTICO INDIVIDUAL
# ==========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnostico_paciente(request, id_paciente):

    from ml_engine import predecir_paciente

    try:

        paciente = Paciente.objects.get(
            id_paciente=id_paciente
        )

        datos = {
            'edad': paciente.edad,
            'imc': paciente.imc,
            'glucosa': paciente.glucosa,
            'colesterol': paciente.colesterol,
            'presion_sistolica': paciente.presion_sistolica,
            'presion_diastolica': paciente.presion_diastolica,
            'frecuencia_cardiaca': paciente.frecuencia_cardiaca,
            'saturacion_oxigeno': paciente.saturacion_oxigeno,
            'temperatura': paciente.temperatura,
            'fumador': paciente.fumador,
            'antecedentes_familiares': paciente.antecedentes_familiares,
            'consumo_alcohol': paciente.consumo_alcohol,
        }

        resultado = predecir_paciente(datos)

        return Response({
            'paciente': f'{paciente.nombres} {paciente.apellidos}',
            'riesgo_actual': paciente.riesgo_enfermedad,
            'riesgo_predicho': resultado['riesgo_predicho'],
            'confianza': resultado['confianza'],
            'probabilidades': resultado['probabilidades'],
            'es_critico': paciente.es_critico
        })

    except Exception as e:

        return Response({
            'error': str(e)
        }, status=500)