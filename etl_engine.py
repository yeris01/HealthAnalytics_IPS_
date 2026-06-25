"""
Motor ETL para HealthAnalytics IPS
Proceso: Extract -> Transform -> Load
"""
import os
import time
import random
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
from django.conf import settings

logger = logging.getLogger(__name__)

NOMBRES = ['Carlos', 'María', 'Juan', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sandra',
           'Jorge', 'Patricia', 'Andrés', 'Claudia', 'Miguel', 'Diana', 'Roberto',
           'Natalia', 'Felipe', 'Valentina', 'Sergio', 'Camila', 'Alejandro', 'Paola']

APELLIDOS = ['García', 'Martínez', 'López', 'González', 'Rodríguez', 'Hernández',
             'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera',
             'Gómez', 'Díaz', 'Cruz', 'Morales', 'Reyes', 'Jiménez', 'Vargas', 'Castillo']

DIAGNOSTICOS_CORRECTOS = [
    'hipertensión', 'diabetes tipo 2', 'obesidad', 'asma', 'artritis',
    'hipotiroidismo', 'anemia', 'insuficiencia renal', 'cardiopatía isquémica',
    'enfermedad pulmonar obstructiva', 'depresión', 'ansiedad', 'migraña',
    'gastritis', 'reflujo gastroesofágico', 'sano'
]

DIAGNOSTICOS_CON_ERRORES = [
    'hipertencion', 'hipertensíon', 'Hipertension', 'HIPERTENSION',
    'diabetis', 'Diabetes tipo2', 'DIABETES',
    'Obesidad', 'OBESIDAD', 'obezidad',
    'asma', 'Asma', 'ASMA',
    'artritis', 'Artritis', 'artritiz',
]


def generar_dataset(n_registros=1800, ruta_salida=None):
    """Genera un dataset clínico simulado con errores intencionales."""
    random.seed(42)
    np.random.seed(42)

    if ruta_salida is None:
        ruta_salida = os.path.join(settings.BASE_DIR, 'datasets', 'dataset_clinico_raw.csv')

    registros = []
    n_base = int(n_registros * 0.85)  # 85% registros base
    n_duplicados = int(n_registros * 0.10)  # 10% duplicados
    n_invalidos = n_registros - n_base - n_duplicados  # 5% inválidos

    for i in range(1, n_base + 1):
        edad = random.randint(18, 85)
        sexo = random.choice(['M', 'F'])
        peso = round(random.uniform(45, 120), 1)
        altura = round(random.uniform(1.50, 1.90), 2)
        imc = round(peso / (altura ** 2), 2)
        ps = random.randint(90, 200)
        presion_diastolica = random.randint(60, 120)
        fc = random.randint(55, 110)
        glucosa = round(random.uniform(70, 350), 1)
        colesterol = round(random.uniform(120, 300), 1)
        sat_o2 = round(random.uniform(80, 100), 1)
        temp = round(random.uniform(35.5, 40.0), 1)
        ant_fam = random.choice([True, False])
        fumador = random.choice([True, False])
        alcohol = random.choice([True, False])
        actividad = random.choice(['sedentario', 'leve', 'moderado', 'intenso'])
        diagnostico = random.choice(DIAGNOSTICOS_CORRECTOS)

        # Clasificar riesgo
        score = 0
        if ps > 160: score += 2
        elif ps > 140: score += 1
        if glucosa > 200: score += 2
        elif glucosa > 126: score += 1
        if imc > 35: score += 2
        elif imc > 30: score += 1
        if fumador: score += 1
        if ant_fam: score += 1
        if sat_o2 < 90: score += 2

        if score >= 6:
            riesgo = 'critico'
        elif score >= 4:
            riesgo = 'alto'
        elif score >= 2:
            riesgo = 'medio'
        else:
            riesgo = 'bajo'

        fecha = date(2023, 1, 1) + timedelta(days=random.randint(0, 500))

        registros.append({
            'id_paciente': i,
            'nombres': random.choice(NOMBRES),
            'apellidos': random.choice(APELLIDOS),
            'edad': edad,
            'sexo': sexo,
            'peso': peso,
            'altura': altura,
            'IMC': imc,
            'presión_sistólica': ps,
            'presión_diastólica': presion_diastolica,
            'frecuencia_cardiaca': fc,
            'glucosa': glucosa,
            'colesterol': colesterol,
            'saturación_oxígeno': sat_o2,
            'temperatura': temp,
            'antecedentes_familiares': ant_fam,
            'fumador': fumador,
            'consumo_alcohol': alcohol,
            'actividad_física': actividad,
            'diagnóstico_preliminar': diagnostico,
            'riesgo_enfermedad': riesgo,
            'fecha_consulta': fecha.strftime('%Y-%m-%d'),
        })

    # Agregar duplicados
    base_muestra = random.sample(registros[:n_base], n_duplicados)
    for reg in base_muestra:
        dup = reg.copy()
        dup['id_paciente'] = reg['id_paciente']  # mismo ID = duplicado
        registros.append(dup)

    # Agregar registros con errores
    for i in range(n_invalidos):
        idx = random.randint(0, n_base - 1)
        reg = registros[idx].copy()
        reg['id_paciente'] = n_base + n_duplicados + i + 1
        tipo_error = random.randint(0, 4)
        if tipo_error == 0:
            reg['glucosa'] = None
        elif tipo_error == 1:
            reg['peso'] = 420  # valor atípico
        elif tipo_error == 2:
            reg['edad'] = 'Treinta'  # tipo incorrecto
        elif tipo_error == 3:
            reg['presión_sistólica'] = 'Alta'  # tipo incorrecto
        elif tipo_error == 4:
            reg['temperatura'] = 28  # valor atípico
        reg['diagnóstico_preliminar'] = random.choice(DIAGNOSTICOS_CON_ERRORES)
        registros.append(reg)

    # Mezclar
    random.shuffle(registros)

    df = pd.DataFrame(registros)
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df.to_csv(ruta_salida, index=False, encoding='utf-8')
    logger.info(f"Dataset generado: {len(df)} registros -> {ruta_salida}")
    return ruta_salida, len(df)


