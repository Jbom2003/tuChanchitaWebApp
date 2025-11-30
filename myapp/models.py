from django.db import models
import requests
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Sum
from django.utils import timezone
from datetime import date
from django.utils.timezone import now
from datetime import timedelta


class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    monthly_limit = models.FloatField(default=0.0)
    points = models.IntegerField(default=0)
    trivia_puntaje = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    login_attempts = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class PaymentMethod(models.Model):
    TIPO_CHOICES = [
        (1, 'Crédito'),
        (2, 'Débito'),
    ]

    TIPO_SISTEMAPAGO = [
        (1, 'Visa'),
        (2, 'Mastercard',)
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tipo = models.IntegerField(choices=TIPO_CHOICES, default=1)
    sistema_de_pago = models.IntegerField(choices=TIPO_SISTEMAPAGO, default=1)
    banco = models.CharField(max_length=100)
    ultimos_4_digitos = models.CharField(max_length=4)
    mes_vencimiento = models.IntegerField()
    anio_vencimiento = models.IntegerField()

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.banco} ****{self.ultimos_4_digitos}"



class Expense(models.Model):
    CATEGORIAS = [
        ('Comida', 'Comida'),
        ('Educación', 'Educación'),
        ('Ropa', 'Ropa'),
        ('Otros', 'Otros'),
        ('Ahorro', 'Ahorro')
    ]

    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORIAS)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)  # actualizado a DateTimeField
    store_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category} - S/.{self.amount} en {self.store_name}"


class RecommendationVideo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    url_video = models.URLField()  # enlace de YouTube u otro
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Investment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    shares = models.FloatField()
    price_at_purchase = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def total_invested(self):
        return round(self.shares * self.price_at_purchase, 2)

    def get_current_price(self):
        url = f"https://api.twelvedata.com/price?symbol={self.symbol}&apikey={settings.TWELVE_API_KEY}"
        response = requests.get(url).json()
        return float(response['price']) if 'price' in response else None

    def current_value(self):
        current_price = self.get_current_price()
        if current_price:
            return round(self.shares * current_price, 2)
        return None

    def profit_loss(self):
        current = self.current_value()
        if current:
            return round(current - self.total_invested(), 2)
        return None

    def __str__(self):
        return f"{self.company} - {self.shares} acciones"



class Challenge(models.Model):
    CHALLENGE_TYPES = [
    ('no_gastos', 'No gastar'),
    ('ahorro', 'Ahorro'),
    ]
    goal_amount = models.FloatField(null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=CHALLENGE_TYPES, default='no_gastar')
    points = models.IntegerField()
    duration_days = models.IntegerField()
    condition = models.CharField(max_length=200)  # lógica de validación (luego se puede extender)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class UserChallenge(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    earned_points = models.IntegerField(default=0)

    def check_status(self):
        if self.completed:
            return

        deadline = self.start_date + timedelta(days=self.challenge.duration_days)

        if timezone.now() > deadline:
            return  # Ya expiró

        gastos = Expense.objects.filter(user=self.user, date__range=[self.start_date, deadline])

        if self.challenge.type == 'ahorro':
            total_ahorro = sum(g.amount for g in gastos if g.category.lower() == 'ahorro')
            self.progress = total_ahorro
            if self.challenge.goal_amount and total_ahorro >= self.challenge.goal_amount:
                self.completed = True
                self.earned_points = self.challenge.points
                self.user.points += self.challenge.points
                self.user.save()
                self.save()



class TriviaQuestion(models.Model):
    pregunta = models.TextField()
    puntos = models.IntegerField(default=10)

    def __str__(self):
        return self.pregunta

