#!/bin/bash
# Script para reemplazar claves hardcodeadas en settings.py

# Asegurar que import os esté presente
if ! grep -q "^import os" "$1"; then
    sed -i '1a import os' "$1"
fi

# Reemplazar SECRET_KEY
sed -i "s/SECRET_KEY = 'django-insecure-[^']*'/SECRET_KEY = os.environ.get('SECRET_KEY', '')/" "$1"

# Reemplazar EMAIL_HOST_USER
sed -i "s/EMAIL_HOST_USER = '[^']*'/EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')/" "$1"

# Reemplazar EMAIL_HOST_PASSWORD
sed -i "s/EMAIL_HOST_PASSWORD = '[^']*'/EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')/" "$1"

# Reemplazar TWELVE_API_KEY
sed -i 's/TWELVE_API_KEY = "[^"]*"/TWELVE_API_KEY = os.environ.get("TWELVE_API_KEY", "")/' "$1"

# Reemplazar GEMINI_API_KEY
sed -i "s/GEMINI_API_KEY = '[^']*'/GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')/" "$1"

# Reemplazar GEMINI_PROJECT_ID
sed -i "s/GEMINI_PROJECT_ID = '[^']*'/GEMINI_PROJECT_ID = os.environ.get('GEMINI_PROJECT_ID', '')/" "$1"

