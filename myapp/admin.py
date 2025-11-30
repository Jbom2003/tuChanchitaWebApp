from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    UserProfile, Expense, PaymentMethod, Investment,
    RecommendationVideo, Challenge, UserChallenge,
    PreguntaTrivia, PuntajeTrivia, FraseCompletar, PuntajeCompletarFrases,
    # Modelos para Investigacion
    FinancialCompetencyAssessment, UserMetrics, PeriodicAssessment,
    CreditSimulator, EmergencySimulator, CreditRiskAlert, TransactionAlert,
    Achievement, UserAchievement, EducationalContent, FraudPreventionContent,
    Storyline, StoryProgress, UserContext, PersonalizedRecommendation
)

@admin.register(PreguntaTrivia)
class PreguntaTriviaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'mostrar_opciones', 'respuesta_correcta')
    search_fields = ('pregunta',)

    def mostrar_opciones(self, obj):
        return ", ".join([f"{k}: {v}" for k, v in obj.opciones.items()])

@admin.register(PuntajeTrivia)
class PuntajeTriviaAdmin(admin.ModelAdmin):
    list_display = ('user', 'puntaje_total', 'intentos', 'ultima_actualizacion')
    search_fields = ('user__email',)

    def save_model(self, request, obj, form, change):
        # Guardar el objeto normalmente
        super().save_model(request, obj, form, change)

        # También actualizar el puntaje en UserProfile si es mayor
        if obj.puntaje_total > obj.user.trivia_puntaje:
            obj.user.trivia_puntaje = obj.puntaje_total
            obj.user.save()


@admin.register(FraseCompletar)
class FraseCompletarAdmin(admin.ModelAdmin):
    list_display = ('frase_completa', 'palabra_clave', 'categoria', 'nivel_dificultad', 'activa', 'fecha_creacion')
    list_filter = ('categoria', 'nivel_dificultad', 'activa', 'fecha_creacion')
    search_fields = ('frase_completa', 'palabra_clave', 'categoria')
    readonly_fields = ('fecha_creacion',)


@admin.register(PuntajeCompletarFrases)
class PuntajeCompletarFrasesAdmin(admin.ModelAdmin):
    list_display = ('user', 'puntaje_total', 'frases_completadas', 'respuestas_correctas', 'respuestas_parciales', 'respuestas_incorrectas', 'ultima_actualizacion')
    list_filter = ('ultima_actualizacion',)
    search_fields = ('user__email',)
    readonly_fields = ('ultima_actualizacion',)

admin.site.register(RecommendationVideo)
admin.site.register(Challenge)
admin.site.register(UserChallenge)


# ============================================
# ADMIN PARA MODELOS DE INVESTIGACION
# ============================================

@admin.register(FinancialCompetencyAssessment)
class FinancialCompetencyAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha_evaluacion', 'puntaje_total', 'nivel_competencia', 'calcular_brecha_teorico_practica')
    list_filter = ('nivel_competencia', 'fecha_evaluacion')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('puntaje_total', 'nivel_competencia')


@admin.register(UserMetrics)
class UserMetricsAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha_registro', 'mejora_porcentual', 'dias_activos', 'retos_completados')
    list_filter = ('fecha_registro',)
    search_fields = ('user__email',)
    readonly_fields = ('fecha_registro', 'fecha_ultima_actividad')


@admin.register(PeriodicAssessment)
class PeriodicAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'periodo_numero', 'fecha_evaluacion', 'puntaje_competencia', 'nivel_competencia')
    list_filter = ('periodo_numero', 'nivel_competencia')
    search_fields = ('user__email',)


@admin.register(CreditSimulator)
class CreditSimulatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_credito', 'monto_solicitado', 'cuota_mensual', 'evaluacion_riesgo', 'fecha_simulacion')
    list_filter = ('tipo_credito', 'evaluacion_riesgo', 'fecha_simulacion')
    search_fields = ('user__email',)


@admin.register(EmergencySimulator)
class EmergencySimulatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'escenario', 'monto_emergencia', 'meses_protegido', 'fecha_simulacion')
    list_filter = ('escenario', 'fecha_simulacion')
    search_fields = ('user__email',)


@admin.register(CreditRiskAlert)
class CreditRiskAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_alerta', 'severidad', 'vista', 'fecha_alerta')
    list_filter = ('tipo_alerta', 'severidad', 'vista', 'fecha_alerta')
    search_fields = ('user__email', 'descripcion')
    readonly_fields = ('fecha_alerta',)


@admin.register(TransactionAlert)
class TransactionAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_alerta', 'nivel_riesgo', 'verificada', 'fecha_deteccion')
    list_filter = ('tipo_alerta', 'nivel_riesgo', 'verificada')
    search_fields = ('user__email',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'categoria', 'puntos_bonus', 'is_active')
    list_filter = ('categoria', 'is_active')
    search_fields = ('titulo', 'codigo')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'fecha_desbloqueo', 'progreso')
    list_filter = ('fecha_desbloqueo',)
    search_fields = ('user__email', 'achievement__titulo')
    readonly_fields = ('fecha_desbloqueo',)


