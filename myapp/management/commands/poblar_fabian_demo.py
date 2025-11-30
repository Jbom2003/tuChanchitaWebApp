from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from myapp.models import (
    UserProfile, PaymentMethod, Expense, PuntajeTrivia, PuntajeCompletarFrases,
    FinancialCompetencyAssessment, UserMetrics, Achievement, UserAchievement,
    Storyline, StoryProgress, UserChallenge, Challenge
)
import random


class Command(BaseCommand):
    help = 'Pobla la cuenta de fabiansilver7@gmail.com con datos de actividad realistas'

    def handle(self, *args, **options):
        email = 'fabiansilver7@gmail.com'
        
        # Obtener o crear usuario
        try:
            user = UserProfile.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'Usuario encontrado: {user.email}'))
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario {email} no existe. Por favor créalo primero.'))
            return
        
        # 1. Agregar tarjeta de pago
        if not PaymentMethod.objects.filter(user=user).exists():
            PaymentMethod.objects.create(
                user=user,
                tipo=1,  # Crédito
                sistema_de_pago=2,  # Mastercard
                banco='Interbank',
                ultimos_4_digitos='5678',
                mes_vencimiento=6,
                anio_vencimiento=2027
            )
            self.stdout.write(self.style.SUCCESS('[OK] Tarjeta de pago agregada'))
        else:
            self.stdout.write(self.style.WARNING('Tarjeta ya existe'))
        
        # 2. Agregar gastos variados (más gastos que Ana Lucía)
        gastos_existentes = Expense.objects.filter(user=user).count()
        if gastos_existentes < 30:
            categorias = ['Comida', 'Transporte', 'Entretenimiento', 'Salud', 'Tecnología', 'Ropa', 'Educación', 'Otros']
            tiendas = ['Metro', 'Tottus', 'Saga Falabella', 'Ripley', 'Movistar', 'Claro', 'Cinemark', 'McDonald\'s', 'KFC', 'Starbucks']
            
            # Gastos desde 28 de agosto 2025 hasta 28 de noviembre 2025
            fecha_inicio = timezone.make_aware(datetime(2025, 8, 28))
            fecha_fin = timezone.make_aware(datetime(2025, 11, 28))
            
            # Montos redondos comunes (máximo 300 soles para jóvenes de 18-25 años)
            montos_redondos = [15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 180, 200, 250, 300]
            
            for i in range(30 - gastos_existentes):
                dias_diferencia = (fecha_fin - fecha_inicio).days
                fecha_base = fecha_inicio + timedelta(days=random.randint(0, dias_diferencia))
                
                # Añadir hora aleatoria (considerando GMT-5 de Perú)
                # Si queremos que sea entre 8am-10pm en Perú, en UTC sería 1pm-3am del día siguiente
                # Para simplificar, usaremos horas entre 13:00 y 05:00 (del día siguiente)
                hora_peru = random.randint(8, 22)  # 8am a 10pm en Perú
                hora_utc = hora_peru + 5  # Sumar 5 horas para UTC
                if hora_utc >= 24:
                    hora_utc -= 24
                    fecha = fecha_base + timedelta(days=1)
                    fecha = fecha.replace(hour=hora_utc, minute=random.randint(0, 59), second=0, microsecond=0)
                else:
                    fecha = fecha_base.replace(hour=hora_utc, minute=random.randint(0, 59), second=0, microsecond=0)
                
                Expense.objects.create(
                    user=user,
                    amount=random.choice(montos_redondos),
                    category=random.choice(categorias),
                    store_name=random.choice(tiendas),
                    date=fecha
                )
            self.stdout.write(self.style.SUCCESS(f'[OK] {30 - gastos_existentes} gastos agregados'))
        else:
            self.stdout.write(self.style.WARNING(f'Ya existen {gastos_existentes} gastos'))
        
        # 3. Configurar puntajes de juegos (mejor desempeño en trivia, peor en completar frases)
        # Trivia Financiera - Usuario muy bueno
        puntaje_trivia, _ = PuntajeTrivia.objects.get_or_create(user=user)
        puntaje_trivia.puntaje_total = 520  # Muy alto
        puntaje_trivia.intentos = 8
        puntaje_trivia.save()
        user.trivia_puntaje = 520
        user.save()
        self.stdout.write(self.style.SUCCESS('[OK] Puntaje de Trivia configurado: 520 puntos'))
        
        # Completar Frases - Usuario promedio
        puntaje_completar, _ = PuntajeCompletarFrases.objects.get_or_create(user=user)
        puntaje_completar.puntaje_total = 95  # Más bajo que Ana Lucía
        puntaje_completar.frases_completadas = 25
        puntaje_completar.respuestas_correctas = 15
        puntaje_completar.respuestas_parciales = 7
        puntaje_completar.respuestas_incorrectas = 3
        puntaje_completar.save()
        self.stdout.write(self.style.SUCCESS('[OK] Puntaje de Completar Frases configurado: 95 puntos'))
        
        # 4. Eliminar evaluaciones existentes y crear solo 2
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
            cantidad_tarjetas=2,
            monto_deuda_actual=800,
            frecuencia_pago_minimo=1,  # A veces paga mínimo
            experiencia_fraude=False,
            conocimiento_teorico=3,
            aplicacion_practica=2
        )
        self.stdout.write(self.style.SUCCESS(f'[OK] Evaluacion 1 creada (28/08/2025): {eval1.puntaje_total} puntos'))
        
        # Evaluación 2 - 28/11 o 29/11/2025 a cualquier hora, 15-70% mejor
        mejora_porcentual = random.uniform(0.15, 0.70)  # 15% a 70% de mejora
        
        # Mejorar competencias (aumentar 1-2 puntos en cada una)
        conocimiento_presupuesto2 = min(5, eval1.conocimiento_presupuesto + random.randint(1, 2))
        conocimiento_ahorro2 = min(5, eval1.conocimiento_ahorro + random.randint(1, 2))
        conocimiento_credito2 = min(5, eval1.conocimiento_credito + random.randint(1, 2))
        conocimiento_inversiones2 = min(5, eval1.conocimiento_inversiones + random.randint(1, 2))
        conocimiento_fraudes2 = min(5, eval1.conocimiento_fraudes + random.randint(1, 2))
        
        # Mejorar brecha teórico-práctica
        conocimiento_teorico2 = min(5, eval1.conocimiento_teorico + random.randint(1, 2))
        aplicacion_practica2 = min(5, eval1.aplicacion_practica + random.randint(1, 2))
        
        # Reducir deuda y mejorar comportamiento
        monto_deuda2 = max(0, eval1.monto_deuda_actual - random.randint(300, 500))
        
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
            cantidad_tarjetas=1,  # Redujo tarjetas
            monto_deuda_actual=monto_deuda2,
            frecuencia_pago_minimo=0,  # Ya no paga mínimo
            experiencia_fraude=False,
            conocimiento_teorico=conocimiento_teorico2,
            aplicacion_practica=aplicacion_practica2
        )
        mejora_real = ((eval2.puntaje_total - eval1.puntaje_total) / eval1.puntaje_total) * 100
        self.stdout.write(self.style.SUCCESS(f'[OK] Evaluacion 2 creada ({dia}/11/2025): {eval2.puntaje_total} puntos ({mejora_real:.1f}% mejor)'))
        
        # Actualizar métricas
        metrics, _ = UserMetrics.objects.get_or_create(user=user)
        
        # Establecer fecha de registro al 28/08/2025 (antes de la primera evaluación)
        fecha_registro = timezone.make_aware(datetime(2025, 8, 28, random.randint(8, 12), random.randint(0, 59)))
        metrics.fecha_registro = fecha_registro
        metrics.fecha_ultima_actividad = timezone.now()  # Última actividad es ahora
        
        metrics.actualizar_mejora()  # Esto calculará desde las evaluaciones reales
        # Sesiones totales
        metrics.sesiones_totales = 38
        # Días activos: entre 10% y 40% de las sesiones totales
        porcentaje_dias = random.uniform(0.10, 0.40)
        metrics.dias_activos = max(1, int(metrics.sesiones_totales * porcentaje_dias))
        metrics.tiempo_total_uso = 18.5  # horas
        metrics.retos_completados = 3
        metrics.trivias_completadas = 12
        metrics.puntos_totales = user.points + 520 + 95
        metrics.save()
        self.stdout.write(self.style.SUCCESS('[OK] Metricas actualizadas (fecha registro: 28/08/2025)'))
        
        # 5. Desbloquear algunos logros (no todos, para ser más realista)
        logros = Achievement.objects.filter(is_active=True)
        logros_desbloqueados = 0
        
        # Desbloquear aproximadamente el 60% de los logros
        logros_a_desbloquear = random.sample(list(logros), min(len(logros), int(len(logros) * 0.6)))
        
        for logro in logros_a_desbloquear:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=logro,
                defaults={
                    'progreso': 100.0,
                    'fecha_desbloqueo': timezone.now() - timedelta(days=random.randint(1, 75))
                }
            )
            if created:
                logros_desbloqueados += 1
                # Agregar puntos bonus si tiene
                if logro.puntos_bonus > 0:
                    user.points += logro.puntos_bonus
        
        user.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] {logros_desbloqueados} logros desbloqueados'))
        
        # 6. Completar algunas narrativas (no todas)
        narrativas = Storyline.objects.all()
        narrativas_completadas = 0
        
        # Completar aproximadamente el 70% de las narrativas
        narrativas_a_completar = random.sample(list(narrativas), min(len(narrativas), int(len(narrativas) * 0.7)))
        
        for narrativa in narrativas_a_completar:
            progress, created = StoryProgress.objects.get_or_create(
                user=user,
                storyline=narrativa,
                defaults={
                    'desbloqueado': True,
                    'completado': True,
                    'fecha_completado': timezone.now() - timedelta(days=random.randint(1, 60))
                }
            )
            if not created:
                progress.desbloqueado = True
                progress.completado = True
                if not progress.fecha_completado:
                    progress.fecha_completado = timezone.now() - timedelta(days=random.randint(1, 60))
                progress.save()
            
            if created or not progress.completado:
                narrativas_completadas += 1
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {narrativas_completadas} narrativas completadas'))
        
        # 7. Completar algunos retos (menos que Ana Lucía)
        retos_disponibles = list(Challenge.objects.filter(is_active=True))
        retos_a_completar = random.sample(retos_disponibles, min(len(retos_disponibles), 3))
        retos_completados = 0
        
        for reto in retos_a_completar:
            user_challenge, created = UserChallenge.objects.get_or_create(
                user=user,
                challenge=reto,
                defaults={
                    'start_date': timezone.now() - timedelta(days=random.randint(15, 60)),
                    'completed': True,
                    'failed': False,
                    'earned_points': reto.points
                }
            )
            if created:
                retos_completados += 1
                user.points += reto.points
        
        user.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] {retos_completados} retos completados'))
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Usuario poblado exitosamente con todos los datos!'))
        self.stdout.write(self.style.SUCCESS(f'   Email: {user.email}'))
        self.stdout.write(self.style.SUCCESS(f'   Puntos totales: {user.points}'))
        self.stdout.write(self.style.SUCCESS(f'   Evaluaciones: {FinancialCompetencyAssessment.objects.filter(user=user).count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Logros: {UserAchievement.objects.filter(user=user).count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Narrativas: {StoryProgress.objects.filter(user=user, completado=True).count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Mejora porcentual: {metrics.mejora_porcentual:.1f}%'))