def limpiar_diagnostico(diag):
    """Normaliza diagnósticos con errores ortográficos."""
    if not isinstance(diag, str):
        return 'sin diagnóstico'
    diag = diag.strip().lower()
    mapeo = {
        'hipertencion': 'hipertensión',
        'hipertensíon': 'hipertensión',
        'hipertension': 'hipertensión',
        'diabetis': 'diabetes tipo 2',
        'diabetes tipo2': 'diabetes tipo 2',
        'diabetes': 'diabetes tipo 2',
        'obezidad': 'obesidad',
        'artritiz': 'artritis',
    }
    for clave, valor in mapeo.items():
        if clave in diag:
            return valor
    return diag


def transformar_dataset(df_raw):
    """Aplica todas las transformaciones ETL al DataFrame."""
    stats = {
        'total_raw': len(df_raw),
        'duplicados_eliminados': 0,
        'nulos_corregidos': 0,
        'invalidos_corregidos': 0,
    }

    df = df_raw.copy()

    # --- Eliminar duplicados ---
    antes = len(df)
    df = df.drop_duplicates(subset=['id_paciente'], keep='first')
    stats['duplicados_eliminados'] = antes - len(df)

    # --- Convertir tipos ---
    def to_numeric_safe(val, tipo=float, default=None):
        try:
            return tipo(val)
        except (ValueError, TypeError):
            return default

    df['edad'] = df['edad'].apply(lambda x: to_numeric_safe(x, int, None))
    df['presión_sistólica'] = df['presión_sistólica'].apply(lambda x: to_numeric_safe(x, int, None))
    df['presión_diastólica'] = df['presión_diastólica'].apply(lambda x: to_numeric_safe(x, int, None))
    df['glucosa'] = df['glucosa'].apply(lambda x: to_numeric_safe(x, float, None))
    df['peso'] = df['peso'].apply(lambda x: to_numeric_safe(x, float, None))
    df['altura'] = df['altura'].apply(lambda x: to_numeric_safe(x, float, None))
    df['colesterol'] = df['colesterol'].apply(lambda x: to_numeric_safe(x, float, None))
    df['saturación_oxígeno'] = df['saturación_oxígeno'].apply(lambda x: to_numeric_safe(x, float, None))
    df['temperatura'] = df['temperatura'].apply(lambda x: to_numeric_safe(x, float, None))
    df['frecuencia_cardiaca'] = df['frecuencia_cardiaca'].apply(lambda x: to_numeric_safe(x, int, None))

    # --- Validar rangos clínicos (valores atípicos -> NaN) ---
    rangos_clinicos = {
        'edad': (0, 120),
        'peso': (10, 300),
        'altura': (0.50, 2.50),
        'temperatura': (33, 43),
        'presión_sistólica': (50, 250),
        'presión_diastólica': (30, 150),
        'frecuencia_cardiaca': (20, 220),
        'glucosa': (20, 500),
        'colesterol': (50, 500),
        'saturación_oxígeno': (50, 100),
        'imc': (10, 60),
    }
    for col, (min_val, max_val) in rangos_clinicos.items():
        if col in df.columns:
            df.loc[df[col] < min_val, col] = np.nan
            df.loc[df[col] > max_val, col] = np.nan

    # --- Tratar nulos con estadísticas ---
    nulos_antes = df.isnull().sum().sum()
    columnas_numericas = ['edad', 'peso', 'altura', 'presión_sistólica', 'presión_diastólica',
                          'frecuencia_cardiaca', 'glucosa', 'colesterol', 'saturación_oxígeno',
                          'temperatura']
    for col in columnas_numericas:
        if col in df.columns:
            mediana = df[col].median()
            df[col] = df[col].fillna(mediana)

    stats['nulos_corregidos'] = int(nulos_antes - df.isnull().sum().sum())
    stats['invalidos_corregidos'] = stats['nulos_corregidos']

    # --- Normalizar sexo ---
    df['sexo'] = df['sexo'].str.strip().str.upper()
    df['sexo'] = df['sexo'].map({'M': 'M', 'F': 'F', 'MASCULINO': 'M', 'FEMENINO': 'F'}).fillna('M')

    # --- Normalizar actividad física ---
    df['actividad_física'] = df['actividad_física'].str.strip().str.lower()
    actividades_validas = ['sedentario', 'leve', 'moderado', 'intenso']
    df.loc[~df['actividad_física'].isin(actividades_validas), 'actividad_física'] = 'sedentario'

    # --- Normalizar diagnósticos ---
    df['diagnóstico_preliminar'] = df['diagnóstico_preliminar'].apply(limpiar_diagnostico)

    # --- Calcular IMC ---
    df['IMC'] = df.apply(
        lambda r: round(r['peso'] / (r['altura'] ** 2), 2) if r['altura'] > 0 else r.get('IMC', 0),
        axis=1
    )

    # --- Clasificación IMC ---
    def clasificar_imc(imc):
        if imc < 18.5:
            return 'Bajo peso'
        elif imc < 25:
            return 'Normal'
        elif imc < 30:
            return 'Sobrepeso'
        else:
            return 'Obesidad'

    df['clasificacion_imc'] = df['IMC'].apply(clasificar_imc)

    # --- Recalcular riesgo ---
    def calcular_riesgo(row):
        score = 0
        if row['presión_sistólica'] > 160:
            score += 2
        elif row['presión_sistólica'] > 140:
            score += 1
        if row['glucosa'] > 200:
            score += 2
        elif row['glucosa'] > 126:
            score += 1
        if row['IMC'] > 35:
            score += 2
        elif row['IMC'] > 30:
            score += 1
        if row.get('fumador', False):
            score += 1
        if row.get('antecedentes_familiares', False):
            score += 1
        if row['saturación_oxígeno'] < 90:
            score += 2
        if score >= 6:
            return 'critico'
        elif score >= 4:
            return 'alto'
        elif score >= 2:
            return 'medio'
        else:
            return 'bajo'

    df['riesgo_enfermedad'] = df.apply(calcular_riesgo, axis=1)

    # --- Detectar críticos ---
    df['es_critico'] = (
        (df['presión_sistólica'] > 180) |
        (df['glucosa'] > 300) |
        (df['saturación_oxígeno'] < 85)
    )

    # --- Convertir booleanos ---
    for col in ['antecedentes_familiares', 'fumador', 'consumo_alcohol', 'es_critico']:
        if col in df.columns:
            df[col] = df[col].map({True: True, False: False, 'True': True, 'False': False,
                                   'true': True, 'false': False, 1: True, 0: False}).fillna(False)

    # --- Convertir fecha ---
    df['fecha_consulta'] = pd.to_datetime(df['fecha_consulta'], errors='coerce').dt.date
    df['fecha_consulta'] = df['fecha_consulta'].fillna(date.today())

    # Renombrar columnas para compatibilidad con modelo Django
    df = df.rename(columns={
        'presión_sistólica': 'presion_sistolica',
        'presión_diastólica': 'presion_diastolica',
        'frecuencia_cardiaca': 'frecuencia_cardiaca',
        'saturación_oxígeno': 'saturacion_oxigeno',
        'actividad_física': 'actividad_fisica',
        'diagnóstico_preliminar': 'diagnostico_preliminar',
        'antecedentes_familiares': 'antecedentes_familiares',
        'IMC': 'imc',
    })

    # --- Anomalías detectadas (valores atípicos pero no fuera de rango) ---
    anomalias = []
    if 'presión_sistólica' in df.columns:
        q1, q3 = df['presión_sistólica'].quantile([0.25, 0.75])
        iqr = q3 - q1
        mask = (df['presión_sistólica'] < (q1 - 1.5 * iqr)) | (df['presión_sistólica'] > (q3 + 1.5 * iqr))
        anomalias.append(('presión_sistólica', int(mask.sum())))
    if 'glucosa' in df.columns:
        q1, q3 = df['glucosa'].quantile([0.25, 0.75])
        iqr = q3 - q1
        mask = (df['glucosa'] < (q1 - 1.5 * iqr)) | (df['glucosa'] > (q3 + 1.5 * iqr))
        anomalias.append(('glucosa', int(mask.sum())))

    stats['total_limpio'] = len(df)
    stats['anomalias'] = dict(anomalias)
    stats['calidad_general'] = round(
        (stats['total_limpio'] / max(stats['total_raw'], 1)) * 100 *
        (1 - stats['nulos_corregidos'] / max(stats['total_raw'] * 10, 1)), 1
    )
    return df, stats


