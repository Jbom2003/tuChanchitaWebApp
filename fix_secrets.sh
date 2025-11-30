#!/bin/bash
# Script para eliminar claves hardcodeadas de settings.py

if [ -f tuchanchita/settings.py ]; then
    # Asegurar que import os esté presente
    if ! grep -q "^import os" tuchanchita/settings.py && ! grep -q "^import os" tuchanchita/settings.py; then
        sed -i '1a import os' tuchanchita/settings.py
    fi
    
    # Reemplazar SECRET_KEY
    sed -i "s/SECRET_KEY = 'django-insecure-[^']*'/SECRET_KEY = os.environ.get('SECRET_KEY', '')/" tuchanchita/settings.py
    
    # Reemplazar EMAIL_HOST_USER
    sed -i "s/EMAIL_HOST_USER = '[^']*'/EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')/" tuchanchita/settings.py
    
    # Reemplazar EMAIL_HOST_PASSWORD
    sed -i "s/EMAIL_HOST_PASSWORD = '[^']*'/EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')/" tuchanchita/settings.py
    
    # Reemplazar TWELVE_API_KEY
    sed -i 's/TWELVE_API_KEY = "[^"]*"/TWELVE_API_KEY = os.environ.get("TWELVE_API_KEY", "")/' tuchanchita/settings.py
    
    # Reemplazar GEMINI_API_KEY
    sed -i "s/GEMINI_API_KEY = '[^']*'/GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')/" tuchanchita/settings.py
    
    # Reemplazar GEMINI_PROJECT_ID
    sed -i "s/GEMINI_PROJECT_ID = '[^']*'/GEMINI_PROJECT_ID = os.environ.get('GEMINI_PROJECT_ID', '')/" tuchanchita/settings.py
fi

