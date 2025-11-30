from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models.functions import TruncMonth
from datetime import date, timedelta
from collections import defaultdict
import json
import random
import requests
import os
import io
from xhtml2pdf import pisa
from django.template.loader import render_to_string

from .decorators import session_login_required
from .forms import (
    LoginForm, RegisterForm, ExpenseForm, PaymentMethodForm,
    InvestmentForm, UpdateLimitForm
)
from .models import (
    UserProfile, Expense, PaymentMethod, Challenge, UserChallenge,
    Investment, RecommendationVideo, PreguntaTrivia, PuntajeTrivia,
    FraseCompletar, PuntajeCompletarFrases, FinancialCompetencyAssessment,
    UserMetrics, PeriodicAssessment, CreditRiskAlert, EducationalContent,
    Achievement, UserAchievement, Storyline, StoryProgress,
    FraudPreventionContent, PersonalizedRecommendation, UserContext,
    PregeneradaEvaluacion, PregeneradaFraseCompletar
)
from .tokens import custom_token_generator


def generar_evaluacion_completa_en_segundo_plano(user):
    """Genera una evaluación completa en segundo plano y la guarda"""
    try:
        from threading import Thread
        
        def generar_y_guardar():
            try:
                # Generar preguntas para cada categoría
                categorias = ['presupuesto', 'ahorro', 'credito', 'inversiones', 'fraudes']
                todas_preguntas = {}
                
                for categoria in categorias:
                    preguntas = generar_preguntas_evaluacion_ia(categoria, cantidad=10)
                    if preguntas:
                        todas_preguntas[categoria] = preguntas
                    else:
                        todas_preguntas[categoria] = []
                
                # Generar preguntas de brecha teórico-práctica
                preguntas_brecha = obtener_preguntas_brecha_teorico_practica()
                
                # Guardar en la base de datos
                from myapp.models import PregeneradaEvaluacion
                PregeneradaEvaluacion.objects.create(
                    user=user,
                    preguntas_evaluacion=todas_preguntas,
                    preguntas_brecha=preguntas_brecha
                )
            except Exception as e:
                print(f"Error generando evaluación en segundo plano: {str(e)}")
        
        # Ejecutar en un hilo separado
        thread = Thread(target=generar_y_guardar)
        thread.daemon = True
        thread.start()
    except Exception as e:
        print(f"Error iniciando generación en segundo plano: {str(e)}")


def generar_frase_completar_en_segundo_plano(user):
    """Genera una frase para Completar Frases en segundo plano y la guarda"""
    try:
        from threading import Thread
        
        def generar_y_guardar():
            try:
                frase_data = generar_frase_completar_ia()
                if frase_data:
                    from myapp.models import PregeneradaFraseCompletar
                    PregeneradaFraseCompletar.objects.create(
                        user=user,
                        frase_completa=frase_data['frase_completa'],
                        palabra_clave=frase_data['palabra_clave']
                    )
            except Exception as e:
                print(f"Error generando frase en segundo plano: {str(e)}")
        
        # Ejecutar en un hilo separado
        thread = Thread(target=generar_y_guardar)
        thread.daemon = True
        thread.start()
    except Exception as e:
        print(f"Error iniciando generación de frase en segundo plano: {str(e)}")


def generar_preguntas_evaluacion_ia(categoria, cantidad=10):
    """Genera preguntas de evaluación usando IA para una categoría específica"""
    try:
        import google.generativeai as genai
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            return []
        
        genai.configure(api_key=api_key)
        
        # Intentar con diferentes modelos
        modelos_a_probar = ['gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro']
        modelo = None
        
        for modelo_nombre in modelos_a_probar:
            try:
                modelo = genai.GenerativeModel(modelo_nombre)
                break
            except:
                continue
        
        if not modelo:
            return []
        
        # Mapeo de categorías a descripciones
        categorias_desc = {
            'presupuesto': 'Presupuestos y planificación financiera',
            'ahorro': 'Ahorro y gestión de ahorros',
            'credito': 'Crédito, tarjetas de crédito y deudas',
            'inversiones': 'Inversiones y productos financieros',
            'fraudes': 'Fraudes digitales y seguridad financiera'
        }
        
        categoria_desc = categorias_desc.get(categoria, categoria)
        
        prompt = f"""Genera {cantidad} preguntas de opción múltiple sobre {categoria_desc} para una evaluación financiera en Perú.

Requisitos:
- Cada pregunta debe tener 4 opciones (A, B, C, D)
- Solo una opción debe ser correcta
- Las preguntas deben variar en dificultad: 2 muy fáciles, 3 fáciles, 3 intermedias, 2 complicadas
- Las preguntas complicadas deben ser conocimientos que alguien con experiencia en el área sabría
- Contexto: Perú, soles peruanos (S/.), sistema financiero peruano
- Formato: JSON con este formato exacto:
{{
  "preguntas": [
    {{
      "pregunta": "Texto de la pregunta",
      "opciones": {{
        "A": "Opción A",
        "B": "Opción B",
        "C": "Opción C",
        "D": "Opción D"
      }},
      "respuesta_correcta": "A",
      "dificultad": "muy_facil|facil|intermedia|complicada"
    }}
  ]
}}

Responde SOLO con el JSON, sin texto adicional."""

        response = modelo.generate_content(prompt)
        texto_respuesta = response.text.strip()
        
        # Limpiar el texto si tiene markdown
        if texto_respuesta.startswith('```'):
            texto_respuesta = texto_respuesta.split('```')[1]
            if texto_respuesta.startswith('json'):
                texto_respuesta = texto_respuesta[4:]
        texto_respuesta = texto_respuesta.strip()
        
        datos = json.loads(texto_respuesta)
        return datos.get('preguntas', [])
        
    except Exception as e:
        print(f"Error generando preguntas con IA: {str(e)}")
        return []


def generar_preguntas_brecha_teorico_practica_ia(tipo='teorico', cantidad=5):
    """Genera preguntas de brecha teórico-práctica usando IA (4-5 opciones)"""
    try:
        import google.generativeai as genai
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            return []
        
        genai.configure(api_key=api_key)
        
        # Intentar con diferentes modelos
        modelos_a_probar = ['gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro']
        modelo = None
        
        for modelo_nombre in modelos_a_probar:
            try:
                modelo = genai.GenerativeModel(modelo_nombre)
                break
            except:
                continue
        
        if not modelo:
            return []
        
        if tipo == 'teorico':
            descripcion = 'conocimiento teórico sobre finanzas personales'
            instrucciones = 'Las preguntas deben evaluar el conocimiento teórico del usuario sobre conceptos financieros básicos.'
        else:  # practico
            descripcion = 'aplicación práctica de conocimientos financieros'
            instrucciones = 'Las preguntas deben evaluar cómo el usuario aplica sus conocimientos financieros en situaciones reales de su vida diaria.'
        
        prompt = f"""Genera {cantidad} preguntas de opción múltiple sobre {descripcion} para una evaluación financiera en Perú.

Requisitos:
- Cada pregunta debe tener exactamente 4 opciones (A, B, C, D)
- Solo una opción debe ser correcta
- {instrucciones}
- Contexto: Perú, soles peruanos (S/.), sistema financiero peruano
- Las preguntas deben ser claras y directas
- Formato: JSON con este formato exacto:
{{
  "preguntas": [
    {{
      "pregunta": "Texto de la pregunta",
      "opciones": {{
        "A": "Opción A",
        "B": "Opción B",
        "C": "Opción C",
        "D": "Opción D"
      }},
      "respuesta_correcta": "A"
    }}
  ]
}}

Responde SOLO con el JSON, sin texto adicional."""

        response = modelo.generate_content(prompt)
        texto_respuesta = response.text.strip()
        
        # Limpiar el texto si tiene markdown
        if texto_respuesta.startswith('```'):
            texto_respuesta = texto_respuesta.split('```')[1]
            if texto_respuesta.startswith('json'):
                texto_respuesta = texto_respuesta[4:]
        
        datos = json.loads(texto_respuesta)
        return datos.get('preguntas', [])
        
    except Exception as e:
        print(f"Error generando preguntas de brecha teórico-práctica con IA: {str(e)}")
        return []


def obtener_preguntas_brecha_teorico_practica():
    """Genera preguntas de brecha teórico-práctica usando IA (4-5 opciones)"""
    preguntas_teorico = generar_preguntas_brecha_teorico_practica_ia('teorico', cantidad=5)
    preguntas_practico = generar_preguntas_brecha_teorico_practica_ia('practico', cantidad=5)
    
    return {
        'teorico': preguntas_teorico,
        'practico': preguntas_practico
    }


@session_login_required
def evaluaciones_view(request):
    """Vista de lista de todas las evaluaciones del usuario"""
    user = UserProfile.objects.get(id=request.session['user_id'])
    evaluaciones = FinancialCompetencyAssessment.objects.filter(user=user).order_by('-fecha_evaluacion')
    
    return render(request, 'research/evaluaciones.html', {
        'user': user,
        'evaluaciones': evaluaciones,
    })


