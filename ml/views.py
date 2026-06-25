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
    tipo = request.data.get("tipo_modelo", "random_forest")
    usar_smote = request.data.get("usar_smote", False)
    try:
        resultado = entrenar_modelo(tipo_modelo=tipo, usar_smote=usar_smote)
        return Response(resultado)
    except Exception as e:
        return Response({"error": True, "mensaje": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predecir(request):
    from ml_engine import predecir_paciente
    try:
        resultado = predecir_paciente(request.data)
        return Response(resultado)
    except Exception as e:
        return Response({"error": True, "mensaje": str(e)}, status=500)


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
            "predicciones_guardadas": actualizados,
        })
    except Exception as e:
        return Response({"error": True, "mensaje": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def segmentar(request):
    from ml_engine import segmentar_pacientes
    n_clusters = request.data.get("n_clusters", 4)
    try:
        resultado = segmentar_pacientes(n_clusters=n_clusters)
        return Response(resultado)
    except Exception as e:
        return Response({"error": True, "mensaje": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detectar_anomalias(request):
    from ml_engine import detectar_anomalias
    contamination = request.data.get("contamination", 0.05)
    try:
        resultado = detectar_anomalias(contamination=contamination)
        return Response(resultado)
    except Exception as e:
        return Response({"error": True, "mensaje": str(e)}, status=500)