class TriviaOption(models.Model):
    pregunta = models.ForeignKey(TriviaQuestion, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class TriviaRespuestaUsuario(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(TriviaQuestion, on_delete=models.CASCADE)
    respondida_correctamente = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)


class PreguntaTrivia(models.Model):
    pregunta = models.CharField(max_length=255)
    opciones = models.JSONField()  # ej. {"a": "Opción A", "b": "Opción B", "c": "Opción C"}
    respuesta_correcta = models.CharField(max_length=1)  # "a", "b", "c", etc.

    def __str__(self):
        return self.pregunta

class PuntajeTrivia(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    puntaje_total = models.IntegerField(default=0)
    intentos = models.IntegerField(default=0)  # intentos fallidos actuales
    ultima_actualizacion = models.DateTimeField(auto_now=True)


class FraseCompletar(models.Model):
    """Frases de economía para completar con IA"""
    frase_completa = models.TextField(help_text="Frase completa con la palabra clave")
    palabra_clave = models.CharField(max_length=200, help_text="Palabra o frase que se oculta")
    categoria = models.CharField(max_length=100, default='general', help_text="Categoría de la frase")
    nivel_dificultad = models.IntegerField(default=1, help_text="1=fácil, 2=medio, 3=difícil")
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.frase_completa[:50]}... ({self.categoria})"
    
    def obtener_frase_con_espacio(self):
        """Retorna la frase con el espacio en blanco"""
        return self.frase_completa.replace(self.palabra_clave, "______________________")


class PuntajeCompletarFrases(models.Model):
    """Puntuación del usuario en el juego de completar frases"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    puntaje_total = models.IntegerField(default=0)
    frases_completadas = models.IntegerField(default=0)
    respuestas_correctas = models.IntegerField(default=0)
    respuestas_parciales = models.IntegerField(default=0)
    respuestas_incorrectas = models.IntegerField(default=0)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user']
    
    def __str__(self):
        return f"{self.user.email} - {self.puntaje_total} puntos"


# ============================================
# FASE 1: EVALUACION Y METRICAS PARA INVESTIGACION
# ============================================

class FinancialCompetencyAssessment(models.Model):
    """Evaluacion de competencias financieras (puede tomarse múltiples veces)"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='competency_assessments')
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    numero_evaluacion = models.IntegerField(default=1)  # Número secuencial de la evaluación
    
    # Competencias Basicas (escala 1-5)
    conocimiento_presupuesto = models.IntegerField(default=0)
    conocimiento_ahorro = models.IntegerField(default=0)
    conocimiento_credito = models.IntegerField(default=0)
    conocimiento_inversiones = models.IntegerField(default=0)
    
    # Comportamientos de Endeudamiento
    tiene_tarjetas_credito = models.BooleanField(default=False)
    cantidad_tarjetas = models.IntegerField(default=0)
    monto_deuda_actual = models.FloatField(default=0.0)
    frecuencia_pago_minimo = models.IntegerField(default=0)  # veces al ano
    
    # Vulnerabilidad Digital
    conocimiento_fraudes = models.IntegerField(default=0)
    experiencia_fraude = models.BooleanField(default=False)
    
    # Brecha Teorico-Practica
    conocimiento_teorico = models.IntegerField(default=0)  # auto-evaluacion
    aplicacion_practica = models.IntegerField(default=0)   # auto-evaluacion
    
    puntaje_total = models.IntegerField(default=0)
    nivel_competencia = models.CharField(max_length=20, default='bajo')  # bajo, medio, alto
    
    def calcular_brecha_teorico_practica(self):
        return self.conocimiento_teorico - self.aplicacion_practica
    
    def calcular_puntaje_total(self):
        """Calcula el puntaje total de la evaluacion"""
        competencias = (
            self.conocimiento_presupuesto +
            self.conocimiento_ahorro +
            self.conocimiento_credito +
            self.conocimiento_inversiones +
            self.conocimiento_fraudes
        ) * 4  # Maximo 100 puntos por competencias
        
        comportamiento = 20 if not self.tiene_tarjetas_credito or self.monto_deuda_actual == 0 else max(0, 20 - (self.monto_deuda_actual / 1000))
        
        brecha = max(0, 20 - abs(self.calcular_brecha_teorico_practica()))
        
        total = competencias + comportamiento + brecha
        
        if total >= 80:
            self.nivel_competencia = 'alto'
        elif total >= 50:
            self.nivel_competencia = 'medio'
        else:
            self.nivel_competencia = 'bajo'
        
        return int(total)
    
    def save(self, *args, **kwargs):
        self.puntaje_total = self.calcular_puntaje_total()
        # Si no tiene número de evaluación, asignar el siguiente número
        if not self.numero_evaluacion or self.numero_evaluacion == 0:
            ultima_evaluacion = FinancialCompetencyAssessment.objects.filter(
                user=self.user
            ).order_by('-numero_evaluacion').first()
            if ultima_evaluacion:
                self.numero_evaluacion = ultima_evaluacion.numero_evaluacion + 1
            else:
                self.numero_evaluacion = 1
        super().save(*args, **kwargs)
        
        # Actualizar métricas del usuario automáticamente cuando se guarda una evaluación
        try:
            metrics, _ = UserMetrics.objects.get_or_create(user=self.user)
            metrics.actualizar_mejora()
            metrics.save()
        except:
            pass
    
    class Meta:
        ordering = ['-fecha_evaluacion']
    
    def __str__(self):
        return f"Evaluación {self.numero_evaluacion} - {self.user.email} ({self.puntaje_total} puntos)"


class UserMetrics(models.Model):
    """Metricas de usuario para evaluacion de impacto"""
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='metrics')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actividad = models.DateTimeField(auto_now=True)
    
    # Metricas de Engagement
    dias_activos = models.IntegerField(default=0)
    sesiones_totales = models.IntegerField(default=0)
    tiempo_total_uso = models.FloatField(default=0.0)  # horas
    
    # Metricas de Competencia Financiera
    puntaje_competencia_inicial = models.IntegerField(default=0)
    puntaje_competencia_actual = models.IntegerField(default=0)
    mejora_porcentual = models.FloatField(default=0.0)
    
    # Metricas de Comportamiento
    gasto_promedio_mensual_inicial = models.FloatField(default=0.0)
    gasto_promedio_mensual_actual = models.FloatField(default=0.0)
    reduccion_gasto = models.FloatField(default=0.0)
    
    ahorro_promedio_mensual_inicial = models.FloatField(default=0.0)
    ahorro_promedio_mensual_actual = models.FloatField(default=0.0)
    aumento_ahorro = models.FloatField(default=0.0)
    
    # Metricas de Riesgo Crediticio
    comportamientos_riesgo_inicial = models.IntegerField(default=0)
    comportamientos_riesgo_actual = models.IntegerField(default=0)
    reduccion_riesgo = models.FloatField(default=0.0)
    
    # Metricas de Gamificacion
    puntos_totales = models.IntegerField(default=0)
    retos_completados = models.IntegerField(default=0)
    trivias_completadas = models.IntegerField(default=0)
    nivel_actual = models.IntegerField(default=1)
    
    def actualizar_mejora(self):
        """Actualiza el porcentaje de mejora en competencias basado en primera y última evaluación"""
        # Obtener todas las evaluaciones ordenadas por número de evaluación
        todas_evaluaciones = FinancialCompetencyAssessment.objects.filter(
            user=self.user
        ).order_by('numero_evaluacion', 'fecha_evaluacion')
        
        if not todas_evaluaciones.exists():
            # No hay evaluaciones
            self.puntaje_competencia_inicial = 0
            self.puntaje_competencia_actual = 0
            self.mejora_porcentual = 0.0
            return
        
        # Primera evaluación (la de menor numero_evaluacion)
        primera_eval = todas_evaluaciones.first()
        
        # Última evaluación (la de mayor numero_evaluacion, o más reciente si hay empate)
        ultima_eval = todas_evaluaciones.order_by('-numero_evaluacion', '-fecha_evaluacion').first()
        
        # Actualizar puntajes basados en evaluaciones reales
        self.puntaje_competencia_inicial = primera_eval.puntaje_total
        self.puntaje_competencia_actual = ultima_eval.puntaje_total
        
        # Calcular mejora porcentual
        if self.puntaje_competencia_inicial > 0:
            self.mejora_porcentual = ((self.puntaje_competencia_actual - self.puntaje_competencia_inicial) / self.puntaje_competencia_inicial) * 100
        else:
            self.mejora_porcentual = 0.0
    
    def __str__(self):
        return f"Metricas {self.user.email} - Mejora: {self.mejora_porcentual:.1f}%"


