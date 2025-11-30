# Plan de Mejoras para Alineacion con Objetivos de Investigacion

## Resumen Ejecutivo

Este documento propone mejoras especificas para alinear la aplicacion TuChanchita con los objetivos de investigacion sobre competencias financieras en jovenes peruanos de 18-25 anos, integrando gamificacion e inteligencia artificial.

---

## 1. DIAGNOSTICO INICIAL DE COMPETENCIAS FINANCIERAS

### Objetivo Especifico Alineado
Diagnosticar el nivel actual de competencias financieras, comportamientos de endeudamiento y vulnerabilidad a riesgos digitales.

### Propuesta de Implementacion

#### 1.1 Cuestionario de Evaluacion Inicial (Al Registrarse)

**Modelo Nuevo: `FinancialCompetencyAssessment`**
```python
class FinancialCompetencyAssessment(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
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
```

**Vista: `evaluacion_inicial_view`**
- Cuestionario interactivo de 20-25 preguntas
- Categorizado por areas (presupuesto, ahorro, credito, fraudes)
- Asigna nivel inicial: Bajo, Medio, Alto
- Guarda baseline para comparacion posterior

#### 1.2 Dashboard de Progreso Individual

**Vista: `progreso_competencia_view`**
- Grafico comparativo: Inicial vs Actual
- Metrica de brecha teorico-practica reducida
- Porcentaje de mejora por area
- Alertas de areas que necesitan refuerzo

---

## 2. SIMULADORES PRACTICOS CONTEXTUALIZADOS AL PERU

### Objetivo Especifico Alineado
Implementar modulos educativos interactivos con simuladores practicos y escenarios contextualizados.

### Propuestas de Implementacion

#### 2.1 Simulador de Credito y Prestamos

**Modelo Nuevo: `CreditSimulator`**
```python
class CreditSimulator(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_simulacion = models.DateTimeField(auto_now_add=True)
    
    # Parametros del simulador (contexto Peruano)
    tipo_credito = models.CharField(max_length=50)  # personal, vehicular, hipotecario
    monto_solicitado = models.FloatField()
    plazo_meses = models.IntegerField()
    tasa_interes_anual = models.FloatField()  # TEA en soles
    tipo_tasa = models.CharField(max_length=20)  # fija, variable
    
    # Resultados simulados
    cuota_mensual = models.FloatField()
    total_pagar = models.FloatField()
    total_intereses = models.FloatField()
    costo_total_credito = models.FloatField()  # CFT
    
    # Analisis de Riesgo
    nivel_endeudamiento = models.FloatField()  # % sobre ingresos
    evaluacion_riesgo = models.CharField(max_length=20)  # bajo, medio, alto
    recomendacion = models.TextField()
```

**Vista: `simulador_credito_view`**
- Calculadora interactiva con tasas actuales de bancos peruanos
- Comparacion entre opciones (BCP, BBVA, Interbank, etc.)
- Alertas de sobreendeudamiento basado en ingresos del usuario
- Simulacion de escenarios "que pasaria si..."

#### 2.2 Simulador de Emergencias Financieras

**Modelo Nuevo: `EmergencySimulator`**
```python
class EmergencySimulator(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    escenario = models.CharField(max_length=100)  # perdida_empleo, enfermedad, reparacion_urgente
    monto_emergencia = models.FloatField()
    fondo_emergencia_actual = models.FloatField()
    ingresos_mensuales = models.FloatField()
    
    # Analisis
    meses_protegido = models.FloatField()
    deficit_fondo = models.FloatField()
    plan_ahorro_emergencia = models.TextField()
```

**Vista: `simulador_emergencia_view`**
- Escenarios comunes en Peru (desempleo, gastos medicos, etc.)
- Calculadora de fondo de emergencia ideal (6 meses de gastos)
- Plan personalizado de ahorro para emergencias

#### 2.3 Simulador de Inversion (Mejora del Existente)

