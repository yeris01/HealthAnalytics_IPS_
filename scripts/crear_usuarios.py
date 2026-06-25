from authentication.models import Usuario
usuarios = [
    ('admin', 'admin123', 'administrador', 'Administrador', 'Sistema'),
    ('medico', 'medico123', 'medico', 'Médico', 'Demo'),
    ('analista', 'analista123', 'analista', 'Analista', 'Demo'),
]
for username, password, rol, first, last in usuarios:
    u, created = Usuario.objects.get_or_create(username=username, defaults={'rol': rol, 'first_name': first, 'last_name': last, 'email': f'{username}@healthanalytics.local'})
    u.rol = rol
    u.first_name = first
    u.last_name = last
    u.email = f'{username}@healthanalytics.local'
    u.set_password(password)
    u.is_staff = username == 'admin'
    u.is_superuser = username == 'admin'
    u.save()
print('Usuarios demo creados/actualizados: admin/admin123, medico/medico123, analista/analista123')
