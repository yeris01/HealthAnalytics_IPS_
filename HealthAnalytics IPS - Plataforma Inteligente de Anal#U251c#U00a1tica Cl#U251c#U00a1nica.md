# HealthAnalytics IPS - Plataforma Inteligente de Analítica Clínica

**Versión:** 1.0  
**Fecha:** Mayo 2024  
**Autor:** Equipo de Desarrollo FullStack

---

## 📋 Descripción General

**HealthAnalytics IPS** es una plataforma web inteligente diseñada para procesar grandes volúmenes de datos clínicos mediante procesos ETL, analítica de datos avanzada y modelos de Machine Learning. El sistema automatiza el procesamiento de información médica y apoya la toma de decisiones clínicas mediante analítica predictiva.

### Problemas que Resuelve

- ✓ Mala calidad de datos clínicos
- ✓ Duplicidad de pacientes
- ✓ Registros médicos inconsistentes
- ✓ Falta de indicadores clínicos
- ✓ Dificultad para detectar pacientes de alto riesgo
- ✓ Ausencia de automatización en análisis predictivo

---

## 🎯 Objetivos Funcionales

1. **Ejecutar proceso ETL completo** (Extract, Transform, Load)
2. **Limpiar y transformar datos clínicos** con validación de rangos
3. **Analizar métricas médicas** y generar KPIs
4. **Detectar pacientes críticos** automáticamente
5. **Predecir riesgos de enfermedades** con Machine Learning
6. **Visualizar información** mediante dashboards interactivos
7. **Exportar reportes** en múltiples formatos (PDF, Excel, CSV)

---

## 🏗️ Arquitectura del Sistema

```
┌────────────────────────────────────────────────────────────────┐
│                    Frontend Web (HTML/CSS/JS)                  │
│              Dashboard Administrativo + Gráficas               │
└────────────────────────┬─────────────────────────────────────┘
                         │ REST APIs
                         ↓
┌────────────────────────────────────────────────────────────────┐
│                  Django Backend (Python 3.12+)                 │
├────────────────────────────────────────────────────────────────┤
│ • Authentication & JWT Tokens                                  │
│ • ETL Engine (Extract, Transform, Load)                        │
│ • Analytics Module (KPIs, Estadísticas)                        │
│ • ML Prediction Module (Random Forest, Logistic Regression)    │
│ • Reporting Module (PDF, Excel, CSV)                           │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
            ┌────────────────────────┐
            │  SQLite / PostgreSQL   │
            │     Clinical DB        │
            └────────────────────────┘
```

### Módulos Principales

| Módulo | Descripción | Responsabilidades |
|--------|-------------|-------------------|
| **authentication** | Autenticación y gestión de usuarios | Login, JWT, Roles (Admin/Médico/Analista) |
| **etl** | Procesamiento de datos clínicos | Extracción, limpieza, transformación, carga |
| **analytics** | Análisis de datos y KPIs | Estadísticas, segmentación, tendencias |
| **ml** | Machine Learning y predicciones | Entrenamiento, predicción, métricas |
| **dashboard** | Interfaz web principal | Vistas, templates, navegación |
| **reports** | Generación de reportes | Exportación PDF, Excel, CSV |

---

## 📊 Tecnologías Utilizadas

### Backend
- **Python 3.12+** - Lenguaje principal
- **Django 5.2** - Framework web
- **Django REST Framework** - APIs REST
- **Django Simple JWT** - Autenticación JWT
- **Pandas** - Procesamiento de datos
- **NumPy** - Cálculos numéricos
- **Scikit-Learn** - Machine Learning
- **ReportLab** - Generación de PDF
- **OpenPyXL** - Manejo de Excel

### Frontend
- **HTML5 / CSS3** - Markup y estilos
- **Bootstrap 5** - Framework CSS
- **Chart.js** - Gráficas interactivas
- **JavaScript Vanilla** - Interactividad

### Base de Datos
- **SQLite** (desarrollo)
- **PostgreSQL** (producción)

### Herramientas
- **Git/GitHub** - Control de versiones
- **Docker** (opcional) - Containerización
- **Postman** - Testing de APIs

---

## 🚀 Instalación y Configuración

### Requisitos Previos