@session_login_required
def evaluacion_view(request):
    """Vista unificada para tomar evaluaciones (puede tomarse múltiples veces)"""
    user = UserProfile.objects.get(id=request.session['user_id'])
    from myapp.models import PregeneradaEvaluacion
    
    # Intentar obtener evaluación pre-generada
    evaluacion_pregenerada = PregeneradaEvaluacion.objects.filter(
        user=user, 
        usada=False
    ).order_by('fecha_creacion').first()
    
    if evaluacion_pregenerada and not request.GET.get('regenerar') == '1':
        # Usar evaluación pre-generada
        preguntas_evaluacion = evaluacion_pregenerada.preguntas_evaluacion
        preguntas_brecha = evaluacion_pregenerada.preguntas_brecha
        
        # Marcar como usada
        evaluacion_pregenerada.usada = True
        evaluacion_pregenerada.fecha_uso = timezone.now()
        evaluacion_pregenerada.save()
        
        # Generar siguiente evaluación en segundo plano
        generar_evaluacion_completa_en_segundo_plano(user)
    else:
        # Generar en tiempo real si no hay pre-generada o se solicita regenerar
        categorias = ['presupuesto', 'ahorro', 'credito', 'inversiones', 'fraudes']
        todas_preguntas = {}
        
        for categoria in categorias:
            preguntas = generar_preguntas_evaluacion_ia(categoria, cantidad=10)
            if preguntas:
                todas_preguntas[categoria] = preguntas
            else:
                todas_preguntas[categoria] = []
        
        preguntas_brecha = obtener_preguntas_brecha_teorico_practica()
        preguntas_evaluacion = todas_preguntas
        
        # Generar siguiente evaluación en segundo plano
        generar_evaluacion_completa_en_segundo_plano(user)
    
    if request.method == 'POST':
        # Procesar respuestas
        respuestas = {}
        respuestas_brecha_teorico = {}
        respuestas_brecha_practico = {}
        
        # Procesar respuestas de preguntas generadas por IA
        for categoria, preguntas in preguntas_evaluacion.items():
            respuestas_categoria = []
            for idx, pregunta in enumerate(preguntas):
                respuesta_key = f'pregunta_{categoria}_{idx}'
                respuesta = request.POST.get(respuesta_key)
                if respuesta:
                    respuestas_categoria.append({
                        'pregunta_idx': idx,
                        'respuesta': respuesta,
                        'correcta': pregunta.get('respuesta_correcta', '')
                    })
            respuestas[categoria] = respuestas_categoria
        
        # Procesar respuestas de brecha teórico-práctica
        for idx, pregunta in enumerate(preguntas_brecha['teorico']):
            respuesta_key = f'brecha_teorico_{idx}'
            respuesta = request.POST.get(respuesta_key)
            if respuesta:
                respuestas_brecha_teorico[idx] = {
                    'respuesta': respuesta,
                    'correcta': pregunta.get('respuesta_correcta', '')
                }
        
        for idx, pregunta in enumerate(preguntas_brecha['practico']):
            respuesta_key = f'brecha_practico_{idx}'
            respuesta = request.POST.get(respuesta_key)
            if respuesta:
                respuestas_brecha_practico[idx] = respuesta
        
        # Calcular puntajes por categoría
        puntajes_categoria = {}
        for categoria, respuestas_cat in respuestas.items():
            correctas = sum(1 for r in respuestas_cat if r['respuesta'] == r['correcta'])
            total = len(respuestas_cat)
            if total > 0:
                puntaje = 1 + int((correctas / total) * 4)
                puntajes_categoria[categoria] = min(5, max(1, puntaje))
            else:
                puntajes_categoria[categoria] = 1
        
        # Calcular brecha teórico-práctica
        correctas_teorico = sum(1 for idx, r in respuestas_brecha_teorico.items() 
                               if r['respuesta'] == r['correcta'])
        total_teorico = len(respuestas_brecha_teorico)
        conocimiento_teorico = 1 + int((correctas_teorico / total_teorico) * 4) if total_teorico > 0 else 1
        conocimiento_teorico = min(5, max(1, conocimiento_teorico))
        
        # Para práctico: contar respuestas correctas y convertir a escala 1-5
        correctas_practico = 0
        total_practico = len(respuestas_brecha_practico)
        if total_practico > 0:
            for idx, respuesta in respuestas_brecha_practico.items():
                if idx < len(preguntas_brecha['practico']):
                    pregunta_practico = preguntas_brecha['practico'][idx]
                    respuesta_correcta = pregunta_practico.get('respuesta_correcta', '')
                    if respuesta == respuesta_correcta:
                        correctas_practico += 1
            aplicacion_practica = 1 + int((correctas_practico / total_practico) * 4) if total_practico > 0 else 1
        else:
            aplicacion_practica = 3
        aplicacion_practica = min(5, max(1, aplicacion_practica))
        
        # Obtener datos adicionales del formulario
        tiene_tarjetas = request.POST.get('tiene_tarjetas_credito') == 'on'
        cantidad_tarjetas = int(request.POST.get('cantidad_tarjetas', 0) or 0)
        monto_deuda = float(request.POST.get('monto_deuda_actual', 0) or 0)
        frecuencia_pago_minimo = int(request.POST.get('frecuencia_pago_minimo', 0) or 0)
        experiencia_fraude = request.POST.get('experiencia_fraude') == 'on'
        
        # Calcular número de evaluación
        ultima_evaluacion = FinancialCompetencyAssessment.objects.filter(
            user=user
        ).order_by('-numero_evaluacion').first()
        numero_evaluacion = (ultima_evaluacion.numero_evaluacion + 1) if ultima_evaluacion else 1
        
        # Crear nueva evaluación
        assessment = FinancialCompetencyAssessment.objects.create(
            user=user,
            numero_evaluacion=numero_evaluacion,
            conocimiento_presupuesto=puntajes_categoria.get('presupuesto', 1),
            conocimiento_ahorro=puntajes_categoria.get('ahorro', 1),
            conocimiento_credito=puntajes_categoria.get('credito', 1),
            conocimiento_inversiones=puntajes_categoria.get('inversiones', 1),
            conocimiento_fraudes=puntajes_categoria.get('fraudes', 1),
            tiene_tarjetas_credito=tiene_tarjetas,
            cantidad_tarjetas=cantidad_tarjetas,
            monto_deuda_actual=monto_deuda,
            frecuencia_pago_minimo=frecuencia_pago_minimo,
            experiencia_fraude=experiencia_fraude,
            conocimiento_teorico=conocimiento_teorico,
            aplicacion_practica=aplicacion_practica
        )
        
        # Actualizar métricas automáticamente (se hace en el save() del modelo)
        # Pero también lo hacemos aquí para asegurar que se actualice
        metrics, _ = UserMetrics.objects.get_or_create(user=user)
        metrics.actualizar_mejora()  # Esto recalcula todo automáticamente
        metrics.save()
        
        # Generar siguiente evaluación en segundo plano (ya se generó antes, pero por si acaso)
        generar_evaluacion_completa_en_segundo_plano(user)
        
        messages.success(request, f'Evaluación {numero_evaluacion} completada exitosamente. Puntaje: {assessment.puntaje_total} puntos.')
        return redirect('progreso_individual')
    
    return render(request, 'research/evaluacion.html', {
        'preguntas_evaluacion': preguntas_evaluacion,
        'preguntas_brecha': preguntas_brecha,
        'user': user,
    })