def cargar_en_bd(df_limpio):
    """Carga el DataFrame limpio en la base de datos."""
    from etl.models import Paciente

    cargados = 0
    errores = 0

    for _, row in df_limpio.iterrows():
        try:
            Paciente.objects.update_or_create(
                id_paciente=int(row['id_paciente']),
                defaults={
                    'nombres': str(row['nombres']),
                    'apellidos': str(row['apellidos']),
                    'edad': int(row['edad']),
                    'sexo': str(row['sexo']),
                    'peso': float(row['peso']),
                    'altura': float(row['altura']),
                    'imc': float(row['imc']),
                    'clasificacion_imc': str(row.get('clasificacion_imc', '')),
                    'presion_sistolica': int(row['presion_sistolica']),
                    'presion_diastolica': int(row['presion_diastolica']),
                    'frecuencia_cardiaca': int(row['frecuencia_cardiaca']),
                    'glucosa': float(row['glucosa']),
                    'colesterol': float(row['colesterol']),
                    'saturacion_oxigeno': float(row['saturacion_oxigeno']),
                    'temperatura': float(row['temperatura']),
                    'antecedentes_familiares': bool(row['antecedentes_familiares']),
                    'fumador': bool(row['fumador']),
                    'consumo_alcohol': bool(row['consumo_alcohol']),
                    'actividad_fisica': str(row['actividad_fisica']),
                    'diagnostico_preliminar': str(row['diagnostico_preliminar']),
                    'riesgo_enfermedad': str(row['riesgo_enfermedad']),
                    'fecha_consulta': row['fecha_consulta'],
                    'es_critico': bool(row['es_critico']),
                }
            )
            cargados += 1
        except Exception as e:
            errores += 1
            logger.warning(f"Error cargando paciente {row.get('id_paciente', '?')}: {e}")

    return cargados, errores