@admin.register(EducationalContent)
class EducationalContentAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_contenido', 'categoria', 'nivel_dificultad', 'visualizaciones', 'is_active')
    list_filter = ('tipo_contenido', 'categoria', 'nivel_dificultad', 'is_active')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('visualizaciones', 'fecha_creacion')


@admin.register(FraudPreventionContent)
class FraudPreventionContentAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_fraude', 'nivel_dificultad', 'fecha_creacion', 'is_active')
    list_filter = ('tipo_fraude', 'nivel_dificultad', 'is_active')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_creacion',)


@admin.register(Storyline)
class StorylineAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'capitulo_numero', 'is_active')
    list_filter = ('is_active',)
    ordering = ('capitulo_numero',)
    search_fields = ('titulo',)


@admin.register(StoryProgress)
class StoryProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'storyline', 'desbloqueado', 'completado', 'fecha_completado')
    list_filter = ('desbloqueado', 'completado')
    search_fields = ('user__email', 'storyline__titulo')
    readonly_fields = ('fecha_completado',)


@admin.register(UserContext)
class UserContextAdmin(admin.ModelAdmin):
    list_display = ('user', 'nivel_socioeconomico', 'region', 'estilo_aprendizaje')
    list_filter = ('nivel_socioeconomico', 'estilo_aprendizaje')
    search_fields = ('user__email', 'region')


@admin.register(PersonalizedRecommendation)
class PersonalizedRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_recomendacion', 'vista', 'aplicada', 'fecha_recomendacion')
    list_filter = ('tipo_recomendacion', 'vista', 'aplicada', 'fecha_recomendacion')
    search_fields = ('user__email', 'contenido')
    readonly_fields = ('fecha_recomendacion',)


