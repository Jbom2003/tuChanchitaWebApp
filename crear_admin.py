"""
Script para crear un superusuario admin de Django
Ejecutar: python crear_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuchanchita.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Crear superusuario
username = input("Nombre de usuario admin: ")
email = input("Email del admin: ")
password = input("Contraseña: ")

try:
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superusuario '{username}' creado exitosamente!")
    print(f"   Email: {email}")
    print(f"   Puedes acceder al admin en: http://127.0.0.1:8000/admin/")
except Exception as e:
    print(f"❌ Error al crear superusuario: {e}")