def leer_dataset(ruta):
    """Lee un dataset clínico desde CSV o Excel (xlsx/xls)."""
    ext = os.path.splitext(ruta)[1].lower()
    if ext in ('.xlsx', '.xls'):
        return pd.read_excel(ruta)
    return pd.read_csv(ruta, encoding='utf-8')


def dataset_entregado():
    """Devuelve la ruta del Excel clínico entregado con el reto, si existe."""
    candidatos = [
        os.path.join(settings.BASE_DIR, 'datasets', 'dataset_clinico_etl_1800_registros.xlsx'),
        os.path.join(settings.BASE_DIR, 'dataset_clinico_etl_1800_registros.xlsx'),
    ]
    for ruta in candidatos:
        if os.path.exists(ruta):
            return ruta
    return None


def generar_perfil_calidad(datos_limpios, stats):
    """Genera un perfil detallado de calidad de datos."""
    perfil = {**stats}
    if datos_limpios is not None and not datos_limpios.empty:
        df = datos_limpios
        perfil['columnas'] = list(df.columns)
        perfil['total_columnas'] = len(df.columns)
        perfil['memoria_kb'] = round(df.memory_usage(deep=True).sum() / 1024, 2)
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols):
            perfil['estadisticas'] = {
                col: {
                    'min': round(float(df[col].min()), 2),
                    'max': round(float(df[col].max()), 2),
                    'media': round(float(df[col].mean()), 2),
                    'mediana': round(float(df[col].median()), 2),
                    'std': round(float(df[col].std()), 2),
                    'nulos': int(df[col].isnull().sum()),
                    'unicos': int(df[col].nunique()),
                }
                for col in num_cols[:20]
            }
        perfil['distribucion_sexo'] = df['sexo'].value_counts().to_dict() if 'sexo' in df else {}
        perfil['distribucion_riesgo'] = df['riesgo_enfermedad'].value_counts().to_dict() if 'riesgo_enfermedad' in df else {}
    return perfil