```bash
- Python 3.12+
- pip (gestor de paquetes)
- Git
- PostgreSQL (opcional, para producción)
```

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/healthcare-etl-platform.git
cd healthcare-etl-platform
```

### Paso 2: Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 5: Crear Usuarios de Prueba

```bash
python manage.py createsuperuser
# O ejecutar el script de carga de usuarios
python manage.py shell < scripts/crear_usuarios.py
```

### Paso 6: Cargar Dataset

```bash
python manage.py shell < scripts/cargar_dataset.py
```

### Paso 7: Ejecutar Servidor

```bash
python manage.py runserver
```

Acceder a: `http://localhost:8000`

---

## 📝 Guía de Uso

### 1. Iniciar Sesión

**URL:** `http://localhost:8000/login/`

**Credenciales de Prueba:**
- **Admin:** `admin` / `admin123`
- **Médico:** `medico` / `medico123`
- **Analista:** `analista` / `analista123`

### 2. Dashboard Principal

Visualiza KPIs en tiempo real:
- Total de pacientes
- Pacientes críticos
- Pacientes hipertensos
- Pacientes diabéticos
- Distribuciones por riesgo, edad, IMC

### 3. Gestión de Pacientes

- **Buscar pacientes** por nombre, riesgo o estado crítico
- **Ver detalles** completos de cada paciente
- **Filtrar** por criterios clínicos

### 4. Proceso ETL

- **Ejecutar ETL automático** con dataset generado
- **Cargar CSV personalizado** para procesamiento
- **Ver historial** de procesos ETL ejecutados
- **Monitorear** registros extraídos, duplicados, nulos, cargados

### 5. Analítica de Datos

- **Estadísticas descriptivas** (media, mediana, desviación estándar)
- **Distribuciones** por edad, diagnóstico, IMC, sexo
- **Segmentación de pacientes** por criterios clínicos
- **Detección de pacientes críticos**
- **Tendencias** de consultas mensuales

### 6. Machine Learning

- **Entrenar modelos:**
  - Random Forest (recomendado)
  - Regresión Logística
  - Árbol de Decisión
- **Ver métricas:** Accuracy, Precision, Recall, F1-Score
- **Aplicar predicciones** a todos los pacientes
- **Historial de modelos** entrenados

### 7. Reportes

- **Exportar CSV** - Datos completos en CSV
- **Exportar Excel** - Datos formateados en Excel
- **Exportar PDF** - Reporte profesional en PDF

---

## 🔌 APIs REST

### Autenticación

```
POST /api/auth/login/
Content-Type: application/json
{
  "username": "admin",
  "password": "admin123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "usuario": { ... }
}
```

### Pacientes

```
GET /api/pacientes/
GET /api/pacientes/?riesgo=alto
GET /api/pacientes/?critico=true
GET /api/pacientes/{id}/
```

### ETL

```
POST /api/etl/run/
POST /api/etl/upload/ (multipart/form-data)
GET /api/etl/historial/
```

### Analítica

```
GET /api/dashboard/kpis/
GET /api/analytics/estadisticas/
GET /api/analytics/edad/
GET /api/analytics/diagnostico/
GET /api/analytics/imc/
GET /api/analytics/sexo/
GET /api/analytics/criticos/
GET /api/analytics/tendencia/
```

### Machine Learning

```
POST /api/ml/entrenar/
  { "tipo_modelo": "random_forest" }

POST /api/ml/predecir/
  { "edad": 45, "imc": 28, "glucosa": 150, ... }

POST /api/ml/predecir-todos/

GET /api/ml/historial/
GET /api/ml/metricas/
```

### Reportes

```
GET /api/reportes/csv/
GET /api/reportes/excel/
GET /api/reportes/pdf/
```

---

## 📊 Proceso ETL Detallado

### 1. EXTRACT (Extracción)

- Genera automáticamente dataset clínico simulado (1800 registros)
- Lee archivos CSV externos
- Registra fuente de datos
- Exporta CSV de extracción

**Errores Intencionales Incluidos:**
- Valores nulos
- Tipos de datos incorrectos
- Duplicados de pacientes
- Valores atípicos
- Errores ortográficos

### 2. TRANSFORM (Transformación)

