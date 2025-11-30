"""
Comando de management para generar recomendaciones personalizadas con IA
Permite forzar la generación de recomendaciones para todos los usuarios o para un usuario específico
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import UserProfile, PersonalizedRecommendation
from myapp.views import generar_recomendaciones_personalizadas


class Command(BaseCommand):
    help = 'Genera recomendaciones personalizadas con IA para usuarios. Puede ser para todos los usuarios o para uno específico.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuario',
            type=str,
            help='Email del usuario específico para generar recomendaciones. Si no se especifica, genera para todos los usuarios activos.',
        )
        parser.add_argument(
            '--forzar',
            action='store_true',
            help='Fuerza la generación incluso si hay recomendaciones recientes (menos de 7 días).',
        )
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina recomendaciones antiguas antes de generar nuevas.',
        )

    def handle(self, *args, **options):
        usuario_email = options.get('usuario')
        forzar = options.get('forzar', False)
        limpiar = options.get('limpiar', False)
        
        if usuario_email:
            # Generar para un usuario específico
            try:
                user = UserProfile.objects.get(email=usuario_email)
                self.stdout.write(self.style.SUCCESS(f'Generando recomendaciones para: {user.email}'))
                
                if limpiar:
                    count = PersonalizedRecommendation.objects.filter(user=user).count()
                    PersonalizedRecommendation.objects.filter(user=user).delete()
                    self.stdout.write(self.style.WARNING(f'  [-] Eliminadas {count} recomendaciones antiguas'))
                
                # Verificar si hay recomendaciones recientes
                ultima_recomendacion = PersonalizedRecommendation.objects.filter(user=user).order_by('-fecha_recomendacion').first()
                if ultima_recomendacion and not forzar:
                    dias_desde_ultima = (timezone.now() - ultima_recomendacion.fecha_recomendacion).days
                    if dias_desde_ultima < 7:
                        self.stdout.write(self.style.WARNING(
                            f'  [-] Ya hay recomendaciones recientes (hace {dias_desde_ultima} días). '
                            f'Usa --forzar para generar de todas formas.'
                        ))
                        return
                
                recomendaciones = generar_recomendaciones_personalizadas(user)
                if recomendaciones:
                    self.stdout.write(self.style.SUCCESS(f'  [OK] Generadas {len(recomendaciones)} recomendaciones'))
                    for rec in recomendaciones:
                        self.stdout.write(f'    - {rec.tipo_recomendacion}: {rec.contenido[:50]}...')
                else:
                    self.stdout.write(self.style.ERROR('  [ERROR] No se pudieron generar recomendaciones'))
                    
            except UserProfile.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuario no encontrado: {usuario_email}'))
                return
        else:
            # Generar para todos los usuarios activos
            usuarios = UserProfile.objects.filter(is_active=True)
            total_usuarios = usuarios.count()
            self.stdout.write(self.style.SUCCESS(f'Generando recomendaciones para {total_usuarios} usuarios...'))
            
            exitosos = 0
            fallidos = 0
            omitidos = 0
            
            for user in usuarios:
                try:
                    if limpiar:
                        PersonalizedRecommendation.objects.filter(user=user).delete()
                    
                    # Verificar si hay recomendaciones recientes
                    ultima_recomendacion = PersonalizedRecommendation.objects.filter(user=user).order_by('-fecha_recomendacion').first()
                    if ultima_recomendacion and not forzar:
                        dias_desde_ultima = (timezone.now() - ultima_recomendacion.fecha_recomendacion).days
                        if dias_desde_ultima < 7:
                            omitidos += 1
                            continue
                    
                    recomendaciones = generar_recomendaciones_personalizadas(user)
                    if recomendaciones:
                        exitosos += 1
                        self.stdout.write(self.style.SUCCESS(f'  [OK] {user.email}: {len(recomendaciones)} recomendaciones'))
                    else:
                        fallidos += 1
                        self.stdout.write(self.style.WARNING(f'  [-] {user.email}: No se pudieron generar'))
                        
                except Exception as e:
                    fallidos += 1
                    self.stdout.write(self.style.ERROR(f'  [ERROR] {user.email}: {str(e)}'))
            
            # Resumen
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS('Resumen:'))
            self.stdout.write(self.style.SUCCESS(f'  Exitosos: {exitosos}'))
            if omitidos > 0:
                self.stdout.write(self.style.WARNING(f'  Omitidos (recientes): {omitidos}'))
            if fallidos > 0:
                self.stdout.write(self.style.ERROR(f'  Fallidos: {fallidos}'))
            self.stdout.write(self.style.SUCCESS('='*50))

