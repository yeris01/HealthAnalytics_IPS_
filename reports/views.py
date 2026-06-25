from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dashboard.views import calcular_kpis
from etl.models import Paciente

@login_required
def index(request):
    return render(request, 'reports/index.html', {'kpis': calcular_kpis()})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resumen(request):
    return Response(calcular_kpis())

@login_required
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="pacientes.csv"'
    response.write('id_paciente,nombres,apellidos,edad,sexo,riesgo,critico\n')
    for p in Paciente.objects.all():
        response.write(f'{p.id_paciente},{p.nombres},{p.apellidos},{p.edad},{p.sexo},{p.riesgo_enfermedad},{p.es_critico}\n')
    return response

@login_required
def exportar_pdf(request):
    buffer = BytesIO()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pacientes.pdf"'

    doc = SimpleDocTemplate(buffer)

    datos = [
        ['ID', 'Nombres', 'Apellidos', 'Edad', 'Sexo', 'Riesgo', 'Crítico']
    ]

    for p in Paciente.objects.all():
        datos.append([
            str(p.id_paciente),
            p.nombres,
            p.apellidos,
            str(p.edad),
            p.sexo,
            p.riesgo_enfermedad,
            str(p.es_critico)
        ])

    tabla = Table(datos)

    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066FF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    doc.build([tabla])

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response