**Limpieza de Datos:**
- Elimina duplicados
- Corrige inconsistencias
- Valida rangos clínicos

**Conversión de Tipos:**
- `edad` → int
- `glucosa` → float
- `sexo` → normalizado (M/F)

**Normalización:**
- Diagnósticos (corrección ortográfica)
- Variables categóricas
- Actividad física

**Tratamiento de Nulos:**
- Media para variables numéricas
- Moda para categóricas
- Reglas clínicas específicas

**Cálculos Automáticos:**
- IMC = peso / altura²
- Clasificación IMC (Bajo peso, Normal, Sobrepeso, Obesidad)
- Riesgo de enfermedad (Bajo, Medio, Alto, Crítico)
- Detección de pacientes críticos

### 3. LOAD (Carga)

- Inserta datos limpios en BD
- Registra logs ETL
- Genera trazabilidad completa
- Crea histórico de ejecuciones

---

## 🤖 Machine Learning

### Modelos Implementados

| Modelo | Ventajas | Desventajas |
|--------|----------|-------------|
| **Random Forest** | Mejor accuracy, maneja no-linealidad | Más lento |
| **Regresión Logística** | Rápido, interpretable | Menos preciso |
| **Árbol de Decisión** | Interpretable, rápido | Overfitting |

### Variables Predictoras

- Edad
- IMC
- Glucosa
- Colesterol
- Presión arterial (sistólica/diastólica)
- Frecuencia cardíaca
- Saturación de oxígeno
- Temperatura
- Fumador (booleano)
- Antecedentes familiares (booleano)
- Consumo de alcohol (booleano)

### Métricas Evaluadas

- **Accuracy** = Predicciones Correctas / Total Predicciones
- **Precision** = TP / (TP + FP)
- **Recall** = TP / (TP + FN)
- **F1-Score** = 2 × (Precision × Recall) / (Precision + Recall)
- **Matriz de Confusión** - Visualización de errores

---

## 📈 KPIs Médicos

| KPI | Descripción | Cálculo |
|-----|-------------|---------|
| **Total Pacientes** | Cantidad total de registros | COUNT(*) |
| **Pacientes Críticos** | Riesgo crítico detectado | PS > 180 OR Glucosa > 300 OR SatO2 < 85 |
| **Pacientes Hipertensos** | Presión sistólica > 140 | COUNT(PS > 140) |
| **Pacientes Diabéticos** | Glucosa > 126 mg/dL | COUNT(Glucosa > 126) |
| **Pacientes Fumadores** | Con antecedente de tabaquismo | COUNT(fumador = True) |
| **Pacientes con Obesidad** | IMC ≥ 30 | COUNT(IMC >= 30) |
| **Riesgo Promedio** | Promedio de puntuación de riesgo | AVG(score_riesgo) |

---

## 🔐 Seguridad

### Autenticación

- **JWT (JSON Web Tokens)** para APIs
- **Session-based** para vistas HTML
- **Tokens con expiración** (8 horas)
- **Refresh tokens** para renovación

### Autorización

**Roles del Sistema:**

| Rol | Funciones |
|-----|-----------|
| **Administrador** | Gestión completa, usuarios, ETL, ML |
| **Médico** | Visualización clínica, consulta de pacientes |
| **Analista** | ETL, analítica, ML, reportes |

### Protecciones

- ✓ CSRF Protection
- ✓ SQL Injection Prevention (ORM)
- ✓ XSS Protection
- ✓ Sanitización de entrada
- ✓ Validación de datos
- ✓ CORS configurado

---

## 📁 Estructura del Proyecto

