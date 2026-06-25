# Resumen de corrección — HealthAnalytics IPS

Se reparó el proyecto adjunto para convertirlo en una aplicación **Django Full Stack funcional**. El paquete original contenía archivos sueltos y referencias a apps inexistentes; por ello se reconstruyó la estructura completa esperada por la propia documentación del reto.

## Cambios principales

| Área | Corrección aplicada |
|---|---|
| Estructura Django | Se agregó `manage.py`, paquete `config/`, `settings.py`, `urls.py`, `wsgi.py` y `asgi.py`. |
| Apps | Se crearon las apps `authentication`, `etl`, `dashboard`, `analytics`, `ml` y `reports`. |
| Autenticación | Se implementó el modelo `Usuario`, login web, logout, registro, perfil, listado y autenticación JWT. |
| ETL | Se implementaron modelos `Paciente` y `LogETL`, serializadores, vistas y endpoints. También se corrigió el bug donde una variable local `pd` sobrescribía `pandas as pd`. |
| Dashboard | Se conectaron KPIs, pacientes, usuarios y endpoints usados por la plantilla existente. |
| Analítica | Se agregaron endpoints de edad, IMC, tendencia, sexo y pacientes críticos. |
| Machine Learning | Se conectaron endpoints para entrenamiento, predicción individual y predicción masiva usando `ml_engine.py`. |
| Reportes | Se agregó pantalla básica de reportes y exportación CSV de pacientes. |
| Dependencias | Se corrigió `requirements.txt` con rangos compatibles y se agregó `whitenoise`. |
| Plantillas | Se reubicaron `base.html`, `index.html` y `login.html` en `templates/`; se añadieron plantillas mínimas para módulos faltantes. |
| Datos iniciales | Se agregó `scripts/crear_usuarios.py` con usuarios demo. |

## Verificación realizada

Se ejecutaron correctamente:

```bash
python3.11 manage.py check
python3.11 manage.py makemigrations authentication etl
python3.11 manage.py migrate --noinput
python3.11 manage.py shell < scripts/crear_usuarios.py
```

También se ejecutó el ETL completo, con resultado exitoso:

| Métrica | Resultado |
|---|---:|
| Registros extraídos | 1800 |
| Duplicados eliminados | 180 |
| Registros cargados | 1620 |
| Errores de carga | 0 |

Finalmente se verificaron páginas HTML y APIs principales, incluyendo autenticación JWT y predicción ML:

```text
OK HTML /dashboard/
OK HTML /dashboard/pacientes/
OK HTML /etl/
OK HTML /analytics/
OK HTML /ml/
OK HTML /reports/
OK API /api/dashboard/kpis/
OK API /api/pacientes/
OK API /api/analytics/edad/
OK API /api/analytics/imc/
OK API /api/analytics/tendencia/
OK API /api/analytics/sexo/
OK API /api/analytics/criticos/
OK API /api/etl/resumen/
OK API /api/etl/logs/
OK API /api/auth/login/
OK API /api/ml/predecir/
```

## Cómo ejecutarlo

```bash
cd reto_fullstack
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < scripts/crear_usuarios.py
python manage.py runserver 0.0.0.0:8000
```

Credenciales demo:

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `medico` | `medico123` | Médico |
| `analista` | `analista123` | Analista |

La base SQLite incluida ya contiene migraciones aplicadas, usuarios demo, datos ETL y artefactos ML generados durante la verificación.

## Complementos añadidos (actualización)

- **EXTRACT desde el Excel entregado**: el ETL ahora usa como fuente principal el dataset clínico oficial `datasets/dataset_clinico_etl_1800_registros.xlsx` (lector universal CSV/Excel `leer_dataset`). Solo genera datos simulados si no encuentra el archivo.
- **Carga manual de datasets**: nuevo endpoint `POST /api/etl/subir/` (CSV/Excel) que valida el formato y ejecuta el ETL automáticamente.
- **Página ETL funcional**: botón de ejecución, subida de archivos, resultado del proceso e historial ETL en vivo.
- **Dataset actualizado**: se reemplazó el Excel del proyecto por el archivo entregado (1850 registros → 1800 limpios; 50 duplicados eliminados, 191 nulos corregidos, 0 nulos restantes).