class PeriodicAssessment(models.Model):
    """Evaluacion periodica mensual"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='periodic_assessments')
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    periodo_numero = models.IntegerField()  # 1, 2, 3 (meses)
    
    # Re-evaluacion de competencias
    puntaje_competencia = models.IntegerField()
    nivel_competencia = models.CharField(max_length=20)
    
    # Comportamientos observados
    gasto_total_periodo = models.FloatField()
    ahorro_total_periodo = models.FloatField()
    alertas_riesgo_recibidas = models.IntegerField(default=0)
    alertas_riesgo_atendidas = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Evaluacion Periodo {self.periodo_numero} - {self.user.email}"


# ============================================
# FASE 2: SIMULADORES
# ============================================

class CreditSimulator(models.Model):
    """Simulador de credito y prestamos"""
    TIPO_CREDITO_CHOICES = [
        ('personal', 'Personal'),
        ('vehicular', 'Vehicular'),
        ('hipotecario', 'Hipotecario'),
        ('tarjeta', 'Tarjeta de Credito'),
    ]
    
    TIPO_TASA_CHOICES = [
        ('fija', 'Tasa Fija'),
        ('variable', 'Tasa Variable'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='credit_simulations')
    fecha_simulacion = models.DateTimeField(auto_now_add=True)
    
    # Parametros del simulador
    tipo_credito = models.CharField(max_length=50, choices=TIPO_CREDITO_CHOICES)
    monto_solicitado = models.FloatField()
    plazo_meses = models.IntegerField()
    tasa_interes_anual = models.FloatField()  # TEA en soles
    tipo_tasa = models.CharField(max_length=20, choices=TIPO_TASA_CHOICES)
    
    # Resultados simulados
    cuota_mensual = models.FloatField()
    total_pagar = models.FloatField()
    total_intereses = models.FloatField()
    costo_total_credito = models.FloatField()  # CFT
    
    # Analisis de Riesgo
    nivel_endeudamiento = models.FloatField()  # % sobre ingresos
    evaluacion_riesgo = models.CharField(max_length=20)  # bajo, medio, alto
    recomendacion = models.TextField()
    
    def __str__(self):
        return f"Simulacion {self.tipo_credito} - {self.user.email}"


class EmergencySimulator(models.Model):
    """Simulador de emergencias financieras"""
    ESCENARIO_CHOICES = [
        ('perdida_empleo', 'Perdida de Empleo'),
        ('enfermedad', 'Enfermedad o Emergencia Medica'),
        ('reparacion_urgente', 'Reparacion Urgente'),
        ('otro', 'Otra Emergencia'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='emergency_simulations')
    escenario = models.CharField(max_length=100, choices=ESCENARIO_CHOICES)
    monto_emergencia = models.FloatField()
    fondo_emergencia_actual = models.FloatField()
    ingresos_mensuales = models.FloatField()
    
    # Analisis
    meses_protegido = models.FloatField()
    deficit_fondo = models.FloatField()
    plan_ahorro_emergencia = models.TextField()
    fecha_simulacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Emergencia {self.escenario} - {self.user.email}"


# ============================================
# FASE 2: ALERTAS DE RIESGO
# ============================================

class CreditRiskAlert(models.Model):
    """Alertas de riesgo crediticio"""
    TIPO_ALERTA_CHOICES = [
        ('gasto_excesivo', 'Gasto Excesivo'),
        ('limite_proximo', 'Limite Proximo'),
        ('deuda_alta', 'Deuda Alta'),
        ('pago_minimo', 'Solo Pago Minimo'),
        ('sin_ahorro', 'Sin Ahorro Mensual'),
    ]
    
    SEVERIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='risk_alerts')
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    tipo_alerta = models.CharField(max_length=50, choices=TIPO_ALERTA_CHOICES)
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES)
    descripcion = models.TextField()
    recomendacion = models.TextField()
    vista = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Alerta {self.tipo_alerta} - {self.user.email}"


class TransactionAlert(models.Model):
    """Alertas de transacciones sospechosas"""
    TIPO_ALERTA_CHOICES = [
        ('monto_inesperado', 'Monto Inesperado'),
        ('horario_inusual', 'Horario Inusual'),
        ('ubicacion_nueva', 'Ubicacion Nueva'),
        ('frecuencia_anomalia', 'Frecuencia Anomala'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transaction_alerts')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='alerts')
    fecha_deteccion = models.DateTimeField(auto_now_add=True)
    tipo_alerta = models.CharField(max_length=50, choices=TIPO_ALERTA_CHOICES)
    nivel_riesgo = models.IntegerField(default=1)  # 1-5
    verificada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Alerta Transaccion {self.tipo_alerta} - {self.user.email}"


# ============================================
# FASE 3: GAMIFICACION AVANZADA
# ============================================

class Achievement(models.Model):
    """Logros y logros del sistema"""
    CATEGORIA_CHOICES = [
        ('ahorro', 'Ahorro'),
        ('educacion', 'Educacion'),
        ('consistencia', 'Consistencia'),
        ('riesgo', 'Gestion de Riesgo'),
        ('presupuesto', 'Presupuesto'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='🏆')
    puntos_bonus = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    requisito = models.JSONField(default=dict)  # condiciones para desbloquear
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo


class UserAchievement(models.Model):
    """Logros desbloqueados por usuario"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='users')
    fecha_desbloqueo = models.DateTimeField(auto_now_add=True)
    progreso = models.FloatField(default=0.0)  # 0-100%
    
    class Meta:
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.email} - {self.achievement.titulo}"


