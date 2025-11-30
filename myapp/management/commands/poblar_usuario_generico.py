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
    help = 'Pobla la cuenta de un usuario con datos de actividad realistas'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email del usuario a poblar')

    def handle(self, *args, **options):
        email = options['email']
        
        # Obtener o crear usuario
        try:
            user = UserProfile.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'Usuario encontrado: {user.email}'))
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario {email} no existe. Por favor créalo primero.'))
            return
        
        # 1. Agregar tarjeta de pago
        if not PaymentMethod.objects.filter(user=user).exists():
            tipos_pago = [1, 2]  # Crédito, Débito
            sistemas = [1, 2]  # Visa, Mastercard
            bancos = ['BCP', 'Interbank', 'BBVA', 'Scotiabank', 'Banco de la Nación']
            PaymentMethod.objects.create(
                user=user,
                tipo=random.choice(tipos_pago),
                sistema_de_pago=random.choice(sistemas),
                banco=random.choice(bancos),
                ultimos_4_digitos=str(random.randint(1000, 9999)),
                mes_vencimiento=random.randint(1, 12),
                anio_vencimiento=random.randint(2026, 2028)
            )
            self.stdout.write(self.style.SUCCESS('[OK] Tarjeta de pago agregada'))
        else:
            self.stdout.write(self.style.WARNING('Tarjeta ya existe'))
        
        # 2. Agregar gastos variados
        gastos_existentes = Expense.objects.filter(user=user).count()
        num_gastos = random.randint(15, 30)  # Entre 15 y 30 gastos
        if gastos_existentes < num_gastos:
            categorias = ['Comida', 'Transporte', 'Entretenimiento', 'Salud', 'Tecnología', 'Ropa', 'Educación', 'Otros']
            tiendas = ['Metro', 'Tottus', 'Saga Falabella', 'Ripley', 'Movistar', 'Claro', 'Cinemark', 'McDonald\'s', 'KFC', 'Starbucks', 'Plaza Norte', 'Wong', 'Falabella', 'Supermercado', 'Restaurante', 'Cine']
            
            # Gastos desde 28 de agosto 2025 hasta 28 de noviembre 2025
            fecha_inicio = timezone.make_aware(datetime(2025, 8, 28))
            fecha_fin = timezone.make_aware(datetime(2025, 11, 28))
            
            # Montos redondos comunes (máximo 300 soles para jóvenes de 18-25 años)
            montos_redondos = [15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 180, 200, 250, 300]
            
            for i in range(num_gastos - gastos_existentes):
                dias_diferencia = (fecha_fin - fecha_inicio).days
                fecha_base = fecha_inicio + timedelta(days=random.randint(0, dias_diferencia))
                
                # Añadir hora aleatoria (considerando GMT-5 de Perú)
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
            self.stdout.write(self.style.SUCCESS(f'[OK] {num_gastos - gastos_existentes} gastos agregados'))
        else:
            self.stdout.write(self.style.WARNING(f'Ya existen {gastos_existentes} gastos'))
        
        # 3. Configurar puntajes de juegos
        # Trivia Financiera
        puntaje_trivia, _ = PuntajeTrivia.objects.get_or_create(user=user)
        puntaje_trivia.puntaje_total = random.randint(100, 600)
        puntaje_trivia.intentos = random.randint(3, 10)
        puntaje_trivia.save()
        user.trivia_puntaje = puntaje_trivia.puntaje_total
        user.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] Puntaje de Trivia configurado: {puntaje_trivia.puntaje_total} puntos'))
        
        # Completar Frases
        puntaje_completar, _ = PuntajeCompletarFrases.objects.get_or_create(user=user)
        puntaje_completar.puntaje_total = random.randint(50, 200)
        puntaje_completar.frases_completadas = random.randint(15, 50)
        puntaje_completar.respuestas_correctas = random.randint(10, puntaje_completar.frases_completadas)
        puntaje_completar.respuestas_parciales = random.randint(0, puntaje_completar.frases_completadas - puntaje_completar.respuestas_correctas)
        puntaje_completar.respuestas_incorrectas = puntaje_completar.frases_completadas - puntaje_completar.respuestas_correctas - puntaje_completar.respuestas_parciales
        puntaje_completar.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] Puntaje de Completar Frases configurado: {puntaje_completar.puntaje_total} puntos'))
        
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
            cantidad_tarjetas=random.randint(1, 2),
            monto_deuda_actual=random.randint(300, 1000),
            frecuencia_pago_minimo=random.choice([0, 0, 0, 1]),  # Mayormente no paga mínimo
            experiencia_fraude=False,
            conocimiento_teorico=3,
            aplicacion_practica=random.randint(2, 3)
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
        monto_deuda2 = max(0, eval1.monto_deuda_actual - random.randint(200, 500))
        
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
        metrics.sesiones_totales = random.randint(20, 50)
        # Días activos: entre 10% y 40% de las sesiones totales
        porcentaje_dias = random.uniform(0.10, 0.40)
        metrics.dias_activos = max(1, int(metrics.sesiones_totales * porcentaje_dias))
        metrics.tiempo_total_uso = random.uniform(10.0, 30.0)  # horas
        metrics.retos_completados = random.randint(2, 6)
        metrics.trivias_completadas = random.randint(5, 15)
        metrics.puntos_totales = user.points + puntaje_trivia.puntaje_total + puntaje_completar.puntaje_total
        metrics.save()
        self.stdout.write(self.style.SUCCESS('[OK] Metricas actualizadas (fecha registro: 28/08/2025)'))
        
        # 5. Desbloquear algunos logros (aleatorio entre 30% y 80%)
        logros = Achievement.objects.filter(is_active=True)
        porcentaje_logros = random.uniform(0.30, 0.80)
        logros_a_desbloquear = random.sample(list(logros), min(len(logros), int(len(logros) * porcentaje_logros)))
        logros_desbloqueados = 0
        
        for logro in logros_a_desbloquear:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=logro,
                defaults={
                    'progreso': 100.0,
                    'fecha_desbloqueo': timezone.now() - timedelta(days=random.randint(1, 90))
                }
            )
            if created:
                logros_desbloqueados += 1
                if logro.puntos_bonus > 0:
                    user.points += logro.puntos_bonus
        
        user.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] {logros_desbloqueados} logros desbloqueados'))
        
        # 6. Completar algunas narrativas (aleatorio entre 50% y 90%)
        narrativas = Storyline.objects.all()
        porcentaje_narrativas = random.uniform(0.50, 0.90)
        narrativas_a_completar = random.sample(list(narrativas), min(len(narrativas), int(len(narrativas) * porcentaje_narrativas)))
        narrativas_completadas = 0
        
        for narrativa in narrativas_a_completar:
            progress, created = StoryProgress.objects.get_or_create(
                user=user,
                storyline=narrativa,
                defaults={
                    'desbloqueado': True,
                    'completado': True,
                    'fecha_completado': timezone.now() - timedelta(days=random.randint(1, 90))
                }
            )
            if not created:
                progress.desbloqueado = True
                progress.completado = True
                if not progress.fecha_completado:
                    progress.fecha_completado = timezone.now() - timedelta(days=random.randint(1, 90))
                progress.save()
            
            if created or not progress.completado:
                narrativas_completadas += 1
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {narrativas_completadas} narrativas completadas'))
        
        # 7. Completar algunos retos
        retos_disponibles = list(Challenge.objects.filter(is_active=True))
        num_retos = random.randint(2, 5)
        retos_a_completar = random.sample(retos_disponibles, min(len(retos_disponibles), num_retos))
        retos_completados = 0
        
        for reto in retos_a_completar:
            user_challenge, created = UserChallenge.objects.get_or_create(
                user=user,
                challenge=reto,
                defaults={
                    'start_date': timezone.now() - timedelta(days=random.randint(15, 90)),
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

