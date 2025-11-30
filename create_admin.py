#!/usr/bin/env python
"""
Script para crear un usuario administrador de Django
Uso: python create_admin.py [username] [email] [password]
O ejecutar sin parámetros para modo interactivo
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuchanchita.settings')
django.setup()

from django.contrib.auth.models import User

def crear_admin(username=None, email=None, password=None):
    """Crea o actualiza un usuario administrador"""
    
    # Si no se proporcionan parámetros, usar valores por defecto
    if not username:
        username = "admin"
    if not email:
        email = "admin@tuchanchita.com"
    if not password:
        password = "admin123"
    
    print("=" * 50)
    print("Crear Usuario Administrador")
    print("=" * 50)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    print("=" * 50)
    
    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        print(f"El usuario '{username}' ya existe. Actualizando...")
        user = User.objects.get(username=username)
        user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("Usuario actualizado correctamente")
    else:
        # Crear nuevo usuario admin
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        print(f"Usuario administrador '{username}' creado correctamente")
    
    print(f"\nEmail: {user.email}")
    print(f"Username: {user.username}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    print("\nPuedes acceder al admin en: http://127.0.0.1:8000/admin/")
    print(f"Login con: {username} / {password}")

if __name__ == '__main__':
    try:
        # Si se pasan argumentos, usarlos; si no, usar valores por defecto
        if len(sys.argv) >= 4:
            username = sys.argv[1]
            email = sys.argv[2]
            password = sys.argv[3]
            crear_admin(username, email, password)
        elif len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
            print("Uso: python create_admin.py [username] [email] [password]")
            print("\nEjemplo:")
            print("  python create_admin.py admin admin@example.com mi_password")
            print("\nO ejecutar sin parámetros para usar valores por defecto:")
            print("  python create_admin.py")
        else:
            # Modo interactivo
            try:
                username = input("Nombre de usuario (admin): ").strip() or "admin"
                email = input("Correo electronico: ").strip() or "admin@tuchanchita.com"
                password = input("Contrasena: ").strip() or "admin123"
                crear_admin(username, email, password)
            except (EOFError, KeyboardInterrupt):
                # Si no hay entrada interactiva, usar valores por defecto
                print("\nUsando valores por defecto...")
                crear_admin()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