**Mejoras al modelo `Investment` existente:**
- Agregar opciones de inversion peruanas (depositos a plazo, fondos mutuos locales)
- Simulador de rendimiento con datos historicos del mercado peruano
- Comparacion riesgo/rendimiento entre opciones
- Educacion sobre diversificacion

---

## 3. SISTEMA DE ALERTAS DE RIESGO CREDITICIO

### Objetivo Especifico Alineado
Reducir comportamientos de riesgo crediticio y sobreendeudamiento.

### Propuesta de Implementacion

#### 3.1 Modelo de Alerta de Riesgo

**Modelo Nuevo: `CreditRiskAlert`**
```python
class CreditRiskAlert(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    tipo_alerta = models.CharField(max_length=50)  # gasto_excesivo, limite_proximo, deuda_alta
    severidad = models.CharField(max_length=20)  # baja, media, alta
    descripcion = models.TextField()
    recomendacion = models.TextField()
    vista = models.BooleanField(default=False)
```

**Vista: `alertas_riesgo_view`**
- Dashboard de alertas activas
- Notificaciones cuando:
  - Gasto mensual > 80% del limite
  - Tasa de ahorro < 10% de ingresos
  - Deuda acumulada creciendo
  - Pagos en fecha limite

#### 3.2 Calculadora de Capacidad de Endeudamiento

**Vista: `capacidad_endeudamiento_view`**
- Formula: (Ingresos - Gastos Fijos) * 30%
- Simulacion: "Puedo asumir un credito de X soles"
- Comparacion con deuda actual
- Recomendaciones personalizadas

---

## 4. MODULO DE PREVENCION DE FRAUDES DIGITALES

### Objetivo Especifico Alineado
Abordar vulnerabilidad a riesgos digitales.

### Propuesta de Implementacion

#### 4.1 Modelo de Contenido Educativo Anti-Fraude

**Modelo Nuevo: `FraudPreventionContent`**
```python
class FraudPreventionContent(models.Model):
    titulo = models.CharField(max_length=200)
    tipo_fraude = models.CharField(max_length=50)  # phishing, pharming, smishing, etc.
    descripcion = models.TextField()
    ejemplo_real = models.TextField()  # Casos en Peru
    como_protegerse = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nivel_dificultad = models.IntegerField(default=1)  # 1-5
```

**Vista: `prevencion_fraudes_view`**
- Biblioteca de contenidos educativos
- Trivias especificas sobre fraudes digitales
- Simulaciones interactivas de intentos de fraude
- Reporte de intentos sospechosos (opcional)

#### 4.2 Sistema de Verificacion de Transacciones

**Modelo Nuevo: `TransactionAlert`**
```python
class TransactionAlert(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    fecha_deteccion = models.DateTimeField(auto_now_add=True)
    tipo_alerta = models.CharField(max_length=50)  # monto_inesperado, horario_insusual, ubicacion_nueva
    nivel_riesgo = models.IntegerField(default=1)  # 1-5
    verificada = models.BooleanField(default=False)
```

**Funcionalidad:**
- IA que detecta patrones inusuales en gastos
- Alertas en tiempo real
- Verificacion manual por el usuario

---

## 5. SISTEMA DE METRICAS PARA EVALUACION DE IMPACTO

### Objetivo Especifico Alineado
Evaluar el impacto mediante estudio piloto durante 3 meses.

### Propuesta de Implementacion

#### 5.1 Modelo de Metricas de Usuario

**Modelo Nuevo: `UserMetrics`**
```python
class UserMetrics(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actividad = models.DateTimeField(auto_now=True)
    
    # Metricas de Engagement (para Hipotesis)
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
```

#### 5.2 Vista de Reporte de Impacto (Para Investigador)

**Vista: `reporte_impacto_admin_view`** (solo administradores)
- Dashboard con metricas agregadas de todos los usuarios
- Calculo automatico de:
  - Mejora promedio en competencias financieras (%)
  - Reduccion promedio en comportamientos de riesgo (%)
  - Engagement promedio (dias activos, tiempo uso)
- Exportacion a CSV/Excel para analisis estadistico
- Graficos comparativos: Antes vs Despues

#### 5.3 Evaluacion Periodica (Cada 30 dias)

