from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from etl.models import Paciente


@login_required
def index(request):
    return render(request, 'ml/index.html')


# ==========================
# ENTRENAR MODELO
# ==========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def entrenar(request):

    from ml_engine import entrenar_modelo

    tipo = request.data.get("tipo_modelo", "random_forest")

    try:

        resultado = entrenar_modelo(tipo_modelo=tipo)

        return Response(resultado)

    except Exception as e:

        return Response({
            "error": True,
            "mensaje": str(e)
        }, status=500)


# ==========================
# PREDECIR UN PACIENTE
# ==========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predecir(request):

    from ml_engine import predecir_paciente

    try:

        resultado = predecir_paciente(request.data)

        return Response(resultado)

    except Exception as e:

        return Response({
            "error": True,
            "mensaje": str(e)
        }, status=500)


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