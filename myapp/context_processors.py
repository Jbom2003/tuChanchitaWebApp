"""
Context processors para templates
"""
from django.contrib.auth.models import User
from .models import UserProfile

def logros_recientes(request):
    """
    Context processor para logros recientes (stub por ahora)
    """
    return {'logros_nuevos': []}

def admin_check(request):
    """
    Verifica si el usuario actual es admin de Django
    """
    is_admin = False
    if 'user_id' in request.session:
        try:
            user_profile = UserProfile.objects.get(id=request.session['user_id'])
            # Verificar si existe un usuario de Django con el mismo email y es admin
            django_user = User.objects.filter(email=user_profile.email).first()
            if django_user and (django_user.is_staff or django_user.is_superuser):
                is_admin = True
        except UserProfile.DoesNotExist:
            pass
    
    return {'is_admin': is_admin}