**Modelo Nuevo: `PeriodicAssessment`**
```python
class PeriodicAssessment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    periodo_numero = models.IntegerField()  # 1, 2, 3 (meses)
    
    # Re-evaluacion de competencias
    puntaje_competencia = models.IntegerField()
    nivel_competencia = models.CharField(max_length=20)
    
    # Comportamientos observados (de datos reales de uso)
    gasto_total_periodo = models.FloatField()
    ahorro_total_periodo = models.FloatField()
    alertas_riesgo_recibidas = models.IntegerField()
    alertas_riesgo_atendidas = models.IntegerField()
```

**Vista: `evaluacion_periodica_view`**
- Cuestionario corto cada mes
- Comparacion con evaluacion anterior
- Feedback visual del progreso

---

## 6. PERSONALIZACION CON INTELIGENCIA ARTIFICIAL

### Objetivo Especifico Alineado
Algoritmos de IA para personalizacion del aprendizaje, adaptando contenido al contexto socioeconomico peruano.

### Propuestas de Implementacion

#### 6.1 Sistema de Recomendaciones Personalizadas Mejorado

**Mejoras al chatbot existente:**
- Analizar perfil financiero del usuario (gastos, ahorros, nivel)
- Recomendar contenido educativo relevante
- Sugerir retos personalizados basados en debilidades
- Alertas proactivas basadas en patrones

**Modelo Nuevo: `PersonalizedRecommendation`**
```python
class PersonalizedRecommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tipo_recomendacion = models.CharField(max_length=50)  # contenido, reto, alerta
    contenido = models.TextField()
    razon = models.TextField()  # Por que se recomienda (basado en IA)
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    vista = models.BooleanField(default=False)
    aplicada = models.BooleanField(default=False)
```

#### 6.2 Adaptacion de Contenido al Contexto Socioeconomico

**Modelo Nuevo: `UserContext`**
```python
class UserContext(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    
    # Contexto Socioeconomico
    nivel_socioeconomico = models.CharField(max_length=20)  # bajo, medio, alto
    region = models.CharField(max_length=50)  # Lima, provincia, etc.
    ingresos_aproximados = models.FloatField(null=True, blank=True)
    
    # Preferencias de Aprendizaje
    estilo_aprendizaje = models.CharField(max_length=20)  # visual, practico, teorico
    nivel_conocimiento_actual = models.CharField(max_length=20)
    areas_interes = models.JSONField(default=list)  # lista de areas
    
    # Adaptaciones IA
    contenido_priorizado = models.JSONField(default=list)
    dificultad_adaptativa = models.IntegerField(default=3)  # 1-5
```

---

## 7. GAMIFICACION AVANZADA

### Objetivo Especifico Alineado
Mecanicas de gamificacion: sistema de recompensas, narrativas progresivas, desafios adaptativos.

### Propuestas de Implementacion

#### 7.1 Sistema de Niveles y Logros

**Modelo Nuevo: `Achievement` y `UserAchievement`**
```python
class Achievement(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50)
    puntos_bonus = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50)  # ahorro, educacion, consistencia
    requisito = models.JSONField(default=dict)  # condiciones para desbloquear
    
class UserAchievement(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    fecha_desbloqueo = models.DateTimeField(auto_now_add=True)
    progreso = models.FloatField(default=0.0)  # 0-100%
```

**Ejemplos de Logros:**
- "Primer Ahorro" (ahorrar por primera vez)
- "Semanario Consistente" (7 dias consecutivos usando la app)
- "Maestro del Presupuesto" (cumplir presupuesto 3 meses seguidos)
- "Guerrero Anti-Fraude" (completar todos los modulos de fraude)

#### 7.2 Narrativa Progresiva

**Modelo Nuevo: `Storyline` y `StoryProgress`**
```python
class Storyline(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    capitulo_numero = models.IntegerField()
    requisitos_desbloqueo = models.JSONField(default=dict)
    contenido_educativo = models.TextField()
    
class StoryProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    storyline = models.ForeignKey(Storyline, on_delete=models.CASCADE)
    desbloqueado = models.BooleanField(default=False)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
```

