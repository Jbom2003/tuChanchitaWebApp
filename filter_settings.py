#!/usr/bin/env python3
# Script para reemplazar claves hardcodeadas en settings.py usando git filter-branch

import re
import sys

def filter_settings(content):
    """Reemplaza claves hardcodeadas con variables de entorno"""
    
    # Asegurar que import os esté presente
    if 'import os' not in content and 'from pathlib import Path' in content:
        content = content.replace('from pathlib import Path', 'from pathlib import Path\nimport os')
    elif 'import os' not in content:
        content = 'import os\n' + content
    
    # Reemplazar SECRET_KEY
    content = re.sub(
        r"SECRET_KEY = 'django-insecure-[^']*'",
        "SECRET_KEY = os.environ.get('SECRET_KEY', '')",
        content
    )
    
    # Reemplazar EMAIL_HOST_USER
    content = re.sub(
        r"EMAIL_HOST_USER = '[^']*'",
        "EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')",
        content
    )
    
    # Reemplazar EMAIL_HOST_PASSWORD
    content = re.sub(
        r"EMAIL_HOST_PASSWORD = '[^']*'",
        "EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')",
        content
    )
    
    # Reemplazar TWELVE_API_KEY
    content = re.sub(
        r'TWELVE_API_KEY = "[^"]*"',
        'TWELVE_API_KEY = os.environ.get("TWELVE_API_KEY", "")',
        content
    )
    
    # Reemplazar GEMINI_API_KEY
    content = re.sub(
        r"GEMINI_API_KEY = '[^']*'",
        "GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')",
        content
    )
    
    # Reemplazar GEMINI_PROJECT_ID
    content = re.sub(
        r"GEMINI_PROJECT_ID = '[^']*'",
        "GEMINI_PROJECT_ID = os.environ.get('GEMINI_PROJECT_ID', '')",
        content
    )
    
    return content

if __name__ == '__main__':
    # Leer de stdin
    content = sys.stdin.read()
    # Filtrar
    filtered = filter_settings(content)
    # Escribir a stdout
    sys.stdout.write(filtered)

