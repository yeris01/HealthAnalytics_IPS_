# 📁 Estructura del Proyecto HealthAnalytics IPS

## Árbol de Directorios Completo

```
healthcare-etl-platform/
│
├── 📄 README.md                    # Documentación principal
├── 📄 QUICK_START.md              # Guía de inicio rápido
├── 📄 ESTRUCTURA_PROYECTO.md      # Este archivo
├── 📄 requirements.txt            # Dependencias Python
├── 📄 manage.py                   # Gestor de Django
├── 📄 .gitignore                  # Archivos ignorados por Git
│
├── 📁 config/                     # Configuración Django
│   ├── __init__.py
│   ├── settings.py                # Configuración principal
│   ├── urls.py                    # URLs globales
│   ├── asgi.py                    # ASGI
│   ├── wsgi.py                    # WSGI
│   └── migrations/
│
├── 📁 authentication/             # Módulo de autenticación
│   ├── __init__.py
│   ├── models.py                  # Modelo Usuario personalizado
│   ├── views.py                   # Vistas de login/logout
│   ├── serializers.py             # Serializers JWT
│   ├── urls.py                    # URLs de autenticación
│   ├── admin.py                   # Admin Django
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│       └── 0001_initial.py
│
├── 📁 etl/                        # Módulo ETL
│   ├── __init__.py
│   ├── models.py                  # Modelos Paciente, LogETL
│   ├── etl_engine.py              # Motor ETL completo
│   ├── views.py                   # Vistas ETL
│   ├── serializers.py             # Serializers
│   ├── urls.py                    # URLs ETL
│   ├── admin.py                   # Admin Django
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│       └── 0001_initial.py
│
├── 📁 analytics/                  # Módulo de analítica
│   ├── __init__.py
│   ├── views.py                   # Vistas de analítica
│   ├── urls.py                    # URLs analytics
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│
├── 📁 ml/                         # Módulo Machine Learning
│   ├── __init__.py
│   ├── models.py                  # Modelo ModeloML
│   ├── ml_engine.py               # Motor ML (Random Forest, etc)
│   ├── views.py                   # Vistas ML
│   ├── serializers.py             # Serializers
│   ├── urls.py                    # URLs ML
│   ├── admin.py                   # Admin Django
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│       └── 0001_initial.py
│
├── 📁 dashboard/                  # Módulo dashboard
│   ├── __init__.py
│   ├── views.py                   # Vistas principales
│   ├── urls.py                    # URLs dashboard
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│
├── 📁 reports/                    # Módulo de reportes
│   ├── __init__.py
│   ├── views.py                   # Vistas de exportación
│   ├── urls.py                    # URLs reportes
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│
├── 📁 templates/                  # Templates HTML
│   ├── base.html                  # Template base (navbar, sidebar)
│   ├── authentication/
│   │   └── login.html             # Página de login
│   └── dashboard/
│       ├── index.html             # Dashboard principal
│       ├── pacientes.html         # Gestión de pacientes
│       ├── etl.html               # Interfaz ETL
│       ├── analytics.html         # Analítica
│       ├── ml.html                # Machine Learning
│       ├── reportes.html          # Reportes
│       └── usuarios.html          # Gestión de usuarios
│
├── 📁 static/                     # Archivos estáticos
│   ├── css/
│   │   └── style.css              # Estilos personalizados
│   ├── js/
│   │   └── main.js                # JavaScript principal
│   └── img/
│       └── logo.png               # Logo de la aplicación
│
├── 📁 datasets/                   # Datos clínicos
│   ├── dataset_clinico_etl_1800_registros.xlsx  # Dataset original
│   ├── dataset_clinico_raw.csv    # CSV generado (raw)
│   ├── dataset_clinico_limpio.csv # CSV procesado (limpio)
│   ├── modelo_ml.pkl              # Modelo ML serializado
│   └── scaler_ml.pkl              # Scaler ML serializado
│
├── 📁 docs/                       # Documentación técnica
│   ├── ARQUITECTURA.md            # Diseño del sistema
│   ├── API.md                     # Referencia de APIs
│   ├── ETL.md                     # Proceso ETL detallado
│   ├── ML.md                      # Machine Learning
│   ├── DEPLOYMENT.md              # Guía de despliegue
│   └── DIAGRAMA_FLUJO.md          # Diagramas de flujo
│
├── 📁 scripts/                    # Scripts de utilidad
│   ├── crear_usuarios.py          # Crear usuarios de prueba
│   ├── cargar_dataset.py          # Cargar dataset Excel
│   ├── entrenar_ml.py             # Entrenar modelos
│   └── generar_reportes.py        # Generar reportes
│
├── 📁 media/                      # Archivos subidos
│   └── uploads/                   # Archivos CSV cargados
│
└── 📁 staticfiles/                # Archivos estáticos compilados (producción)
```

---

## 📊 Modelos de Datos

### Usuario (authentication/models.py)
```python
- id (PK)
- username (unique)
- email
- password (hashed)
- rol (administrador, medico, analista)
- first_name, last_name
- telefono
- fecha_creacion
- is_active, is_staff, is_superuser
```

