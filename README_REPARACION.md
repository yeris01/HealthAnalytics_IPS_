# HealthAnalytics IPS reparado

Este proyecto fue reconstruido para funcionar como aplicación Django completa. Se añadieron `manage.py`, el paquete `config`, las apps `authentication`, `etl`, `dashboard`, `analytics`, `ml` y `reports`, modelos, vistas, serializadores, rutas, plantillas auxiliares y dependencias compatibles.

## Ejecución

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py shell < scripts/crear_usuarios.py
python manage.py runserver 0.0.0.0:8000
```

Credenciales demo: `admin/admin123`, `medico/medico123`, `analista/analista123`.

## Carga inicial de datos

Después de iniciar sesión, ejecute el ETL con:

```bash
curl -X POST http://localhost:8000/etl/api/etl/ejecutar/ -H "Authorization: Bearer <token>"
```

También puede usar sesión web autenticada y llamar el endpoint desde el navegador/herramientas API.