# ============================================
# AUTENTICACIÓN Y REGISTRO
# ============================================

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = UserProfile.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    
                    # Las métricas se actualizan automáticamente en el decorator @session_login_required
                    # cuando accede al dashboard, así que no necesitamos actualizarlas aquí
                    
                    return redirect('dashboard')
                else:
                    form.add_error(None, 'Contraseña incorrecta')
            except UserProfile.DoesNotExist:
                form.add_error('email', 'No existe un usuario con este correo electrónico')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.save()
            
            request.session['user_id'] = user.id
            
            try:
                send_mail(
                    subject='🎉 ¡Bienvenido a TuChanchita!',
                    message=f'''Hola {user.first_name},

¡Gracias por registrarte en TuChanchita! 🎊

Ahora puedes comenzar a llevar el control de tus gastos, asumir retos financieros y aprender jugando.

¡Disfruta la experiencia!

El equipo de TuChanchita 💰''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
            
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def solicitar_reset_contrasena(request):
    mensaje = ""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = UserProfile.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = custom_token_generator.make_token(user)
            link = request.build_absolute_uri(f"/resetear/{uid}/{token}/")
            
            send_mail(
                "Recupera tu contraseña",
                f"Haz clic en el siguiente enlace para restablecer tu contraseña:\n{link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            mensaje = "✅ Se ha enviado un enlace a tu correo para restablecer tu contraseña."
        except UserProfile.DoesNotExist:
            mensaje = "❌ No existe un usuario con ese correo."
    
    return render(request, "olvide_contrasena.html", {"mensaje": mensaje})


def resetear_contrasena(request, uidb64, token):
    mensaje = ""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    
    if user is not None and custom_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contrasena = request.POST.get("nueva_contrasena")
            confirmar_contrasena = request.POST.get("confirmar_contrasena")
            
            if nueva_contrasena and nueva_contrasena == confirmar_contrasena:
                user.password = make_password(nueva_contrasena)
                user.save()
                mensaje = "✅ Contraseña restablecida correctamente. Puedes iniciar sesión."
                return redirect("login")
            else:
                mensaje = "❌ Las contraseñas no coinciden."
        return render(request, "resetear_contrasena.html", {"validlink": True, "mensaje": mensaje})
    else:
        return render(request, "resetear_contrasena.html", {"validlink": False})


# ============================================
# DASHBOARD Y PERFIL
# ============================================

@session_login_required
def dashboard_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    hoy = timezone.now()
    inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if hoy.month == 12:
        fin_mes = hoy.replace(year=hoy.year + 1, month=1, day=1)
    else:
        fin_mes = hoy.replace(month=hoy.month + 1, day=1)
    
    ultimos_gastos = Expense.objects.filter(
        user=user,
        date__range=(inicio_mes, fin_mes)
    ).order_by('-date')[:10]
    
    total_gastado = ultimos_gastos.aggregate(Sum('amount'))['amount__sum'] or 0
    cards = PaymentMethod.objects.filter(user=user)
    
    return render(request, 'dashboard.html', {
        'user': user,
        'ultimos_gastos': ultimos_gastos,
        'total_mes': total_gastado,
        'cards': cards,
        'puntos': user.points
    })


@session_login_required
def profile_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    cards = PaymentMethod.objects.filter(user=user)
    return render(request, 'profile.html', {
        'user': user,
        'cards': cards,
        'puntos': user.points
    })


@session_login_required
def upload_profile_photo(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    if request.method == 'POST' and request.FILES.get('photo'):
        if user.photo:
            old_photo_path = os.path.join(settings.MEDIA_ROOT, user.photo.name)
            if os.path.isfile(old_photo_path):
                os.remove(old_photo_path)
        
        user.photo = request.FILES['photo']
        user.save()
        messages.success(request, 'Foto de perfil actualizada correctamente.')
    
    return redirect('profile')


@session_login_required
def update_limit_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    if request.method == 'POST':
        form = UpdateLimitForm(request.POST)
        if form.is_valid():
            nuevo_limite = form.cleaned_data['nuevo_limite']
            user.monthly_limit = nuevo_limite
            user.save()
            messages.success(request, 'Límite actualizado correctamente.')
            return redirect('profile')
    else:
        form = UpdateLimitForm(initial={'nuevo_limite': user.monthly_limit})
    
    return render(request, 'update_limit.html', {'form': form})


@session_login_required
def add_card_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = user
            card.save()
            return redirect('profile')
    else:
        form = PaymentMethodForm()
    return render(request, 'add_card.html', {'form': form})


@session_login_required
def delete_card(request, card_id):
    user = UserProfile.objects.get(id=request.session['user_id'])
    card = get_object_or_404(PaymentMethod, id=card_id, user=user)
    card.delete()
    return redirect('profile')


# ============================================
# GASTOS Y REPORTES
# ============================================

@session_login_required
def register_expense_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=user)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.user = user
            gasto.date = timezone.now()
            gasto.save()
            
            # Verificar y actualizar retos después del gasto
            actualizar_retos_usuario(user)
            
            return redirect('dashboard')
    else:
        form = ExpenseForm(user=user)
    
    return render(request, 'register_expense.html', {'form': form})


@session_login_required
def reports_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    gastos_categoria = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount')).order_by('-total')
    
    resumen = Expense.objects.filter(user=user).annotate(
        mes=TruncMonth('date')
    ).values('mes').annotate(total=Sum('amount')).order_by('mes')
    
    resumen_mensual = [(r['mes'].strftime('%B %Y'), r['total']) for r in resumen]
    
    return render(request, 'reports.html', {
        'user': user,
        'gastos_categoria': gastos_categoria,
        'resumen_mensual': resumen_mensual,
        'today': date.today()
    })


@session_login_required
def export_pdf_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    mes_actual = date.today().strftime('%B %Y')
    fecha_emision = date.today().strftime('%B %d, %Y')
    
    gastos = Expense.objects.filter(
        user=user,
        date__month=date.today().month,
        date__year=date.today().year
    )
    
    html_string = render_to_string("estado_cuenta_pdf.html", {
        'user': user,
        'gastos': gastos,
        'mes_actual': mes_actual,
        'fecha_emision': fecha_emision,
        'total_mes': gastos.aggregate(Sum('amount'))['amount__sum'] or 0,
        'limite': user.monthly_limit,
    })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="estado_cuenta_{user.email}.pdf"'
    
    pisa_status = pisa.CreatePDF(io.StringIO(html_string), dest=response)
    if pisa_status.err:
        return HttpResponse('Hubo un error generando el PDF', status=500)
    
    return response


# ============================================
# RECOMENDACIONES Y CHATBOT
# ============================================

@session_login_required
def recommendations_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    recomendaciones = RecommendationVideo.objects.all()
    return render(request, 'recommendations.html', {'videos': recomendaciones})


def obtener_modelo_gemini():
    """Obtiene un modelo de Gemini funcional, probando diferentes opciones"""
    try:
        import google.generativeai as genai
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            return None
        
        genai.configure(api_key=api_key)
        
        # Lista de modelos a probar en orden de preferencia
        modelos_a_probar = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        for modelo_nombre in modelos_a_probar:
            try:
                modelo = genai.GenerativeModel(modelo_nombre)
                # Probar que el modelo funciona haciendo una prueba simple
                modelo.generate_content("test")
                return modelo
            except Exception as e:
                print(f"Modelo {modelo_nombre} no disponible: {str(e)}")
                continue
        
        return None
    except Exception as e:
        print(f"Error configurando Gemini: {str(e)}")
        return None


@csrf_exempt
@session_login_required
def chatbot_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    if 'chat_historial' not in request.session:
        request.session['chat_historial'] = []
    
    historial = request.session['chat_historial']
    
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        if mensaje:
            historial.append({"pregunta": mensaje})
            
            modelo = obtener_modelo_gemini()
            
            if not modelo:
                respuesta = "El chatbot no está disponible en este momento. Por favor, verifica la configuración de GEMINI_API_KEY en settings."
            else:
                try:
                    # Construir el contexto de la conversación
                    contexto = "Eres un asistente financiero útil especializado en finanzas personales para jóvenes peruanos. Responde de manera clara, concisa y adaptada al contexto peruano (soles, sistema financiero peruano)."
                    
                    # Construir el historial de conversación
                    conversacion = contexto + "\n\n"
                    for h in historial:
                        if 'pregunta' in h:
                            conversacion += f"Usuario: {h['pregunta']}\n"
                        if 'respuesta' in h:
                            conversacion += f"Asistente: {h['respuesta']}\n"
                    
                    # Agregar la nueva pregunta
                    conversacion += f"Usuario: {mensaje}\nAsistente:"
                    
                    # Generar respuesta
                    response = modelo.generate_content(conversacion)
                    respuesta = response.text.strip()
                    
                except Exception as e:
                    print(f"Error generando respuesta con Gemini: {str(e)}")
                    respuesta = "Error al conectarse al asistente. Intenta más tarde."
            
            historial[-1]["respuesta"] = respuesta
            request.session['chat_historial'] = historial
    
    return render(request, 'chatbot.html', {
        'historial': historial,
        'user': user,
    })


# ============================================
# INVERSIONES
# ============================================

@session_login_required
def investment_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    mensaje = ""
    
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            company_symbol = form.cleaned_data['company']
            shares = form.cleaned_data['shares']
            
            api_key = getattr(settings, 'TWELVE_API_KEY', None)
            if api_key:
                try:
                    url = f"https://api.twelvedata.com/price?symbol={company_symbol}&apikey={api_key}"
                    response = requests.get(url).json()
                    price = float(response['price']) if 'price' in response else None
                except Exception as e:
                    price = None
            else:
                price = None
            
            if price is not None:
                investment = Investment.objects.create(
                    user=user,
                    company=dict(form.fields['company'].choices)[company_symbol],
                    symbol=company_symbol,
                    shares=shares,
                    price_at_purchase=price
                )
                mensaje = f"Inversión en {investment.company} registrada exitosamente."
            else:
                mensaje = "No se pudo obtener el precio actual. Intenta más tarde."
    else:
        form = InvestmentForm()
    
    inversiones = Investment.objects.filter(user=user)
    
    return render(request, 'investments.html', {
        'form': form,
        'inversiones': inversiones,
        'mensaje': mensaje
    })


@require_POST
@session_login_required
def delete_investment_view(request, id):
    user = UserProfile.objects.get(id=request.session['user_id'])
    try:
        inversion = Investment.objects.get(id=id, user=user)
    except Investment.DoesNotExist:
        raise Http404("La inversión no existe o no te pertenece.")
    
    inversion.delete()
    return redirect('investments')


# ============================================
# RETOS
# ============================================

def actualizar_retos_usuario(user):
    retos_usuario = UserChallenge.objects.filter(user=user, completed=False, failed=False)
    
    for uc in retos_usuario:
        reto = uc.challenge
        fecha_inicio = uc.start_date
        fecha_fin = fecha_inicio + timedelta(days=reto.duration_days)
        
        if reto.type == 'ahorro':
            total_ahorrado = Expense.objects.filter(
                user=user,
                category__iexact='Ahorro',
                date__range=[fecha_inicio, fecha_fin]
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            if total_ahorrado >= reto.goal_amount:
                uc.completed = True
                uc.earned_points = reto.points
                user.points += reto.points
                user.save()
                uc.save()
            elif timezone.now() > fecha_fin:
                uc.failed = True
                uc.save()
        
        elif reto.type == 'no_gastos':
            total_gastado = Expense.objects.filter(
                user=user,
                date__range=[fecha_inicio, fecha_fin]
            ).exclude(category__iexact='Ahorro').aggregate(Sum('amount'))['amount__sum'] or 0
            
            if total_gastado > reto.goal_amount:
                uc.failed = True
                uc.save()
            elif timezone.now() > fecha_fin:
                uc.completed = True
                uc.earned_points = reto.points
                user.points += reto.points
                user.save()
                uc.save()


@session_login_required
def retos_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    retos_disponibles = Challenge.objects.filter(is_active=True).exclude(type='juego')
    retos_usuario = UserChallenge.objects.filter(user=user)
    
    retos_mostrar = []
    
    for uc in retos_usuario:
        reto = uc.challenge
        fecha_inicio = uc.start_date
        fecha_fin = fecha_inicio + timedelta(days=reto.duration_days)
        
        if uc.completed or uc.failed:
            continue
        
        progreso = 0
        color = '#4caf50'
        
        if reto.type == 'ahorro':
            total_ahorrado = Expense.objects.filter(
                user=user,
                category__iexact='Ahorro',
                date__range=[fecha_inicio, fecha_fin]
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            progreso = int(min((total_ahorrado / reto.goal_amount) * 100, 100)) if reto.goal_amount else 0
            if total_ahorrado >= reto.goal_amount:
                uc.completed = True
                uc.earned_points = reto.points
                user.points += reto.points
                user.save()
                uc.save()
                continue
            elif timezone.now() > fecha_fin:
                uc.failed = True
                uc.save()
                continue
        
        elif reto.type == 'no_gastos':
            total_gastos = Expense.objects.filter(
                user=user,
                date__range=[fecha_inicio, fecha_fin]
            ).exclude(category__iexact='Ahorro').aggregate(Sum('amount'))['amount__sum'] or 0
            
            progreso = int(min((total_gastos / reto.goal_amount) * 100, 100)) if reto.goal_amount else 0
            color = '#ef4444' if total_gastos > 0 else '#4caf50'
            if total_gastos > reto.goal_amount:
                uc.failed = True
                uc.save()
                continue
            elif timezone.now() > fecha_fin:
                uc.completed = True
                uc.earned_points = reto.points
                user.points += reto.points
                user.save()
                uc.save()
                continue
        
        retos_mostrar.append({
            'ur': uc,
            'progreso': progreso,
            'color': color,
        })
    
    if request.method == 'POST':
        reto_id = request.POST.get('reto_id')
        reto = get_object_or_404(Challenge, id=reto_id)
        if not UserChallenge.objects.filter(user=user, challenge=reto).exists():
            UserChallenge.objects.create(user=user, challenge=reto, start_date=timezone.now())
        return redirect('retos')
    
    top_users = UserProfile.objects.order_by('-points')[:5]
    
    return render(request, 'retos.html', {
        'retos': retos_disponibles.exclude(id__in=retos_usuario.values_list('challenge_id', flat=True)),
        'retos_mostrar': retos_mostrar,
        'retos_unidos': retos_usuario.values_list('challenge_id', flat=True),
        'top_users': top_users
    })


@session_login_required
def historial_retos_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    historial = UserChallenge.objects.filter(
        user=user,
    ).filter(
        completed=True
    ) | UserChallenge.objects.filter(
        user=user
    ).filter(
        failed=True
    )
    
    historial = historial.order_by('-start_date')[:10]
    
    datos_historial = []
    for ur in historial:
        tipo = "Ahorro" if ur.challenge.type == "ahorro" else "No gastar"
        estado = "Completado" if ur.completed else "Fallido"
        datos_historial.append({
            'titulo': ur.challenge.title,
            'tipo': tipo,
            'estado': estado,
            'monto': ur.challenge.goal_amount,
            'puntos': ur.earned_points or 0,
            'fecha': ur.start_date.date(),
        })
    
    return render(request, 'historial_retos.html', {
        'datos_historial': datos_historial
    })


# ============================================
# JUEGOS
# ============================================

@session_login_required
def juegos_seleccion_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    # Obtener puntajes de trivia
    puntaje_trivia = user.trivia_puntaje or 0
    
    # Obtener puntaje de completar frases
    try:
        puntaje_completar_obj = PuntajeCompletarFrases.objects.get(user=user)
        puntaje_completar = puntaje_completar_obj.puntaje_total or 0
    except PuntajeCompletarFrases.DoesNotExist:
        puntaje_completar = 0
    
    return render(request, 'juegos_seleccion.html', {
        'puntaje_trivia': puntaje_trivia,
        'puntaje_completar': puntaje_completar,
    })


@csrf_exempt
@session_login_required
def trivia_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    if 'puntos_trivia' not in request.session:
        request.session['puntos_trivia'] = 0
        request.session['fallos_trivia'] = 0
        request.session['preguntas_respondidas'] = []
    
    mensaje = ""
    resultado_audio = ""
    pregunta_actual = None
    opciones = {}
    
    if request.method == 'POST':
        seleccion = request.POST.get('opcion_seleccionada', "").strip().lower()
        pregunta_id = request.session.get('pregunta_actual_id')
        
        try:
            pregunta = PreguntaTrivia.objects.get(id=pregunta_id)
        except PreguntaTrivia.DoesNotExist:
            return redirect('trivia')
        
        if seleccion == pregunta.respuesta_correcta.strip().lower():
            request.session['puntos_trivia'] += 100
            mensaje = "Correcto! Has ganado 100 puntos."
            resultado_audio = "correct"
        else:
            request.session['fallos_trivia'] += 1
            mensaje = ""
            resultado_audio = "incorrect"
        
        if pregunta_id not in request.session['preguntas_respondidas']:
            request.session['preguntas_respondidas'].append(pregunta_id)
        
        if request.session['fallos_trivia'] >= 3:
            puntos_finales = request.session['puntos_trivia']
            if puntos_finales > user.trivia_puntaje:
                user.trivia_puntaje = puntos_finales
                user.save()
            
            puntaje, _ = PuntajeTrivia.objects.get_or_create(user=user)
            puntaje.intentos += 1
            if puntos_finales > puntaje.puntaje_total:
                puntaje.puntaje_total = puntos_finales
            puntaje.save()
            
            request.session['puntos_trivia'] = 0
            request.session['fallos_trivia'] = 0
            request.session['preguntas_respondidas'] = []
            
            return render(request, 'trivia_resultado.html', {
                'puntos': puntos_finales,
                'mensaje': mensaje,
                'resultado_audio': resultado_audio
            })
    
    preguntas_disponibles = PreguntaTrivia.objects.exclude(id__in=request.session['preguntas_respondidas'])
    if preguntas_disponibles.exists():
        pregunta_actual = random.choice(list(preguntas_disponibles))
        request.session['pregunta_actual_id'] = pregunta_actual.id
        opciones = pregunta_actual.opciones
    else:
        mensaje = "🎉 Has respondido todas las preguntas."
        puntos_finales = request.session['puntos_trivia']
        if puntos_finales > user.trivia_puntaje:
            user.trivia_puntaje = puntos_finales
            user.save()
        puntaje, _ = PuntajeTrivia.objects.get_or_create(user=user)
        puntaje.intentos += 1
        if puntos_finales > puntaje.puntaje_total:
            puntaje.puntaje_total = puntos_finales
        puntaje.save()
        
        request.session['puntos_trivia'] = 0
        request.session['fallos_trivia'] = 0
        request.session['preguntas_respondidas'] = []
        
        return render(request, 'trivia_resultado.html', {
            'puntos': puntos_finales,
            'mensaje': mensaje,
            'resultado_audio': "timeout"
        })
    
    return render(request, 'trivia.html', {
        'pregunta': pregunta_actual,
        'opciones': opciones,
        'puntos': request.session.get('puntos_trivia', 0) or 0,
        'fallos': request.session.get('fallos_trivia', 0) or 0,
        'mensaje': mensaje,
        'resultado_audio': resultado_audio
    })


@session_login_required
def ranking_trivia_view(request):
    top_users_queryset = UserProfile.objects.order_by('-trivia_puntaje')[:3]
    top_users = list(top_users_queryset)
    
    while len(top_users) < 3:
        top_users.append(None)
    
    all_users = UserProfile.objects.filter(trivia_puntaje__gt=0).order_by('-trivia_puntaje')
    
    return render(request, 'trivia_ranking.html', {
        'top_users': top_users,
        'all_users': all_users
    })


def generar_frase_completar_ia():
    """Genera una oración/definición económica con IA y extrae una palabra clave"""
    try:
        import google.generativeai as genai
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            return None
        
        genai.configure(api_key=api_key)
        
        # Intentar con diferentes modelos
        modelos_a_probar = ['gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro']
        modelo = None
        
        for modelo_nombre in modelos_a_probar:
            try:
                modelo = genai.GenerativeModel(modelo_nombre)
                break
            except:
                continue
        
        if not modelo:
            return None
        
        prompt = """Genera una oración educativa sobre economía, finanzas, inversiones, fraudes digitales o conceptos financieros. Debe ser una DEFINICIÓN, HECHO o EXPLICACIÓN, no una frase narrativa.

La oración debe cubrir DIVERSOS temas:
- Conceptos de economía general (inflación, oferta, demanda, PIB, etc.)
- Finanzas personales (presupuesto, ahorro, crédito, deudas, etc.)
- Inversiones (acciones, bonos, fondos mutuos, diversificación, etc.)
- Fraudes digitales (phishing, smishing, vishing, estafas online, etc.)
- Conceptos bancarios (cuenta corriente, cuenta de ahorros, depósitos, etc.)
- Seguros y protección financiera
- Planificación financiera
- Conceptos de crédito y préstamos
- Educación financiera general

IMPORTANTE:
- Varía los temas, NO solo siglas peruanas (SUNAT, SBS, IGV)
- Puede ser sobre conceptos universales o contextualizados a Perú
- Tener entre 10 y 25 palabras
- Contener un término clave (concepto, palabra importante o sigla) que se pueda completar
- Usar el género correcto de los artículos
- Ser apropiada para jóvenes de 18-25 años

Ejemplos VARIADOS de buenas oraciones:
- "El interés compuesto permite que el dinero crezca exponencialmente con el tiempo"
- "La diversificación reduce el riesgo al distribuir inversiones en diferentes activos"
- "El phishing es un fraude donde se intenta obtener información personal mediante engaño"
- "Un presupuesto personal ayuda a controlar los gastos y planificar el ahorro"
- "La inflación reduce el poder adquisitivo del dinero con el tiempo"
- "Las acciones representan una participación en la propiedad de una empresa"
- "Un fondo de emergencia debe cubrir entre 3 y 6 meses de gastos básicos"
- "La tasa de interés determina cuánto pagarás por pedir dinero prestado"
- "La diversificación es clave para reducir el riesgo en una cartera de inversiones"
- "El smishing es un fraude que usa mensajes de texto para robar información"

Responde SOLO con JSON en este formato exacto:
{
  "frase_completa": "La oración completa con el término clave incluido",
  "palabra_clave": "el término clave que debe completarse (puede ser una palabra, concepto o sigla)"
}

Ejemplo:
{
  "frase_completa": "El interés compuesto permite que el dinero crezca exponencialmente",
  "palabra_clave": "interés compuesto"
}

Otro ejemplo:
{
  "frase_completa": "El phishing es un fraude donde se intenta obtener información personal mediante engaño",
  "palabra_clave": "phishing"
}

Responde SOLO con el JSON, sin texto adicional."""
        
        response = modelo.generate_content(prompt)
        texto_respuesta = response.text.strip()
        
        # Limpiar el texto si tiene markdown
        if texto_respuesta.startswith('```'):
            texto_respuesta = texto_respuesta.split('```')[1]
            if texto_respuesta.startswith('json'):
                texto_respuesta = texto_respuesta[4:]
        texto_respuesta = texto_respuesta.strip()
        
        datos = json.loads(texto_respuesta)
        
        # Limpiar formato markdown de la frase completa
        frase_completa = datos.get('frase_completa', '')
        # Remover asteriscos, guiones bajos y otros formatos markdown
        frase_completa = frase_completa.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
        # Remover espacios múltiples
        frase_completa = ' '.join(frase_completa.split())
        
        palabra_clave = datos.get('palabra_clave', '')
        # Limpiar formato markdown de la palabra clave también
        palabra_clave = palabra_clave.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
        palabra_clave = palabra_clave.strip()
        
        return {
            'frase_completa': frase_completa,
            'palabra_clave': palabra_clave
        }
        
    except Exception as e:
        print(f"Error generando frase con IA: {str(e)}")
        return None


@session_login_required
def completar_frases_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    if 'puntos_completar_frases' not in request.session:
        request.session['puntos_completar_frases'] = 0
    
    if request.method == 'POST':
        respuesta_usuario = request.POST.get('respuesta', '').strip()
        frase_completa = request.session.get('frase_completa_actual', '')
        palabra_clave = request.session.get('palabra_clave_actual', '')
        
        if not frase_completa or not palabra_clave:
            messages.error(request, 'Error: No se encontró la frase actual. Intenta de nuevo.')
            return redirect('completar_frases')
        
        # Limpiar formato markdown de la frase recuperada ANTES de procesar
        frase_completa = frase_completa.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
        frase_completa = ' '.join(frase_completa.split())
        
        # Asegurarse de que no tenga guiones (por si acaso se guardó con guiones)
        if "______________________" in frase_completa:
            frase_completa = frase_completa.replace("______________________", palabra_clave)
        
        # Verificar respuesta con IA
        resultado = verificar_respuesta_ia(palabra_clave, respuesta_usuario)
        
        puntos = 0
        if resultado['es_correcta']:
            puntos = 5
        elif resultado['es_similar']:
            puntos = 2
        
        request.session['puntos_completar_frases'] += puntos
        
        # Guardar puntaje en BD
        puntaje, _ = PuntajeCompletarFrases.objects.get_or_create(user=user)
        puntaje.puntaje_total += puntos
        if resultado['es_correcta']:
            puntaje.respuestas_correctas += 1
        elif resultado['es_similar']:
            puntaje.respuestas_parciales += 1
        else:
            puntaje.respuestas_incorrectas += 1
        puntaje.frases_completadas += 1
        puntaje.save()
        
        # Asegurarse de que la frase completa tenga la palabra correcta (no los guiones)
        # La frase_completa ya viene con la palabra correcta, pero por si acaso la reemplazamos
        frase_completa_mostrar = frase_completa
        if "______________________" in frase_completa_mostrar:
            frase_completa_mostrar = frase_completa_mostrar.replace("______________________", palabra_clave)
        
        # Limpiar formato markdown si existe
        frase_completa_mostrar = frase_completa_mostrar.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
        frase_completa_mostrar = ' '.join(frase_completa_mostrar.split())
        
        # Limpiar frase actual de la sesión
        if 'frase_completa_actual' in request.session:
            del request.session['frase_completa_actual']
        if 'palabra_clave_actual' in request.session:
            del request.session['palabra_clave_actual']
        
        # Generar siguiente frase en segundo plano
        generar_frase_completar_en_segundo_plano(user)
        
        return render(request, 'completar_frases.html', {
            'respuesta_usuario': respuesta_usuario,
            'resultado': resultado,
            'puntos': puntos,
            'puntos_totales': request.session['puntos_completar_frases'],
            'frase_completa_mostrar': frase_completa_mostrar,  # Frase completa con palabra correcta, sin markdown
            'palabra_clave': palabra_clave,
            'mostrar_resultado': True
        })
    
    # Intentar obtener frase pre-generada
    from myapp.models import PregeneradaFraseCompletar
    frase_pregenerada = PregeneradaFraseCompletar.objects.filter(
        user=user,
        usada=False
    ).order_by('fecha_creacion').first()
    
    if frase_pregenerada:
        # Usar frase pre-generada
        frase_completa = frase_pregenerada.frase_completa
        palabra_clave = frase_pregenerada.palabra_clave
        
        # Marcar como usada
        frase_pregenerada.usada = True
        frase_pregenerada.fecha_uso = timezone.now()
        frase_pregenerada.save()
        
        # Generar siguiente frase en segundo plano
        generar_frase_completar_en_segundo_plano(user)
    else:
        # Generar en tiempo real si no hay pre-generada
        frase_data = generar_frase_completar_ia()
        
        if not frase_data:
            messages.error(request, 'Error al generar frase. Intenta más tarde.')
            return redirect('juegos')
        
        frase_completa = frase_data['frase_completa']
        palabra_clave = frase_data['palabra_clave']
        
        # Asegurarse de que la frase completa esté limpia (sin markdown)
        # Ya viene limpia de generar_frase_completar_ia, pero por si acaso
        frase_completa = frase_completa.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
        frase_completa = ' '.join(frase_completa.split())
        
        # Generar siguiente frase en segundo plano
        generar_frase_completar_en_segundo_plano(user)
    
    # Guardar en sesión la versión limpia (sin guiones, con la palabra completa)
    request.session['frase_completa_actual'] = frase_completa
    request.session['palabra_clave_actual'] = palabra_clave
    
    # Crear frase con espacio en blanco para mostrar (usar la versión limpia)
    frase_con_espacio = frase_completa.replace(palabra_clave, "______________________")
    
    return render(request, 'completar_frases.html', {
        'frase_con_espacio': frase_con_espacio,
        'puntos_totales': request.session.get('puntos_completar_frases', 0),
        'mostrar_resultado': False
    })


def verificar_respuesta_ia(palabra_correcta, respuesta_usuario):
    """Verifica si la respuesta del usuario es correcta usando IA"""
    try:
        import google.generativeai as genai
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            return verificar_respuesta_simple(palabra_correcta, respuesta_usuario)
        
        genai.configure(api_key=api_key)
        
        # Intentar con diferentes modelos (sistema de fallback)
        modelos_a_probar = ['gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        modelo = None
        
        for modelo_nombre in modelos_a_probar:
            try:
                modelo = genai.GenerativeModel(modelo_nombre)
                # Probar que el modelo funciona
                modelo.generate_content("test")
                break
            except Exception as e:
                print(f"Modelo {modelo_nombre} no disponible: {str(e)}")
                continue
        
        if not modelo:
            return verificar_respuesta_simple(palabra_correcta, respuesta_usuario)
        
        prompt = f"""Evalúa si la respuesta del usuario es correcta para completar una oración de economía.

Palabra correcta esperada: "{palabra_correcta}"
Respuesta del usuario: "{respuesta_usuario}"

Responde SOLO con JSON en este formato:
{{
  "es_correcta": true/false,
  "es_similar": true/false,
  "explicacion": "breve explicación"
}}

Criterios:
- es_correcta: true si la respuesta es exactamente correcta, equivalente o sinónimo directo (ej: "TEA" = "Tasa Efectiva Anual", o viceversa)
- es_similar: true SOLO si la respuesta está CERCA en significado o es un concepto relacionado que tiene sentido en el contexto (ej: "interés" cuando la respuesta correcta es "interés compuesto", o "ahorro" cuando es "fondo de emergencia")
- es_similar: false si la respuesta está completamente equivocada, no tiene relación o es un concepto diferente
- es_similar debe ser false si es_correcta es true
- NO consideres errores de ortografía o escritura como "similar", solo evalúa el significado y cercanía conceptual

Ejemplos:
- Palabra correcta: "TEA", Usuario: "Tasa Efectiva Anual" → es_correcta: true
- Palabra correcta: "Tasa Efectiva Anual", Usuario: "TEA" → es_correcta: true
- Palabra correcta: "interés compuesto", Usuario: "interés" → es_similar: true (cerca en significado)
- Palabra correcta: "IGV", Usuario: "impuesto general a las ventas" → es_correcta: true (equivalente)
- Palabra correcta: "fondo de emergencia", Usuario: "ahorro" → es_similar: true (relacionado)
- Palabra correcta: "TEA", Usuario: "IGV" → es_correcta: false, es_similar: false (diferente concepto)"""
        
        response = modelo.generate_content(prompt)
        texto = response.text.strip()
        
        if texto.startswith('```'):
            texto = texto.split('```')[1]
            if texto.startswith('json'):
                texto = texto[4:]
        texto = texto.strip()
        
        resultado = json.loads(texto)
        return {
            'es_correcta': resultado.get('es_correcta', False),
            'es_similar': resultado.get('es_similar', False),
            'explicacion': resultado.get('explicacion', '')
        }
    except Exception as e:
        print(f"Error verificando respuesta con IA: {e}")
        return verificar_respuesta_simple(palabra_correcta, respuesta_usuario)


def verificar_respuesta_simple(palabra_correcta, respuesta_usuario):
    """Verificación simple sin IA"""
    palabra_lower = palabra_correcta.lower().strip()
    respuesta_lower = respuesta_usuario.lower().strip()
    
    if palabra_lower == respuesta_lower:
        return {'es_correcta': True, 'es_similar': False, 'explicacion': 'Respuesta correcta'}
    elif palabra_lower in respuesta_lower or respuesta_lower in palabra_lower:
        return {'es_correcta': False, 'es_similar': True, 'explicacion': 'Respuesta parcialmente correcta'}
    else:
        return {'es_correcta': False, 'es_similar': False, 'explicacion': 'Respuesta incorrecta'}


@session_login_required
def ranking_completar_frases_view(request):
    top_users_queryset = PuntajeCompletarFrases.objects.order_by('-puntaje_total')[:3]
    top_users = list(top_users_queryset)
    
    while len(top_users) < 3:
        top_users.append(None)
    
    all_users = PuntajeCompletarFrases.objects.filter(puntaje_total__gt=0).order_by('-puntaje_total')
    
    return render(request, 'completar_frases_ranking.html', {
        'top_users': top_users,
        'all_users': all_users
    })


# ============================================
# VISTAS DE INVESTIGACIÓN (Placeholders - necesitan implementación completa)
# ============================================

@session_login_required
def evaluacion_inicial_view(request):
    # Redirigir a la vista unificada de evaluación
    return redirect('evaluacion_view')


@session_login_required
def evaluacion_periodica_view(request):
    # Redirigir a la vista unificada de evaluación
    return redirect('evaluacion_view')


@session_login_required
def progreso_individual_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    metrics, _ = UserMetrics.objects.get_or_create(user=user)
    
    # Obtener historial de evaluaciones
    evaluaciones = FinancialCompetencyAssessment.objects.filter(
        user=user
    ).order_by('-numero_evaluacion', '-fecha_evaluacion')
    
    # ACTUALIZAR MÉTRICAS DESDE EVALUACIONES REALES antes de mostrar
    # Esto asegura que los valores siempre estén sincronizados
    metrics.actualizar_mejora()
    metrics.save()
    
    # Calcular estadísticas adicionales
    gasto_actual = 0
    ahorro_actual = 0
    if evaluaciones.exists():
        # Obtener gastos y ahorros del mes actual
        from datetime import datetime
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        
        gastos_mes = Expense.objects.filter(
            user=user,
            date__month=mes_actual,
            date__year=anio_actual
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Calcular ahorro (ingresos - gastos) - simplificado
        gasto_actual = gastos_mes
        ahorro_actual = user.monthly_limit - gasto_actual if user.monthly_limit > 0 else 0
    
    # Obtener primera evaluación para comparaciones
    assessment_inicial = evaluaciones.filter(numero_evaluacion=1).first()
    brecha_inicial = 0
    if assessment_inicial:
        brecha_inicial = assessment_inicial.calcular_brecha_teorico_practica()
    
    # Obtener evaluación más reciente (última) para brecha actual
    assessment_actual = evaluaciones.first()  # Ya está ordenado por -numero_evaluacion, -fecha_evaluacion
    brecha_actual = 0
    if assessment_actual:
        brecha_actual = assessment_actual.calcular_brecha_teorico_practica()
    
    return render(request, 'research/progreso_individual.html', {
        'user': user,
        'metrics': metrics,
        'evaluaciones': evaluaciones,
        'assessment_inicial': assessment_inicial,
        'brecha_inicial': brecha_inicial,
        'assessment_actual': assessment_actual,
        'brecha_actual': brecha_actual,
        'gasto_actual': gasto_actual,
        'ahorro_actual': ahorro_actual,
    })


@session_login_required
def recomendaciones_personalizadas_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    recomendaciones = PersonalizedRecommendation.objects.filter(user=user).order_by('-fecha_recomendacion')
    
    return render(request, 'research/recomendaciones_personalizadas.html', {
        'user': user,
        'recomendaciones': recomendaciones,
    })


@session_login_required
def marcar_recomendacion_vista(request, recomendacion_id):
    user = UserProfile.objects.get(id=request.session['user_id'])
    recomendacion = get_object_or_404(PersonalizedRecommendation, id=recomendacion_id, user=user)
    recomendacion.vista = True
    recomendacion.save()
    return redirect('recomendaciones_personalizadas')


@session_login_required
def alertas_riesgo_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    alertas = CreditRiskAlert.objects.filter(user=user).order_by('-fecha_alerta')
    return render(request, 'research/alertas_riesgo.html', {
        'user': user,
        'alertas': alertas,
    })


@session_login_required
def biblioteca_educativa_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    contenidos = EducationalContent.objects.filter(is_active=True)
    
    # Filtros
    q = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    tipo = request.GET.get('tipo', '')
    
    if q:
        contenidos = contenidos.filter(titulo__icontains=q) | contenidos.filter(descripcion__icontains=q)
    if categoria:
        contenidos = contenidos.filter(categoria=categoria)
    if tipo:
        contenidos = contenidos.filter(tipo_contenido=tipo)
    
    # Obtener recomendaciones personalizadas (primeros 3)
    contenido_recomendado = contenidos[:3] if contenidos.exists() else []
    
    return render(request, 'research/biblioteca_educativa.html', {
        'user': user,
        'contenidos': contenidos,
        'contenido_recomendado': contenido_recomendado,
        'categorias': EducationalContent.CATEGORIA_CHOICES,
        'tipos': EducationalContent.TIPO_CONTENIDO_CHOICES,
    })


@session_login_required
def ver_contenido_view(request, contenido_id):
    user = UserProfile.objects.get(id=request.session['user_id'])
    contenido = get_object_or_404(EducationalContent, id=contenido_id, is_active=True)
    contenido.visualizaciones += 1
    contenido.save()
    return render(request, 'research/ver_contenido.html', {
        'user': user,
        'contenido': contenido,
    })


@session_login_required
def logros_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    logros = Achievement.objects.filter(is_active=True)
    logros_usuario_ids = UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
    
    # Separar logros desbloqueados y bloqueados
    logros_desbloqueados = logros.filter(id__in=logros_usuario_ids)
    logros_bloqueados = logros.exclude(id__in=logros_usuario_ids)
    
    total_logros = logros.count()
    logros_completados = logros_desbloqueados.count()
    porcentaje_completado = int((logros_completados / total_logros * 100)) if total_logros > 0 else 0
    
    return render(request, 'research/logros.html', {
        'user': user,
        'logros_desbloqueados': logros_desbloqueados,
        'logros_bloqueados': logros_bloqueados,
        'total_logros': total_logros,
        'logros_completados': logros_completados,
        'porcentaje_completado': porcentaje_completado,
    })


@session_login_required
def narrativa_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    capitulos = Storyline.objects.filter(is_active=True).order_by('capitulo_numero')
    
    # Crear lista con progreso de cada capítulo
    capitulos_con_progreso = []
    for capitulo in capitulos:
        progreso, created = StoryProgress.objects.get_or_create(
            user=user,
            storyline=capitulo,
            defaults={'desbloqueado': capitulo.capitulo_numero == 1}  # Primer capítulo desbloqueado por defecto
        )
        # Desbloquear capítulos anteriores si están completados
        if capitulo.capitulo_numero > 1:
            capitulo_anterior = Storyline.objects.filter(
                capitulo_numero=capitulo.capitulo_numero - 1,
                is_active=True
            ).first()
            if capitulo_anterior:
                progreso_anterior, _ = StoryProgress.objects.get_or_create(
                    user=user,
                    storyline=capitulo_anterior
                )
                if progreso_anterior.completado:
                    progreso.desbloqueado = True
                    progreso.save()
        
        capitulos_con_progreso.append({
            'capitulo': capitulo,
            'progreso': progreso
        })
    
    return render(request, 'research/narrativa.html', {
        'user': user,
        'capitulos_con_progreso': capitulos_con_progreso,
    })


@session_login_required
def ver_capitulo_view(request, capitulo_id):
    user = UserProfile.objects.get(id=request.session['user_id'])
    capitulo = get_object_or_404(Storyline, id=capitulo_id, is_active=True)
    return render(request, 'research/ver_capitulo.html', {
        'user': user,
        'capitulo': capitulo,
    })


@session_login_required
def completar_capitulo_view(request, capitulo_id):
    user = UserProfile.objects.get(id=request.session['user_id'])
    capitulo = get_object_or_404(Storyline, id=capitulo_id)
    
    progress, created = StoryProgress.objects.get_or_create(user=user, storyline=capitulo)
    if not progress.completado:
        progress.completado = True
        progress.fecha_completado = timezone.now()
        progress.save()
        user.points += 50
        user.save()
    
    return redirect('narrativa')


@session_login_required
def admin_dashboard_view(request):
    """Vista personalizada de administración"""
    from django.contrib.auth.models import User
    from django.db.models import Count, Sum
    
    user = UserProfile.objects.get(id=request.session['user_id'])
    
    # Verificar que el usuario sea admin
    django_user = User.objects.filter(email=user.email).first()
    if not django_user or (not django_user.is_staff and not django_user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder al panel de administración.')
        return redirect('dashboard')
    
    # Estadísticas generales
    total_usuarios = UserProfile.objects.count()
    usuarios_activos = UserProfile.objects.filter(is_blocked=False).count()
    total_evaluaciones = FinancialCompetencyAssessment.objects.count()
    
    # Gasto promedio de todos los usuarios
    gastos_por_usuario = Expense.objects.values('user').annotate(total=Sum('amount'))
    if gastos_por_usuario.exists():
        gasto_promedio = sum(g['total'] for g in gastos_por_usuario) / len(gastos_por_usuario)
    else:
        gasto_promedio = 0
    
    # Obtener todos los usuarios con sus métricas
    usuarios = UserProfile.objects.all().select_related('metrics').prefetch_related('competency_assessments').order_by('-id')
    
    return render(request, 'admin/dashboard.html', {
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'total_evaluaciones': total_evaluaciones,
        'gasto_promedio': gasto_promedio,
        'usuarios': usuarios,
    })


@session_login_required
def admin_editar_usuario_view(request, usuario_id):
    """Vista para editar un usuario desde el admin"""
    from django.contrib.auth.models import User
    from django.utils.dateparse import parse_datetime
    
    admin_user = UserProfile.objects.get(id=request.session['user_id'])
    
    # Verificar que el usuario sea admin
    django_user = User.objects.filter(email=admin_user.email).first()
    if not django_user or (not django_user.is_staff and not django_user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder al panel de administración.')
        return redirect('dashboard')
    
    usuario = get_object_or_404(UserProfile, id=usuario_id)
    
    if request.method == 'POST':
        # Actualizar campos del usuario
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.monthly_limit = float(request.POST.get('monthly_limit', usuario.monthly_limit))
        usuario.points = int(request.POST.get('points', usuario.points))
        usuario.trivia_puntaje = int(request.POST.get('trivia_puntaje', usuario.trivia_puntaje))
        usuario.is_blocked = request.POST.get('is_blocked') == 'on'
        usuario.login_attempts = int(request.POST.get('login_attempts', usuario.login_attempts))
        usuario.save()
        
        # Actualizar métricas si existen
        metrics, created = UserMetrics.objects.get_or_create(user=usuario)
        if request.POST.get('fecha_registro'):
            try:
                fecha_registro = parse_datetime(request.POST.get('fecha_registro'))
                if fecha_registro:
                    metrics.fecha_registro = fecha_registro
            except:
                pass
        
        metrics.dias_activos = int(request.POST.get('dias_activos', metrics.dias_activos))
        metrics.sesiones_totales = int(request.POST.get('sesiones_totales', metrics.sesiones_totales))
        # Los puntajes se pueden editar manualmente, pero la mejora se recalcula automáticamente
        if request.POST.get('puntaje_competencia_inicial'):
            metrics.puntaje_competencia_inicial = int(request.POST.get('puntaje_competencia_inicial'))
        if request.POST.get('puntaje_competencia_actual'):
            metrics.puntaje_competencia_actual = int(request.POST.get('puntaje_competencia_actual'))
        
        # Recalcular mejora automáticamente basándose en evaluaciones reales
        # Esto sobrescribe cualquier valor manual y usa las evaluaciones reales
        metrics.actualizar_mejora()
        metrics.gasto_promedio_mensual_inicial = float(request.POST.get('gasto_promedio_mensual_inicial', metrics.gasto_promedio_mensual_inicial))
        metrics.gasto_promedio_mensual_actual = float(request.POST.get('gasto_promedio_mensual_actual', metrics.gasto_promedio_mensual_actual))
        metrics.reduccion_gasto = float(request.POST.get('reduccion_gasto', metrics.reduccion_gasto))
        metrics.ahorro_promedio_mensual_inicial = float(request.POST.get('ahorro_promedio_mensual_inicial', metrics.ahorro_promedio_mensual_inicial))
        metrics.ahorro_promedio_mensual_actual = float(request.POST.get('ahorro_promedio_mensual_actual', metrics.ahorro_promedio_mensual_actual))
        metrics.aumento_ahorro = float(request.POST.get('aumento_ahorro', metrics.aumento_ahorro))
        metrics.puntos_totales = int(request.POST.get('puntos_totales', metrics.puntos_totales))
        metrics.retos_completados = int(request.POST.get('retos_completados', metrics.retos_completados))
        metrics.trivias_completadas = int(request.POST.get('trivias_completadas', metrics.trivias_completadas))
        metrics.nivel_actual = int(request.POST.get('nivel_actual', metrics.nivel_actual))
        metrics.save()
        
        # Actualizar evaluaciones si se proporcionan
        # Extraer IDs únicos de evaluaciones (formato: eval_ID_campo)
        evaluaciones_ids = set()
        for key in request.POST.keys():
            if key.startswith('eval_') and '_' in key:
                parts = key.split('_')
                if len(parts) >= 2:
                    try:
                        eval_id = int(parts[1])  # El ID está en la segunda parte
                        evaluaciones_ids.add(eval_id)
                    except ValueError:
                        continue
        
        for eval_id in evaluaciones_ids:
            try:
                evaluacion = FinancialCompetencyAssessment.objects.get(id=eval_id, user=usuario)
                if request.POST.get(f'eval_{eval_id}_fecha'):
                    try:
                        fecha_eval = parse_datetime(request.POST.get(f'eval_{eval_id}_fecha'))
                        if fecha_eval:
                            evaluacion.fecha_evaluacion = fecha_eval
                    except:
                        pass
                if request.POST.get(f'eval_{eval_id}_numero'):
                    evaluacion.numero_evaluacion = int(request.POST.get(f'eval_{eval_id}_numero'))
                if request.POST.get(f'eval_{eval_id}_nivel'):
                    evaluacion.nivel_competencia = request.POST.get(f'eval_{eval_id}_nivel')
                # Calcular puntajes basados en respuestas correctas (0-10 preguntas por categoría)
                # Fórmula: puntaje = 1 + int((correctas / 10) * 4), luego min(5, max(1, puntaje))
                if request.POST.get(f'eval_{eval_id}_presupuesto_correctas'):
                    correctas = int(request.POST.get(f'eval_{eval_id}_presupuesto_correctas'))
                    puntaje = 1 + int((correctas / 10) * 4)
                    evaluacion.conocimiento_presupuesto = min(5, max(1, puntaje))
                if request.POST.get(f'eval_{eval_id}_ahorro_correctas'):
                    correctas = int(request.POST.get(f'eval_{eval_id}_ahorro_correctas'))
                    puntaje = 1 + int((correctas / 10) * 4)
                    evaluacion.conocimiento_ahorro = min(5, max(1, puntaje))
                if request.POST.get(f'eval_{eval_id}_credito_correctas'):
                    correctas = int(request.POST.get(f'eval_{eval_id}_credito_correctas'))
                    puntaje = 1 + int((correctas / 10) * 4)
                    evaluacion.conocimiento_credito = min(5, max(1, puntaje))
                if request.POST.get(f'eval_{eval_id}_inversiones_correctas'):
                    correctas = int(request.POST.get(f'eval_{eval_id}_inversiones_correctas'))
                    puntaje = 1 + int((correctas / 10) * 4)
                    evaluacion.conocimiento_inversiones = min(5, max(1, puntaje))
                if request.POST.get(f'eval_{eval_id}_fraudes_correctas'):
                    correctas = int(request.POST.get(f'eval_{eval_id}_fraudes_correctas'))
                    puntaje = 1 + int((correctas / 10) * 4)
                    evaluacion.conocimiento_fraudes = min(5, max(1, puntaje))
                # Calcular brecha teórico-práctica basado en respuestas correctas (0-5 preguntas)
                if request.POST.get(f'eval_{eval_id}_teorico_correctas'):
                    correctas_teorico = int(request.POST.get(f'eval_{eval_id}_teorico_correctas'))
                    puntaje = 1 + int((correctas_teorico / 5) * 4) if correctas_teorico > 0 else 1
                    evaluacion.conocimiento_teorico = min(5, max(1, puntaje))
                if request.POST.get(f'eval_{eval_id}_practico_correctas'):
                    correctas_practico = int(request.POST.get(f'eval_{eval_id}_practico_correctas'))
                    puntaje = 1 + int((correctas_practico / 5) * 4) if correctas_practico > 0 else 1
                    evaluacion.aplicacion_practica = min(5, max(1, puntaje))
                
                # Recalcular puntaje total usando la fórmula
                evaluacion.save()  # Esto recalculará el puntaje_total y actualizará métricas automáticamente
            except FinancialCompetencyAssessment.DoesNotExist:
                pass
        
        # Recalcular mejora porcentual para el usuario después de actualizar evaluaciones
        try:
            metrics, _ = UserMetrics.objects.get_or_create(user=usuario)
            metrics.actualizar_mejora()
            metrics.save()
        except:
            pass
        
        # Actualizar gastos
        gastos_ids = set()
        for key in request.POST.keys():
            if key.startswith('gasto_') and '_' in key:
                parts = key.split('_')
                if len(parts) >= 2:
                    try:
                        gasto_id = int(parts[1])
                        gastos_ids.add(gasto_id)
                    except ValueError:
                        continue
        
        for gasto_id in gastos_ids:
            try:
                gasto = Expense.objects.get(id=gasto_id, user=usuario)
                if request.POST.get(f'gasto_{gasto_id}_amount'):
                    gasto.amount = float(request.POST.get(f'gasto_{gasto_id}_amount'))
                if request.POST.get(f'gasto_{gasto_id}_category'):
                    gasto.category = request.POST.get(f'gasto_{gasto_id}_category')
                if request.POST.get(f'gasto_{gasto_id}_store_name'):
                    gasto.store_name = request.POST.get(f'gasto_{gasto_id}_store_name')
                if request.POST.get(f'gasto_{gasto_id}_date'):
                    try:
                        fecha_gasto = parse_datetime(request.POST.get(f'gasto_{gasto_id}_date'))
                        if fecha_gasto:
                            gasto.date = fecha_gasto
                    except:
                        pass
                gasto.save()
            except Expense.DoesNotExist:
                pass
        
        # Actualizar retos completados
        retos_ids = set()
        for key in request.POST.keys():
            if key.startswith('reto_') and '_' in key:
                parts = key.split('_')
                if len(parts) >= 2:
                    try:
                        reto_id = int(parts[1])
                        retos_ids.add(reto_id)
                    except ValueError:
                        continue
        
        for reto_id in retos_ids:
            try:
                reto = UserChallenge.objects.get(id=reto_id, user=usuario)
                if request.POST.get(f'reto_{reto_id}_completed'):
                    reto.completed = request.POST.get(f'reto_{reto_id}_completed') == 'on'
                if request.POST.get(f'reto_{reto_id}_failed'):
                    reto.failed = request.POST.get(f'reto_{reto_id}_failed') == 'on'
                if request.POST.get(f'reto_{reto_id}_earned_points'):
                    reto.earned_points = int(request.POST.get(f'reto_{reto_id}_earned_points'))
                if request.POST.get(f'reto_{reto_id}_start_date'):
                    try:
                        fecha_reto = parse_datetime(request.POST.get(f'reto_{reto_id}_start_date'))
                        if fecha_reto:
                            reto.start_date = fecha_reto
                    except:
                        pass
                reto.save()
            except UserChallenge.DoesNotExist:
                pass
        
        # Actualizar puntajes de juegos
        try:
            puntaje_trivia, _ = PuntajeTrivia.objects.get_or_create(user=usuario)
            if request.POST.get('trivia_puntaje_total'):
                puntaje_trivia.puntaje_total = int(request.POST.get('trivia_puntaje_total'))
            if request.POST.get('trivia_intentos'):
                puntaje_trivia.intentos = int(request.POST.get('trivia_intentos'))
            puntaje_trivia.save()
        except:
            pass
        
        try:
            puntaje_completar, _ = PuntajeCompletarFrases.objects.get_or_create(user=usuario)
            if request.POST.get('completar_puntaje_total'):
                puntaje_completar.puntaje_total = int(request.POST.get('completar_puntaje_total'))
            if request.POST.get('completar_frases_completadas'):
                puntaje_completar.frases_completadas = int(request.POST.get('completar_frases_completadas'))
            if request.POST.get('completar_respuestas_correctas'):
                puntaje_completar.respuestas_correctas = int(request.POST.get('completar_respuestas_correctas'))
            if request.POST.get('completar_respuestas_parciales'):
                puntaje_completar.respuestas_parciales = int(request.POST.get('completar_respuestas_parciales'))
            if request.POST.get('completar_respuestas_incorrectas'):
                puntaje_completar.respuestas_incorrectas = int(request.POST.get('completar_respuestas_incorrectas'))
            puntaje_completar.save()
        except:
            pass
        
        messages.success(request, f'Usuario {usuario.email} actualizado exitosamente.')
        return redirect('admin_editar_usuario', usuario_id=usuario_id)
    
    # Obtener métricas y evaluaciones
    metrics, _ = UserMetrics.objects.get_or_create(user=usuario)
    evaluaciones = FinancialCompetencyAssessment.objects.filter(user=usuario).order_by('-numero_evaluacion')
    
    # Obtener gastos
    gastos = Expense.objects.filter(user=usuario).order_by('-date')[:50]  # Últimos 50 gastos
    
    # Obtener retos
    retos = UserChallenge.objects.filter(user=usuario).order_by('-start_date')
    
    # Obtener puntajes de juegos
    puntaje_trivia, _ = PuntajeTrivia.objects.get_or_create(user=usuario)
    puntaje_completar, _ = PuntajeCompletarFrases.objects.get_or_create(user=usuario)
    
    # Calcular respuestas correctas estimadas para cada evaluación
    evaluaciones_con_correctas = []
    for eval in evaluaciones:
        # Fórmula inversa: puntaje = 1 + int((correctas / total) * 4)
        # correctas = ((puntaje - 1) / 4) * total
        def calcular_correctas(puntaje, total=10):
            if puntaje <= 1:
                return 0
            return round(((puntaje - 1) / 4) * total)
        
        def calcular_correctas_brecha(puntaje, total=5):
            if puntaje <= 1:
                return 0
            return round(((puntaje - 1) / 4) * total)
        
        eval_data = {
            'eval': eval,
            'presupuesto_correctas': calcular_correctas(eval.conocimiento_presupuesto),
            'ahorro_correctas': calcular_correctas(eval.conocimiento_ahorro),
            'credito_correctas': calcular_correctas(eval.conocimiento_credito),
            'inversiones_correctas': calcular_correctas(eval.conocimiento_inversiones),
            'fraudes_correctas': calcular_correctas(eval.conocimiento_fraudes),
            'teorico_correctas': calcular_correctas_brecha(eval.conocimiento_teorico),
            'practico_correctas': calcular_correctas_brecha(eval.aplicacion_practica),
        }
        evaluaciones_con_correctas.append(eval_data)
    
    return render(request, 'admin/editar_usuario.html', {
        'usuario': usuario,
        'metrics': metrics,
        'evaluaciones_con_correctas': evaluaciones_con_correctas,
        'gastos': gastos,
        'retos': retos,
        'puntaje_trivia': puntaje_trivia,
        'puntaje_completar': puntaje_completar,
    })


@session_login_required
def prevencion_fraudes_view(request):
    user = UserProfile.objects.get(id=request.session['user_id'])
    contenidos = FraudPreventionContent.objects.filter(is_active=True).order_by('fecha_creacion')
    
    # Filtro por tipo de fraude
    tipo_filtro = request.GET.get('tipo', '')
    if tipo_filtro:
        contenidos = contenidos.filter(tipo_fraude=tipo_filtro)
    
    return render(request, 'research/prevencion_fraudes.html', {
        'user': user,
        'contenidos': contenidos,
        'tipos_fraude': FraudPreventionContent.TIPO_FRAUDE_CHOICES,
    })


@session_login_required
def ver_fraude_view(request, fraude_id):
    user = UserProfile.objects.get(id=request.session['user_id'])
    fraude = get_object_or_404(FraudPreventionContent, id=fraude_id, is_active=True)
    fraude.visualizaciones += 1
    fraude.save()
    return render(request, 'research/ver_fraude.html', {
        'user': user,
        'fraude': fraude,
    })


@session_login_required
def reporte_impacto_admin_view(request):
    # Esta vista es para administradores - necesita verificación de permisos
    metrics = UserMetrics.objects.all().order_by('-mejora_porcentual')
    return render(request, 'research/reporte_impacto_admin.html', {
        'metrics': metrics,
    })