### Paciente (etl/models.py)
```python
- id (PK)
- id_paciente (unique)
- nombres, apellidos
- edad, sexo
- peso, altura, imc, clasificacion_imc
- presion_sistolica, presion_diastolica
- frecuencia_cardiaca
- glucosa, colesterol
- saturacion_oxigeno, temperatura
- antecedentes_familiares, fumador, consumo_alcohol
- actividad_fisica
- diagnostico_preliminar
- riesgo_enfermedad
- fecha_consulta
- fecha_carga
- es_critico
```

### LogETL (etl/models.py)
```python
- id (PK)
- fecha_ejecucion
- usuario (FK)
- registros_extraidos
- registros_duplicados
- registros_nulos_corregidos
- registros_invalidos
- registros_cargados
- tiempo_ejecucion
- estado (exitoso, error, en_proceso)
- mensaje
- archivo_fuente
```

### ModeloML (ml/models.py)
```python
- id (PK)
- tipo (random_forest, logistic_regression, decision_tree)
- fecha_entrenamiento
- usuario (FK)
- accuracy, precision, recall, f1_score
- total_entrenamiento, total_prueba
- activo
- metricas_json
```

---

## 🔗 URLs Principales

| Ruta | Módulo | Descripción |
|------|--------|-------------|
| `/` | dashboard | Redirige a dashboard |
| `/login/` | authentication | Página de login |
| `/logout/` | authentication | Cerrar sesión |
| `/dashboard/` | dashboard | Dashboard principal |
| `/dashboard/pacientes/` | dashboard | Gestión de pacientes |
| `/dashboard/usuarios/` | dashboard | Gestión de usuarios (admin) |
| `/etl/` | etl | Interfaz ETL |
| `/analytics/` | analytics | Analítica de datos |
| `/ml/` | ml | Machine Learning |
| `/reportes/` | reports | Generación de reportes |
| `/admin/` | django.admin | Admin de Django |

---

## 🔌 Endpoints de API

### Autenticación
- `POST /api/auth/login/` - Obtener tokens JWT
- `POST /api/auth/refresh/` - Renovar access token
- `POST /api/auth/registro/` - Registrar nuevo usuario
- `GET /api/auth/perfil/` - Obtener perfil del usuario
- `GET /api/auth/usuarios/` - Listar usuarios (admin)
- `POST /api/auth/logout/` - Cerrar sesión

### ETL
- `POST /api/etl/run/` - Ejecutar ETL
- `POST /api/etl/upload/` - Cargar CSV
- `GET /api/etl/historial/` - Historial de ETL
- `GET /api/pacientes/` - Listar pacientes
- `GET /api/pacientes/{id}/` - Detalle de paciente

### Analítica
- `GET /api/dashboard/kpis/` - Obtener KPIs
- `GET /api/analytics/estadisticas/` - Estadísticas descriptivas
- `GET /api/analytics/edad/` - Distribución por edad
- `GET /api/analytics/diagnostico/` - Distribución por diagnóstico
- `GET /api/analytics/imc/` - Distribución por IMC
- `GET /api/analytics/sexo/` - Segmentación por sexo
- `GET /api/analytics/criticos/` - Pacientes críticos
- `GET /api/analytics/tendencia/` - Tendencia de consultas

### Machine Learning
- `POST /api/ml/entrenar/` - Entrenar modelo
- `POST /api/ml/predecir/` - Predecir riesgo
- `POST /api/ml/predecir-todos/` - Predecir todos
- `GET /api/ml/historial/` - Historial de modelos
- `GET /api/ml/metricas/` - Métricas del último modelo

### Reportes
- `GET /api/reportes/csv/` - Exportar CSV
- `GET /api/reportes/excel/` - Exportar Excel
- `GET /api/reportes/pdf/` - Exportar PDF

---

## 🔐 Roles y Permisos

| Funcionalidad | Admin | Médico | Analista |
|---------------|-------|--------|----------|
| Ver Dashboard | ✅ | ✅ | ✅ |
| Ver Pacientes | ✅ | ✅ | ✅ |
| Ejecutar ETL | ✅ | ❌ | ✅ |
| Cargar CSV | ✅ | ❌ | ✅ |
| Ver Analítica | ✅ | ✅ | ✅ |
| Entrenar ML | ✅ | ❌ | ✅ |
| Generar Reportes | ✅ | ✅ | ✅ |
| Gestionar Usuarios | ✅ | ❌ | ❌ |
| Acceder a Admin | ✅ | ❌ | ❌ |

---

## 📦 Dependencias Principales

```
Django==5.2.14              # Framework web
djangorestframework==3.14.0 # APIs REST
pandas==2.2.0               # Procesamiento de datos
scikit-learn==1.8.0         # Machine Learning
openpyxl==3.11.0            # Manejo de Excel
reportlab==4.0.9            # Generación de PDF
```

---

## 🚀 Flujo de Desarrollo

1. **Desarrollo Local**
   - Clonar repositorio
   - Crear entorno virtual
   - Instalar dependencias
   - Ejecutar migraciones
   - Cargar datos de prueba
   - Ejecutar servidor

2. **Testing**
   - Pruebas unitarias
   - Pruebas de integración
   - Pruebas de APIs (Postman)

3. **Despliegue**
   - Configurar variables de entorno
   - Ejecutar migraciones en producción
   - Configurar servidor web (Gunicorn)
   - Configurar reverse proxy (Nginx)
   - Configurar SSL/TLS

---

**Última actualización:** Mayo 21, 2024
**Versión:** 1.0

