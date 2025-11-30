# Script PowerShell para reemplazar claves en settings.py
$file = "tuchanchita/settings.py"
if (Test-Path $file) {
    $content = Get-Content $file -Raw
    
    # Asegurar que import os esté presente
    if ($content -notmatch "import os") {
        $content = $content -replace "(from pathlib import Path)", "`$1`nimport os"
    }
    
    # Reemplazar SECRET_KEY
    $content = $content -replace "SECRET_KEY = 'django-insecure-[^']*'", "SECRET_KEY = os.environ.get('SECRET_KEY', '')"
    
    # Reemplazar EMAIL_HOST_USER
    $content = $content -replace "EMAIL_HOST_USER = '[^']*'", "EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')"
    
    # Reemplazar EMAIL_HOST_PASSWORD
    $content = $content -replace "EMAIL_HOST_PASSWORD = '[^']*'", "EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')"
    
    # Reemplazar TWELVE_API_KEY
    $content = $content -replace 'TWELVE_API_KEY = "[^"]*"', 'TWELVE_API_KEY = os.environ.get("TWELVE_API_KEY", "")'
    
    # Reemplazar GEMINI_API_KEY
    $content = $content -replace "GEMINI_API_KEY = '[^']*'", "GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')"
    
    # Reemplazar GEMINI_PROJECT_ID
    $content = $content -replace "GEMINI_PROJECT_ID = '[^']*'", "GEMINI_PROJECT_ID = os.environ.get('GEMINI_PROJECT_ID', '')"
    
    Set-Content $file -Value $content -NoNewline
}