```
healthcare-etl-platform/
│
├── config/
│   ├── settings.py          # Configuración Django
│   ├── urls.py              # URLs principales
│   ├── wsgi.py              # WSGI
│   └── asgi.py              # ASGI
│
├── authentication/
│   ├── models.py            # Modelo Usuario
│   ├── views.py             # Vistas de autenticación
│   ├── serializers.py       # Serializers JWT
│   ├── urls.py              # URLs de auth
│   └── migrations/
│
├── etl/
│   ├── models.py            # Modelos Paciente, LogETL
│   ├── etl_engine.py        # Motor ETL completo
│   ├── views.py             # Vistas ETL
│   ├── serializers.py       # Serializers
│   ├── urls.py              # URLs ETL
│   └── migrations/
│
├── analytics/
│   ├── views.py             # Vistas de analítica
│   ├── urls.py              # URLs analytics
│   └── migrations/
│
├── ml/
│   ├── models.py            # Modelo ModeloML
│   ├── ml_engine.py         # Motor ML
│   ├── views.py             # Vistas ML
│   ├── serializers.py       # Serializers
│   ├── urls.py              # URLs ML
│   └── migrations/
│
├── dashboard/
│   ├── views.py             # Vistas dashboard
│   ├── urls.py              # URLs dashboard
│   └── migrations/
│
├── reports/
│   ├── views.py             # Vistas reportes
│   ├── urls.py              # URLs reportes
│   └── migrations/
│
├── templates/
│   ├── base.html            # Template base
│   ├── authentication/
│   │   └── login.html
│   └── dashboard/
│       ├── index.html
│       ├── pacientes.html
│       ├── etl.html
│       ├── analytics.html
│       ├── ml.html
│       └── reportes.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── datasets/
│   ├── dataset_clinico_raw.csv
│   ├── dataset_clinico_limpio.csv
│   └── dataset_clinico_etl_1800_registros.xlsx
│
├── docs/
│   ├── ARQUITECTURA.md
│   ├── API.md
│   ├── ETL.md
│   └── ML.md
│
├── manage.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

---

## 🧪 Testing

### Ejecutar Pruebas

```bash
python manage.py test
```

### Pruebas de API (Postman)

1. Importar colección: `docs/HealthAnalytics.postman_collection.json`
2. Configurar variables de entorno
3. Ejecutar pruebas

---

## 📦 Requisitos (requirements.txt)

```
Django==5.2.14
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.2
django-cors-headers==4.3.1
pandas==2.2.0
numpy==1.24.3
scikit-learn==1.8.0
openpyxl==3.11.0
xlsxwriter==3.2.9
reportlab==4.0.9
psycopg2-binary==2.9.9
python-decouple==3.8
```

---

## 🚢 Despliegue en Producción

### Usando Gunicorn + Nginx

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Configurar Nginx como reverse proxy
# Ver: docs/DEPLOYMENT.md
```

### Usando Docker

```bash
docker build -t healthanalytics:latest .
docker run -p 8000:8000 healthanalytics:latest
```

### Variables de Entorno (.env)

```
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://user:pass@localhost/healthanalytics
CORS_ALLOWED_ORIGINS=https://tu-dominio.com
```

---

## 📚 Documentación Adicional

- **[ARQUITECTURA.md](docs/ARQUITECTURA.md)** - Diseño del sistema
- **[API.md](docs/API.md)** - Referencia de APIs
- **[ETL.md](docs/ETL.md)** - Detalles del proceso ETL
- **[ML.md](docs/ML.md)** - Documentación de Machine Learning
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guía de despliegue

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'django'"

```bash
pip install -r requirements.txt
```

### Error: "No such table: etl_paciente"

```bash
python manage.py migrate
```

### Error: "CORS policy blocked"

Verificar `CORS_ALLOWED_ORIGINS` en `settings.py`

### Error: "Connection refused" (Base de datos)

```bash
# SQLite (desarrollo)
# Verificar que db.sqlite3 existe

# PostgreSQL (producción)
# Verificar que PostgreSQL está corriendo
sudo service postgresql status
```

---

## 📞 Soporte y Contacto

- **Email:** support@healthanalytics.com
- **Documentación:** https://docs.healthanalytics.com
- **Issues:** https://github.com/tu-usuario/healthcare-etl-platform/issues

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## ✨ Características Futuras (Roadmap)

- [ ] Integración HL7/FHIR
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Celery + Redis para tareas asincrónicas
- [ ] IA generativa para análisis médico
- [ ] Despliegue en cloud (AWS, Azure, GCP)
- [ ] Aplicación móvil (React Native)
- [ ] Integración con sistemas EHR
- [ ] Auditoría y compliance (HIPAA)

---

**Versión:** 1.0  
**Última actualización:** Mayo 21, 2024  
**Estado:** ✅ Producción

