# 🚀 Guía de Inicio Rápido - HealthAnalytics IPS

## Acceso Inmediato

### 🔗 URL del Servidor
```
https://8000-iiyra60sgwlyohwli6fvd-dcc26607.us3.manus.computer
```

### 🔐 Credenciales de Acceso

| Rol | Usuario | Contraseña |
|-----|---------|-----------|
| **Administrador** | `admin` | `admin123` |
| **Médico** | `medico` | `medico123` |
| **Analista** | `analista` | `analista123` |

---

## 📊 Datos Cargados

✅ **1,780 pacientes clínicos** cargados en la base de datos
- Dataset: `dataset_clinico_etl_1800_registros.xlsx`
- Registros procesados exitosamente
- Errores de carga: 22 (valores inválidos)

---

## 🎯 Funcionalidades Disponibles

### 1. Dashboard Principal
- **URL:** `/dashboard/`
- **Acceso:** Todos los roles
- **Contenido:** KPIs, gráficas, tendencias

### 2. Gestión de Pacientes
- **URL:** `/dashboard/pacientes/`
- **Acceso:** Todos los roles
- **Funciones:** Búsqueda, filtrado, detalles

### 3. Proceso ETL
- **URL:** `/etl/`
- **Acceso:** Administrador, Analista
- **Funciones:** Ejecutar ETL, cargar CSV, historial

### 4. Analítica de Datos
- **URL:** `/analytics/`
- **Acceso:** Todos los roles
- **Funciones:** Estadísticas, segmentación, críticos

### 5. Machine Learning
- **URL:** `/ml/`
- **Acceso:** Administrador, Analista
- **Funciones:** Entrenar modelos, predicciones, métricas

### 6. Reportes
- **URL:** `/reportes/`
- **Acceso:** Todos los roles
- **Funciones:** Exportar CSV, Excel, PDF

---

## 📝 Primeros Pasos

### Paso 1: Iniciar Sesión
1. Ir a `/login/`
2. Usar credenciales de prueba (ver arriba)
3. Hacer clic en "Ingresar"

### Paso 2: Explorar Dashboard
1. Ver KPIs en tiempo real
2. Revisar gráficas de distribución
3. Consultar pacientes críticos

### Paso 3: Entrenar Modelo ML
1. Ir a `/ml/`
2. Seleccionar "Random Forest"
3. Hacer clic en "Entrenar Modelo"
4. Esperar a que se complete (1-2 minutos)

### Paso 4: Aplicar Predicciones
1. Una vez entrenado el modelo
2. Hacer clic en "Predecir Todos los Pacientes"
3. Verificar actualización de riesgos

### Paso 5: Generar Reportes
1. Ir a `/reportes/`
2. Seleccionar formato (CSV, Excel, PDF)
3. Descargar archivo

---

## 🔌 APIs REST

### Autenticación
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Obtener KPIs
```bash
curl -X GET http://localhost:8000/api/dashboard/kpis/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Listar Pacientes
```bash
curl -X GET http://localhost:8000/api/pacientes/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Entrenar Modelo ML
```bash
curl -X POST http://localhost:8000/api/ml/entrenar/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tipo_modelo":"random_forest"}'
```

---

## 📊 Estadísticas del Sistema

| Métrica | Valor |
|---------|-------|
| **Total Pacientes** | 1,780 |
| **Pacientes Críticos** | ~180-200 |
| **Pacientes Hipertensos** | ~400-500 |
| **Pacientes Diabéticos** | ~300-400 |
| **Pacientes Fumadores** | ~200-300 |
| **Pacientes con Obesidad** | ~300-400 |

---

## 🛠️ Configuración Local

### Requisitos
- Python 3.12+
- pip
- Git

### Instalación
```bash
# Clonar repositorio
git clone <repo-url>
cd healthcare-etl-platform

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Crear usuarios
python manage.py shell < scripts/crear_usuarios.py

# Ejecutar servidor
python manage.py runserver
```

---

## 📚 Documentación

- **README.md** - Documentación completa
- **docs/ARQUITECTURA.md** - Diseño del sistema
- **docs/API.md** - Referencia de APIs
- **docs/ETL.md** - Proceso ETL detallado
- **docs/ML.md** - Machine Learning

---

## 🐛 Troubleshooting

### No puedo acceder al servidor
- Verificar que el servidor está corriendo
- Revisar la URL correcta
- Limpiar caché del navegador

### Error de autenticación
- Verificar credenciales
- Asegurar que el usuario existe
- Revisar los logs

### Modelos ML no se entrenan
- Verificar que hay datos en la BD
- Revisar logs en `/admin/`
- Intentar con menos datos

---

## 📞 Soporte

Para reportar problemas o sugerencias:
- Email: support@healthanalytics.com
- GitHub Issues: [Enlace al repo]

---

**Última actualización:** Mayo 21, 2024
**Versión:** 1.0
**Estado:** ✅ Listo para usar

