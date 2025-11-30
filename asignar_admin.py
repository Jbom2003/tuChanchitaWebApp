"""
Script para asignar permisos de admin a un usuario existente
Ejecutar: python asignar_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuchanchita.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 50)
print("ASIGNAR PERMISOS DE ADMIN A UN USUARIO")
print("=" * 50)
print()

# Listar usuarios existentes
usuarios = User.objects.all()
if usuarios.exists():
    print("Usuarios existentes:")
    for u in usuarios:
        print(f"  - {u.username} ({u.email}) - {'ADMIN' if u.is_superuser else 'Usuario normal'}")
    print()

username = input("Ingresa el nombre de usuario (username) a convertir en admin: ")

try:
    user = User.objects.get(username=username)
    
    # Asignar permisos de admin
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    
    print()
    print(f"✅ Usuario '{username}' ahora es ADMINISTRADOR!")
    print(f"   - Puede acceder al panel de admin en: http://127.0.0.1:8000/admin/")
    print(f"   - Email: {user.email}")
    print(f"   - Staff: {user.is_staff}")
    print(f"   - Superusuario: {user.is_superuser}")
    
except User.DoesNotExist:
    print(f"❌ Error: No existe un usuario con el username '{username}'")
    print()
    print("Opciones:")
    print("1. Crear un nuevo superusuario: python manage.py createsuperuser")
    print("2. Ver usuarios existentes y crear uno nuevo")
    
    crear = input("¿Deseas crear un nuevo usuario admin? (s/n): ")
    if crear.lower() == 's':
        email = input("Email: ")
        password = input("Contraseña: ")
        try:
            new_user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Superusuario '{username}' creado exitosamente!")
        except Exception as e:
            print(f"❌ Error: {e}")