# ============================================
# ADMIN PERSONALIZADO PARA USERPROFILE
# ============================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre_completo', 'fecha_registro', 'puntaje_competencia_actual', 'mejora_porcentual', 'dias_activos', 'retos_completados', 'ver_detalles')
    list_filter = ('is_blocked',)
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('password', 'fecha_registro', 'stats_evaluaciones', 'stats_metricas', 'stats_gastos', 'stats_juegos')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('email', 'password', 'first_name', 'last_name', 'photo')
        }),
        ('Configuración Financiera', {
            'fields': ('monthly_limit', 'points', 'trivia_puntaje')
        }),
        ('Seguridad', {
            'fields': ('login_attempts', 'is_blocked')
        }),
        ('Estadísticas de Evaluaciones', {
            'fields': ('stats_evaluaciones',),
            'classes': ('collapse',)
        }),
        ('Estadísticas de Métricas', {
            'fields': ('stats_metricas',),
            'classes': ('collapse',)
        }),
        ('Estadísticas de Gastos', {
            'fields': ('stats_gastos',),
            'classes': ('collapse',)
        }),
        ('Estadísticas de Juegos', {
            'fields': ('stats_juegos',),
            'classes': ('collapse',)
        }),
    )
    
    def nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    nombre_completo.short_description = 'Nombre Completo'
    
    def fecha_registro(self, obj):
        try:
            metrics = obj.metrics
            return metrics.fecha_registro.strftime('%d/%m/%Y %H:%M')
        except:
            return 'N/A'
    fecha_registro.short_description = 'Fecha de Registro'
    
    def puntaje_competencia_actual(self, obj):
        try:
            metrics = obj.metrics
            return f"{metrics.puntaje_competencia_actual} puntos"
        except:
            return 'N/A'
    puntaje_competencia_actual.short_description = 'Puntaje Actual'
    
    def mejora_porcentual(self, obj):
        try:
            metrics = obj.metrics
            color = 'green' if metrics.mejora_porcentual > 0 else 'red' if metrics.mejora_porcentual < 0 else 'gray'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
                color,
                metrics.mejora_porcentual
            )
        except:
            return 'N/A'
    mejora_porcentual.short_description = 'Mejora %'
    
    def dias_activos(self, obj):
        try:
            metrics = obj.metrics
            return metrics.dias_activos
        except:
            return 0
    dias_activos.short_description = 'Días Activos'
    
    def retos_completados(self, obj):
        try:
            metrics = obj.metrics
            return metrics.retos_completados
        except:
            return 0
    retos_completados.short_description = 'Retos Completados'
    
    def ver_detalles(self, obj):
        url = reverse('admin:myapp_userprofile_change', args=[obj.pk])
        return format_html('<a href="{}">Ver/Editar</a>', url)
    ver_detalles.short_description = 'Acciones'
    
    def stats_evaluaciones(self, obj):
        evaluaciones = FinancialCompetencyAssessment.objects.filter(user=obj).order_by('-numero_evaluacion')[:10]
        if not evaluaciones.exists():
            return "No hay evaluaciones registradas"
        
        html = "<table style='width:100%; border-collapse: collapse;'>"
        html += "<tr style='background: #f0f0f0;'><th style='padding: 8px; border: 1px solid #ddd;'>Evaluación</th>"
        html += "<th style='padding: 8px; border: 1px solid #ddd;'>Fecha</th>"
        html += "<th style='padding: 8px; border: 1px solid #ddd;'>Puntaje</th>"
        html += "<th style='padding: 8px; border: 1px solid #ddd;'>Nivel</th>"
        html += "<th style='padding: 8px; border: 1px solid #ddd;'>Brecha</th></tr>"
        
        for eval in evaluaciones:
            color = 'green' if eval.nivel_competencia == 'alto' else 'orange' if eval.nivel_competencia == 'medio' else 'red'
            html += f"<tr>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd;'>{eval.numero_evaluacion}</td>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd;'>{eval.fecha_evaluacion.strftime('%d/%m/%Y')}</td>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd; font-weight: bold;'>{eval.puntaje_total}</td>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd; color: {color}; font-weight: bold;'>{eval.nivel_competencia.upper()}</td>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd;'>{eval.calcular_brecha_teorico_practica()}</td>"
            html += f"</tr>"
        
        html += "</table>"
        html += f"<p style='margin-top: 10px;'><strong>Total de evaluaciones:</strong> {evaluaciones.count()}</p>"
        return mark_safe(html)
    stats_evaluaciones.short_description = 'Historial de Evaluaciones'
    
    def stats_metricas(self, obj):
        try:
            metrics = obj.metrics
            html = "<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>"
            html += f"<div><strong>Mejora en Competencias:</strong> {metrics.mejora_porcentual:.1f}%</div>"
            html += f"<div><strong>Días Activos:</strong> {metrics.dias_activos}</div>"
            html += f"<div><strong>Retos Completados:</strong> {metrics.retos_completados}</div>"
            html += f"<div><strong>Puntos Totales:</strong> {metrics.puntos_totales}</div>"
            html += f"<div><strong>Reducción de Gasto:</strong> {metrics.reduccion_gasto:.1f}%</div>"
            html += f"<div><strong>Aumento de Ahorro:</strong> {metrics.aumento_ahorro:.1f}%</div>"
            html += f"<div><strong>Puntaje Inicial:</strong> {metrics.puntaje_competencia_inicial}</div>"
            html += f"<div><strong>Puntaje Actual:</strong> {metrics.puntaje_competencia_actual}</div>"
            html += "</div>"
            return mark_safe(html)
        except:
            return "No hay métricas disponibles"
    stats_metricas.short_description = 'Métricas del Usuario'
    
    def stats_gastos(self, obj):
        from django.db.models import Sum, Count
        from datetime import datetime, timedelta
        
        gastos_totales = Expense.objects.filter(user=obj).aggregate(total=Sum('amount'))['total'] or 0
        cantidad_gastos = Expense.objects.filter(user=obj).count()
        
        # Gastos del mes actual
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        gastos_mes = Expense.objects.filter(
            user=obj,
            date__month=mes_actual,
            date__year=anio_actual
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        html = f"<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>"
        html += f"<div><strong>Gastos Totales:</strong> S/. {gastos_totales:.2f}</div>"
        html += f"<div><strong>Cantidad de Gastos:</strong> {cantidad_gastos}</div>"
        html += f"<div><strong>Gastos del Mes Actual:</strong> S/. {gastos_mes:.2f}</div>"
        html += f"<div><strong>Límite Mensual:</strong> S/. {obj.monthly_limit:.2f}</div>"
        html += "</div>"
        return mark_safe(html)
    stats_gastos.short_description = 'Estadísticas de Gastos'
    
    def stats_juegos(self, obj):
        try:
            puntaje_trivia = PuntajeTrivia.objects.filter(user=obj).first()
            puntaje_completar = PuntajeCompletarFrases.objects.filter(user=obj).first()
            
            html = "<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>"
            html += f"<div><strong>Puntaje Trivia:</strong> {obj.trivia_puntaje or 0}</div>"
            if puntaje_trivia:
                html += f"<div><strong>Intentos Trivia:</strong> {puntaje_trivia.intentos}</div>"
            if puntaje_completar:
                html += f"<div><strong>Puntaje Completar Frases:</strong> {puntaje_completar.puntaje_total}</div>"
                html += f"<div><strong>Frases Completadas:</strong> {puntaje_completar.frases_completadas}</div>"
            html += "</div>"
            return mark_safe(html)
        except:
            return "No hay estadísticas de juegos"
    stats_juegos.short_description = 'Estadísticas de Juegos'