def ejecutar_etl_completo(usuario=None, archivo_csv=None):
    """Ejecuta el proceso ETL completo: Extract -> Transform -> Load.

    Orden de prioridad de la fuente de datos (EXTRACT):
    1. Archivo cargado manualmente (CSV/Excel).
    2. Dataset clínico entregado con el reto (Excel oficial).
    3. Dataset simulado generado automáticamente (fallback).
    """
    from etl.models import LogETL

    log = LogETL.objects.create(usuario=usuario, estado='en_proceso')
    inicio = time.time()

    try:
        # 1. EXTRACT
        entregado = dataset_entregado()
        if archivo_csv and os.path.exists(archivo_csv):
            df_raw = leer_dataset(archivo_csv)
            log.archivo_fuente = os.path.basename(archivo_csv)
        elif entregado:
            df_raw = leer_dataset(entregado)
            log.archivo_fuente = os.path.basename(entregado)
        else:
            ruta, _ = generar_dataset()
            df_raw = pd.read_csv(ruta, encoding='utf-8')
            log.archivo_fuente = 'dataset_clinico_raw.csv (generado)'

        log.registros_extraidos = len(df_raw)

        # 2. TRANSFORM
        df_limpio, stats = transformar_dataset(df_raw)
        log.registros_duplicados = stats['duplicados_eliminados']
        log.registros_nulos_corregidos = stats['nulos_corregidos']
        log.registros_invalidos = stats['invalidos_corregidos']

        # Exportar CSV limpio
        ruta_limpio = os.path.join(settings.BASE_DIR, 'datasets', 'dataset_clinico_limpio.csv')
        df_limpio.to_csv(ruta_limpio, index=False, encoding='utf-8')

        # 3. LOAD
        cargados, errores = cargar_en_bd(df_limpio)
        log.registros_cargados = cargados

        fin = time.time()
        log.tiempo_ejecucion = round(fin - inicio, 2)
        log.estado = 'exitoso'
        log.mensaje = (
            f"ETL completado exitosamente. "
            f"Extraídos: {log.registros_extraidos}, "
            f"Duplicados eliminados: {log.registros_duplicados}, "
            f"Nulos corregidos: {log.registros_nulos_corregidos}, "
            f"Cargados: {cargados}, Errores: {errores}. "
            f"Tiempo: {log.tiempo_ejecucion}s"
        )
        log.save()
        return log

    except Exception as e:
        fin = time.time()
        log.tiempo_ejecucion = round(fin - inicio, 2)
        log.estado = 'error'
        log.mensaje = f"Error en ETL: {str(e)}"
        log.save()
        logger.error(f"Error en ETL: {e}", exc_info=True)
        raise
