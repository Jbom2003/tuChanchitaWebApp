from functools import wraps
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from myapp.models import UserMetrics, UserProfile

def session_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')  # Asegúrate que exista una URL llamada 'login'
        
        # Actualizar métricas de actividad del usuario
        try:
            user = UserProfile.objects.get(id=request.session['user_id'])
            metrics, _ = UserMetrics.objects.get_or_create(user=user)
            
            ahora = timezone.now()
            
            # Contar sesiones: nueva sesión si pasaron más de 30 minutos desde última actividad
            # o si es la primera vez que accede en esta sesión HTTP
            ultima_actividad = metrics.fecha_ultima_actividad
            tiempo_inactividad = timedelta(minutes=30)  # 30 minutos de inactividad = nueva sesión
            
            if ultima_actividad is None:
                # Primera vez que accede
                metrics.sesiones_totales += 1
            elif (ahora - ultima_actividad) > tiempo_inactividad:
                # Pasaron más de 30 minutos sin actividad = nueva sesión
                metrics.sesiones_totales += 1
            
            # Actualizar días activos (si es un día nuevo desde la última actividad)
            fecha_ultima = ultima_actividad.date() if ultima_actividad else None
            fecha_hoy = ahora.date()
            
            if fecha_ultima is None:
                # Primera vez, establecer a 1
                metrics.dias_activos = 1
            elif fecha_ultima < fecha_hoy:
                # Es un día nuevo, incrementar días activos
                # Solo incrementa 1 día, no importa cuántos días hayan pasado
                # (para evitar saltos grandes si el usuario no usa la app por mucho tiempo)
                metrics.dias_activos += 1
            
            # Actualizar fecha de última actividad (se actualiza en cada acceso)
            metrics.fecha_ultima_actividad = ahora
            metrics.save()
        except Exception as e:
            # Si hay error, continuar sin actualizar métricas
            pass
        
        # Limpiar logros de la sesion si se solicita
        if request.GET.get('clear_achievements') == '1':
            if 'logros_desbloqueados_recientes' in request.session:
                del request.session['logros_desbloqueados_recientes']
                request.session.modified = True
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view