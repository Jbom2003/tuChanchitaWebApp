from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from myapp.models import (
    UserProfile, FinancialCompetencyAssessment, UserMetrics
)
import random


class Command(BaseCommand):
    help = 'Pobla solo fecha de registro y 2 evaluaciones para un usuario'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email del usuario a poblar')

    def handle(self, *args, **options):
        email = options['email']
        
        # Obtener usuario
        try:
            user = UserProfile.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'Usuario encontrado: {user.email}'))
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario {email} no existe. Por favor créalo primero.'))
            return
        
        # 1. Establecer fecha de registro al 28/08/2025
        metrics, _ = UserMetrics.objects.get_or_create(user=user)
        fecha_registro = timezone.make_aware(datetime(2025, 8, 28, random.randint(8, 12), random.randint(0, 59)))
        metrics.fecha_registro = fecha_registro
        metrics.fecha_ultima_actividad = timezone.now()
        self.stdout.write(self.style.SUCCESS(f'[OK] Fecha de registro establecida: 28/08/2025'))
        
        # 2. Eliminar evaluaciones existentes y crear solo 2
        FinancialCompetencyAssessment.objects.filter(user=user).delete()
        
        # Evaluación 1 - 28/08/2025 entre 15:00 y 20:00 (hora Perú = 20:00-01:00 UTC)
        hora_peru = random.randint(15, 20)  # 15:00 a 20:00 en Perú
        hora_utc = hora_peru + 5  # Sumar 5 horas para UTC
        if hora_utc >= 24:
            hora_utc -= 24
            fecha_eval1 = timezone.make_aware(datetime(2025, 8, 29, hora_utc, random.randint(0, 59)))
        else:
            fecha_eval1 = timezone.make_aware(datetime(2025, 8, 28, hora_utc, random.randint(0, 59)))
        
        # Puntaje promedio: competencias alrededor de 3/5
        eval1 = FinancialCompetencyAssessment.objects.create(
            user=user,
            numero_evaluacion=1,
            fecha_evaluacion=fecha_eval1,
            conocimiento_presupuesto=3,
            conocimiento_ahorro=3,
            conocimiento_credito=3,
            conocimiento_inversiones=2,
            conocimiento_fraudes=3,
            tiene_tarjetas_credito=True,
            cantidad_tarjetas=1,
            monto_deuda_actual=500,
            frecuencia_pago_minimo=0,
            experiencia_fraude=False,
            conocimiento_teorico=3,
            aplicacion_practica=3
        )
        self.stdout.write(self.style.SUCCESS(f'[OK] Evaluacion 1 creada (28/08/2025): {eval1.puntaje_total} puntos'))
        
        # Evaluación 2 - 28/11 o 29/11/2025 a cualquier hora, entre -5% a +10%
        # Hacer más probable que sea positiva (70% probabilidad de ser positiva)
        es_positiva = random.random() < 0.70  # 70% probabilidad de mejora positiva
        
        if es_positiva:
            # Mejora positiva: entre 2% y +10% (siempre positiva, mínimo 2%)
            variacion_objetivo = random.uniform(0.02, 0.10)
        else:
            # Mejora negativa: entre -5% y -1% (menos negativa)
            variacion_objetivo = random.uniform(-0.05, -0.01)
        puntaje_objetivo = int(eval1.puntaje_total * (1 + variacion_objetivo))
        
        max_intentos = 50
        for intento in range(max_intentos):
            # Calcular competencias basadas en la variación objetivo
            if variacion_objetivo > 0:
                # Mejora: aumentar competencias (80% probabilidad de aumentar 1 punto)
                conocimiento_presupuesto2 = min(5, eval1.conocimiento_presupuesto + random.choice([0, 1, 1, 1, 1]))
                conocimiento_ahorro2 = min(5, eval1.conocimiento_ahorro + random.choice([0, 1, 1, 1, 1]))
                conocimiento_credito2 = min(5, eval1.conocimiento_credito + random.choice([0, 1, 1, 1, 1]))
                conocimiento_inversiones2 = min(5, eval1.conocimiento_inversiones + random.choice([0, 1, 1, 1, 1]))
                conocimiento_fraudes2 = min(5, eval1.conocimiento_fraudes + random.choice([0, 1, 1, 1, 1]))
                conocimiento_teorico2 = min(5, eval1.conocimiento_teorico + random.choice([0, 1, 1, 1, 1]))
                aplicacion_practica2 = min(5, eval1.aplicacion_practica + random.choice([0, 1, 1, 1, 1]))
                monto_deuda2 = max(0, eval1.monto_deuda_actual - random.randint(150, 300))
            else:
                # Empeora: disminuir competencias muy ligeramente (85% mantener, 15% disminuir)
                conocimiento_presupuesto2 = max(1, eval1.conocimiento_presupuesto - random.choice([0, 0, 0, 0, 0, 1]))
                conocimiento_ahorro2 = max(1, eval1.conocimiento_ahorro - random.choice([0, 0, 0, 0, 0, 1]))
                conocimiento_credito2 = max(1, eval1.conocimiento_credito - random.choice([0, 0, 0, 0, 0, 1]))
                conocimiento_inversiones2 = max(1, eval1.conocimiento_inversiones - random.choice([0, 0, 0, 0, 0, 1]))
                conocimiento_fraudes2 = max(1, eval1.conocimiento_fraudes - random.choice([0, 0, 0, 0, 0, 1]))
                conocimiento_teorico2 = max(1, eval1.conocimiento_teorico - random.choice([0, 0, 0, 0, 0, 1]))
                aplicacion_practica2 = max(1, eval1.aplicacion_practica - random.choice([0, 0, 0, 0, 0, 1]))
                monto_deuda2 = eval1.monto_deuda_actual + random.randint(50, 100)
            
            # Fecha: 28/11 o 29/11 a cualquier hora
            dia = random.choice([28, 29])
            hora_utc2 = random.randint(0, 23)
            fecha_eval2 = timezone.make_aware(datetime(2025, 11, dia, hora_utc2, random.randint(0, 59)))
            
            eval2 = FinancialCompetencyAssessment.objects.create(
                user=user,
                numero_evaluacion=2,
                fecha_evaluacion=fecha_eval2,
                conocimiento_presupuesto=conocimiento_presupuesto2,
                conocimiento_ahorro=conocimiento_ahorro2,
                conocimiento_credito=conocimiento_credito2,
                conocimiento_inversiones=conocimiento_inversiones2,
                conocimiento_fraudes=conocimiento_fraudes2,
                tiene_tarjetas_credito=True,
                cantidad_tarjetas=1,
                monto_deuda_actual=monto_deuda2,
                frecuencia_pago_minimo=0,
                experiencia_fraude=False,
                conocimiento_teorico=conocimiento_teorico2,
                aplicacion_practica=aplicacion_practica2
            )
            
            variacion_real = ((eval2.puntaje_total - eval1.puntaje_total) / eval1.puntaje_total) * 100
            
            # Verificar si está en el rango correcto (-5% a +10%)
            if -5.0 <= variacion_real <= 10.0:
                break
            else:
                # Eliminar y reintentar
                eval2.delete()
                if intento == max_intentos - 1:
                    # Si no se logra después de varios intentos, usar la última
                    eval2 = FinancialCompetencyAssessment.objects.create(
                        user=user,
                        numero_evaluacion=2,
                        fecha_evaluacion=fecha_eval2,
                        conocimiento_presupuesto=conocimiento_presupuesto2,
                        conocimiento_ahorro=conocimiento_ahorro2,
                        conocimiento_credito=conocimiento_credito2,
                        conocimiento_inversiones=conocimiento_inversiones2,
                        conocimiento_fraudes=conocimiento_fraudes2,
                        tiene_tarjetas_credito=True,
                        cantidad_tarjetas=1,
                        monto_deuda_actual=monto_deuda2,
                        frecuencia_pago_minimo=0,
                        experiencia_fraude=False,
                        conocimiento_teorico=conocimiento_teorico2,
                        aplicacion_practica=aplicacion_practica2
                    )
                    variacion_real = ((eval2.puntaje_total - eval1.puntaje_total) / eval1.puntaje_total) * 100
        
        self.stdout.write(self.style.SUCCESS(f'[OK] Evaluacion 2 creada ({dia}/11/2025): {eval2.puntaje_total} puntos ({variacion_real:+.1f}%)'))
        
        # Actualizar métricas
        metrics.actualizar_mejora()
        # Establecer días activos y sesiones específicas
        metrics.dias_activos = 2
        metrics.sesiones_totales = random.randint(2, 4)
        metrics.save()
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Usuario configurado exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'   Email: {user.email}'))
        self.stdout.write(self.style.SUCCESS(f'   Fecha registro: {metrics.fecha_registro.strftime("%d/%m/%Y")}'))
        self.stdout.write(self.style.SUCCESS(f'   Días activos: {metrics.dias_activos}'))
        self.stdout.write(self.style.SUCCESS(f'   Sesiones totales: {metrics.sesiones_totales}'))
        self.stdout.write(self.style.SUCCESS(f'   Evaluaciones: {FinancialCompetencyAssessment.objects.filter(user=user).count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Mejora porcentual: {metrics.mejora_porcentual:.1f}%'))

