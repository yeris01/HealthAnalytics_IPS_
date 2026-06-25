from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from etl.models import Paciente, LogETL
from etl.serializers import PacienteSerializer
from etl_engine import transformar_dataset, limpiar_diagnostico
import pandas as pd
import numpy as np

Usuario = get_user_model()


class TestLimpiarDiagnostico(TestCase):
    def test_diagnostico_correcto(self):
        self.assertEqual(limpiar_diagnostico('hipertensión'), 'hipertensión')

    def test_diagnostico_con_error_ortografico(self):
        self.assertEqual(limpiar_diagnostico('hipertencion'), 'hipertensión')
        self.assertEqual(limpiar_diagnostico('diabetis'), 'diabetes tipo 2')
        self.assertEqual(limpiar_diagnostico('obezidad'), 'obesidad')
        self.assertEqual(limpiar_diagnostico('artritiz'), 'artritis')

    def test_diagnostico_none(self):
        self.assertEqual(limpiar_diagnostico(None), 'sin diagnóstico')

    def test_diagnostico_vacio(self):
        self.assertEqual(limpiar_diagnostico(''), 'sin diagnóstico')


class TestTransformarDataset(TestCase):
    def setUp(self):
        self.df_raw = pd.DataFrame({
            'id_paciente': [1, 2, 2, 3],
            'nombres': ['Carlos', 'María', 'María', 'Luis'],
            'apellidos': ['García', 'López', 'López', 'Martínez'],
            'edad': [45, 30, 30, 'Treinta'],
            'sexo': ['M', 'F', 'F', 'M'],
            'peso': [80.0, 65.0, 65.0, 420.0],
            'altura': [1.75, 1.60, 1.60, 1.80],
            'IMC': [26.12, 25.39, 25.39, 129.63],
            'presión_sistólica': [120, 110, 110, 130],
            'presión_diastólica': [80, 70, 70, 85],
            'frecuencia_cardiaca': [72, 80, 80, 75],
            'glucosa': [95.0, 110.0, 110.0, None],
            'colesterol': [180.0, 200.0, 200.0, 190.0],
            'saturación_oxígeno': [98.0, 97.0, 97.0, 96.0],
            'temperatura': [36.5, 36.8, 36.8, 28.0],
            'antecedentes_familiares': [False, True, True, False],
            'fumador': [False, False, False, True],
            'consumo_alcohol': [True, False, False, False],
            'actividad_física': ['moderado', 'leve', 'leve', 'sedentario'],
            'diagnóstico_preliminar': ['hipertensión', 'sano', 'sano', 'diabetis'],
            'riesgo_enfermedad': ['medio', 'bajo', 'bajo', 'alto'],
            'fecha_consulta': ['2023-06-15', '2023-07-20', '2023-07-20', '2023-08-10'],
        })

    def test_elimina_duplicados(self):
        df_limpio, stats = transformar_dataset(self.df_raw)
        self.assertEqual(stats['duplicados_eliminados'], 1)
        self.assertEqual(len(df_limpio), 3)

    def test_corrige_tipos_edad(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        self.assertFalse(df_limpio['edad'].isnull().any())
        self.assertTrue((df_limpio['edad'] >= 0).all())
        self.assertTrue((df_limpio['edad'] <= 120).all())

    def test_valida_rangos_peso(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        self.assertFalse(df_limpio['peso'].isnull().any())
        self.assertTrue((df_limpio['peso'] <= 300).all())

    def test_valida_rangos_temperatura(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        self.assertTrue((df_limpio['temperatura'] >= 33).all())

    def test_calcula_imc(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        imc_esperado = round(80.0 / (1.75 ** 2), 2)
        self.assertEqual(df_limpio.iloc[0]['imc'], imc_esperado)

    def test_clasifica_imc(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        self.assertIn('clasificacion_imc', df_limpio.columns)

    def test_normaliza_diagnostico(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        diag = df_limpio[df_limpio['id_paciente'] == 3]['diagnostico_preliminar'].values
        self.assertEqual(diag[0], 'diabetes tipo 2')

    def test_calcula_riesgo(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        self.assertIn('riesgo_enfermedad', df_limpio.columns)
        self.assertIn(df_limpio['riesgo_enfermedad'].iloc[0], ['bajo', 'medio', 'alto', 'critico'])

    def test_detecta_criticos(self):
        df_limpio, _ = transformar_dataset(self.df_raw)
        self.assertIn('es_critico', df_limpio.columns)
        self.assertIsInstance(df_limpio['es_critico'].iloc[0], (bool, np.bool_))


class TestPacienteModel(TestCase):
    def setUp(self):
        self.paciente = Paciente.objects.create(
            id_paciente=1, nombres='Carlos', apellidos='García',
            edad=45, sexo='M', peso=80.0, altura=1.75, imc=26.12,
            presion_sistolica=180, presion_diastolica=100,
            frecuencia_cardiaca=72, glucosa=95.0, colesterol=180.0,
            saturacion_oxigeno=98.0, temperatura=36.5,
            antecedentes_familiares=False, fumador=False,
            consumo_alcohol=True, actividad_fisica='moderado',
            diagnostico_preliminar='hipertensión',
            riesgo_enfermedad='alto', fecha_consulta='2023-06-15',
        )

    def test_criticidad_alta_presion(self):
        self.assertTrue(self.paciente.es_critico)

    def test_str_representation(self):
        self.assertIn('Carlos', str(self.paciente))


class TestETLApi(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_superuser('admin', 'admin@test.com', 'admin123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_resumen_etl(self):
        response = self.client.get('/api/etl/resumen/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pacientes', response.data)

    def test_logs_etl_vacio(self):
        response = self.client.get('/api/etl/logs/')
        self.assertEqual(response.status_code, 200)


class TestDashboardApi(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user('analista', 'a@test.com', 'pass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_kpis(self):
        response = self.client.get('/api/dashboard/kpis/')
        self.assertEqual(response.status_code, 200)

    def test_pacientes_sin_datos(self):
        response = self.client.get('/api/pacientes/')
        self.assertEqual(response.status_code, 200)

    def test_pacientes_con_filtro_riesgo(self):
        response = self.client.get('/api/pacientes/?riesgo=alto')
        self.assertEqual(response.status_code, 200)


class TestAnalyticsApi(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user('analista', 'a@test.com', 'pass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_edad_endpoint(self):
        response = self.client.get('/api/analytics/edad/')
        self.assertEqual(response.status_code, 200)

    def test_imc_endpoint(self):
        response = self.client.get('/api/analytics/imc/')
        self.assertEqual(response.status_code, 200)

    def test_tendencia_endpoint(self):
        response = self.client.get('/api/analytics/tendencia/')
        self.assertEqual(response.status_code, 200)

    def test_sexo_endpoint(self):
        response = self.client.get('/api/analytics/sexo/')
        self.assertEqual(response.status_code, 200)