**Concepto:**
- Historia de "El Viaje Financiero" del usuario
- Cada capitulo desbloquea al completar objetivos
- Narrativa adaptada al contexto peruano

#### 7.3 Desafios Adaptativos

**Mejoras al modelo `Challenge` existente:**
- Agregar campo `dificultad_adaptativa`
- IA ajusta dificultad segun desempeno previo
- Retos mas desafiantes para usuarios avanzados
- Retos mas accesibles para principiantes

---

## 8. CONTENIDO EDUCATIVO CONTEXTUALIZADO AL PERU

### Propuesta de Implementacion

#### 8.1 Biblioteca de Contenido Educativo

**Modelo Nuevo: `EducationalContent`**
```python
class EducationalContent(models.Model):
    titulo = models.CharField(max_length=200)
    tipo_contenido = models.CharField(max_length=50)  # articulo, video, infografia, curso
    categoria = models.CharField(max_length=50)  # presupuesto, credito, ahorro, inversion, fraude
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
```

**Vista: `biblioteca_educativa_view`**
- Filtros por categoria y nivel
- Busqueda por palabras clave
- Progreso de contenido visto
- Recomendaciones basadas en perfil

---

## 9. PRIORIZACION DE IMPLEMENTACION

### Fase 1 (Critico para Investigacion - 2 semanas)
1. **Cuestionario de Evaluacion Inicial** (Objetivo 1)
2. **Modelo de Metricas de Usuario** (Objetivo 4)
3. **Dashboard de Progreso Individual** (Objetivo 4)

### Fase 2 (Alto Impacto - 3 semanas)
4. **Simulador de Credito** (Objetivo 3)
5. **Sistema de Alertas de Riesgo** (Hipotesis)
6. **Evaluacion Periodica** (Objetivo 4)

### Fase 3 (Mejoras de Engagement - 2 semanas)
7. **Sistema de Logros** (Gamificacion)
8. **Biblioteca de Contenido Educativo** (Objetivo 3)
9. **Mejoras al Chatbot con IA** (Personalizacion)

### Fase 4 (Caracteristicas Avanzadas - 3 semanas)
10. **Modulo de Prevencion de Fraudes** (Objetivo 1)
11. **Simulador de Emergencias** (Objetivo 3)
12. **Sistema de Narrativa** (Gamificacion avanzada)
13. **Vista de Reporte de Impacto para Admin** (Objetivo 4)

---

## 10. METRICAS PARA VALIDAR HIPOTESIS

### Hipotesis General
Mejora >=30% en competencias financieras practicas

**Metricas:**
- `mejora_porcentual` en `UserMetrics` (calculado mensualmente)
- Comparacion: `puntaje_competencia_actual` vs `puntaje_competencia_inicial`
- Filtro: Solo usuarios con >=30 dias de uso

### Hipotesis Especifica 1
Retencion y aplicacion practica del conocimiento incrementa >=50%

**Metricas:**
- Numero de simuladores completados
- Aplicacion real de conocimiento (gastos vs presupuesto)
- Repeticion de contenido educativo (visualizaciones multiples)

### Hipotesis Especifica 2
Reduccion >=25% en comportamientos de riesgo crediticio

**Metricas:**
- `reduccion_riesgo` en `UserMetrics`
- Numero de alertas de riesgo atendidas
- Cambio en patrones de gasto (mas consistente, menos impulsivo)

---

## CONCLUSIONES

Estas mejoras permitiran:

1. **Diagnosticar** competencias financieras al inicio y durante el estudio
2. **Educar** mediante simuladores practicos contextualizados al Peru
3. **Prevenir** sobreendeudamiento con alertas inteligentes
4. **Evaluar** el impacto con metricas cuantificables
5. **Engagement** sostenido mediante gamificacion avanzada
6. **Personalizar** la experiencia con IA

Todas las propuestas estan alineadas con los objetivos de investigacion y permitiran obtener datos concretos para validar las hipotesis planteadas.