class Storyline(models.Model):
    """Narrativa progresiva del viaje financiero"""
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    capitulo_numero = models.IntegerField()
    requisitos_desbloqueo = models.JSONField(default=dict)
    contenido_educativo = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['capitulo_numero']
    
    def __str__(self):
        return f"Capitulo {self.capitulo_numero}: {self.titulo}"


class StoryProgress(models.Model):
    """Progreso del usuario en la narrativa"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='story_progress')
    storyline = models.ForeignKey(Storyline, on_delete=models.CASCADE, related_name='progress')
    desbloqueado = models.BooleanField(default=False)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'storyline']
    
    def __str__(self):
        return f"{self.user.email} - {self.storyline.titulo}"


# ============================================
# FASE 3: CONTENIDO EDUCATIVO
# ============================================

class EducationalContent(models.Model):
    """Biblioteca de contenido educativo"""
    TIPO_CONTENIDO_CHOICES = [
        ('articulo', 'Articulo'),
        ('video', 'Video'),
        ('infografia', 'Infografia'),
        ('curso', 'Curso Interactivo'),
    ]
    
    CATEGORIA_CHOICES = [
        ('presupuesto', 'Presupuesto'),
        ('credito', 'Credito'),
        ('ahorro', 'Ahorro'),
        ('inversion', 'Inversion'),
        ('fraude', 'Fraude Digital'),
        ('general', 'General'),
    ]
    
    titulo = models.CharField(max_length=200)
    tipo_contenido = models.CharField(max_length=50, choices=TIPO_CONTENIDO_CHOICES)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField()
    contenido = models.TextField()  # o URL si es video
    nivel_dificultad = models.IntegerField(default=1)  # 1-5
    duracion_minutos = models.IntegerField(default=10)
    
    # Contextualizacion Peruana
    incluye_ejemplos_peru = models.BooleanField(default=True)
    instituciones_mencionadas = models.JSONField(default=list)  # SBS, BCP, etc.
    tasas_actuales = models.JSONField(default=dict)  # referencias actualizadas
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    visualizaciones = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo


# ============================================
# FASE 4: PREVENCION DE FRAUDES
# ============================================

class FraudPreventionContent(models.Model):
    """Contenido educativo sobre prevencion de fraudes"""
    TIPO_FRAUDE_CHOICES = [
        ('phishing', 'Phishing'),
        ('pharming', 'Pharming'),
        ('smishing', 'Smishing'),
        ('vishing', 'Vishing'),
        ('skimming', 'Skimming'),
        ('identity_theft', 'Robo de Identidad'),
    ]
    
    titulo = models.CharField(max_length=200)
    tipo_fraude = models.CharField(max_length=50, choices=TIPO_FRAUDE_CHOICES)
    descripcion = models.TextField()
    ejemplo_real = models.TextField()  # Casos en Peru
    como_protegerse = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nivel_dificultad = models.IntegerField(default=1)  # 1-5
    is_active = models.BooleanField(default=True)
    visualizaciones = models.IntegerField(default=0)
    
    def __str__(self):
        return self.titulo


# ============================================
# FASE 4: PERSONALIZACION
# ============================================

class UserContext(models.Model):
    """Contexto socioeconomico y preferencias del usuario"""
    NIVEL_SOCIOECONOMICO_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]
    
    ESTILO_APRENDIZAJE_CHOICES = [
        ('visual', 'Visual'),
        ('practico', 'Practico'),
        ('teorico', 'Teorico'),
    ]
    
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='context')
    
    # Contexto Socioeconomico
    nivel_socioeconomico = models.CharField(max_length=20, choices=NIVEL_SOCIOECONOMICO_CHOICES, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    ingresos_aproximados = models.FloatField(null=True, blank=True)
    
    # Preferencias de Aprendizaje
    estilo_aprendizaje = models.CharField(max_length=20, choices=ESTILO_APRENDIZAJE_CHOICES, null=True, blank=True)
    nivel_conocimiento_actual = models.CharField(max_length=20, null=True, blank=True)
    areas_interes = models.JSONField(default=list)  # lista de areas
    
    # Adaptaciones IA
    contenido_priorizado = models.JSONField(default=list)
    dificultad_adaptativa = models.IntegerField(default=3)  # 1-5
    
    def __str__(self):
        return f"Contexto {self.user.email}"


class PersonalizedRecommendation(models.Model):
    """Recomendaciones personalizadas por IA"""
    TIPO_RECOMENDACION_CHOICES = [
        ('contenido', 'Contenido Educativo'),
        ('reto', 'Reto Personalizado'),
        ('alerta', 'Alerta Proactiva'),
        ('simulador', 'Simulador Relevante'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='personalized_recommendations')
    tipo_recomendacion = models.CharField(max_length=50, choices=TIPO_RECOMENDACION_CHOICES)
    contenido = models.TextField()
    razon = models.TextField()  # Por que se recomienda (basado en IA)
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    vista = models.BooleanField(default=False)
    aplicada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Recomendacion {self.tipo_recomendacion} - {self.user.email}"


class PregeneradaEvaluacion(models.Model):
    """Evaluación pre-generada por IA para un usuario"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='pregeneradas_evaluaciones')
    preguntas_evaluacion = models.JSONField()  # Todas las preguntas por categoría
    preguntas_brecha = models.JSONField()  # Preguntas de brecha teórico-práctica
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usada = models.BooleanField(default=False)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Evaluación pre-generada para {self.user.email} - {'Usada' if self.usada else 'Disponible'}"


class PregeneradaFraseCompletar(models.Model):
    """Frase pre-generada por IA para el juego Completar Frases"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='pregeneradas_frases')
    frase_completa = models.TextField()
    palabra_clave = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usada = models.BooleanField(default=False)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Frase pre-generada para {self.user.email} - {'Usada' if self.usada else 'Disponible'}"