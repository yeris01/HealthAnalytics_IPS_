@echo off
echo ========================================
echo   HealthAnalytics IPS - Iniciando...
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instala Python 3.10+
    pause
    exit
)

:: Instalar dependencias si faltan
echo [1/3] Instalando dependencias...
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers whitenoise pandas numpy scikit-learn openpyxl reportlab -q

:: Correr migraciones
echo [2/3] Verificando base de datos...
python manage.py migrate --run-syncdb -v 0

:: Crear usuarios si no existen
echo [3/3] Verificando usuarios...
python manage.py shell -c "
from authentication.models import Usuario
if not Usuario.objects.filter(username='admin').exists():
    u = Usuario.objects.create_superuser('admin', '', 'admin123')
    u.rol = 'administrador'; u.save()
    print('Usuario admin creado')
if not Usuario.objects.filter(username='medico').exists():
    u = Usuario.objects.create_user('medico', '', 'medico123')
    u.rol = 'medico'; u.save()
    print('Usuario medico creado')
if not Usuario.objects.filter(username='analista').exists():
    u = Usuario.objects.create_user('analista', '', 'analista123')
    u.rol = 'analista'; u.save()
    print('Usuario analista creado')
print('Usuarios listos.')
" 2>nul

echo.
echo ========================================
echo   Servidor listo en:
echo   http://127.0.0.1:8000
echo.
echo   Credenciales:
echo   admin / admin123
echo   medico / medico123
echo   analista / analista123
echo ========================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver
pause
