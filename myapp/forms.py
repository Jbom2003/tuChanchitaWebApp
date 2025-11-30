from django import forms
from .models import UserProfile
from django import forms
from .models import PaymentMethod
import re
import requests

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['tipo', 'sistema_de_pago', 'banco', 'ultimos_4_digitos', 'mes_vencimiento', 'anio_vencimiento']
        widgets = {
            'ultimos_4_digitos': forms.TextInput(attrs={'maxlength': 4, 'placeholder': 'Ej: 1234'}),
            'mes_vencimiento': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'anio_vencimiento': forms.NumberInput(attrs={'min': 2024, 'max': 2100}),
        }

    def clean_ultimos_4_digitos(self):
        ultimos_4 = self.cleaned_data.get('ultimos_4_digitos')

        if not ultimos_4 or not ultimos_4.isdigit():
            raise forms.ValidationError('Solo se permiten números en este campo.')

        if len(ultimos_4) != 4:
            raise forms.ValidationError('Debe ingresar exactamente 4 dígitos.')

        return ultimos_4

    def clean_mes_vencimiento(self):
        mes = self.cleaned_data.get('mes_vencimiento')

        if mes is None:
            raise forms.ValidationError('Este campo es obligatorio.')

        if not (1 <= mes <= 12):
            raise forms.ValidationError('El mes debe estar entre 1 y 12.')

        return mes

    def clean_anio_vencimiento(self):
        from datetime import date
        anio = self.cleaned_data.get('anio_vencimiento')

        if anio is None:
            raise forms.ValidationError('Este campo es obligatorio.')

        current_year = date.today().year
        if anio < current_year:
            raise forms.ValidationError('El año no puede ser menor al actual.')

        return anio

    def clean(self):
        cleaned_data = super().clean()
        mes = cleaned_data.get('mes_vencimiento')
        anio = cleaned_data.get('anio_vencimiento')

        # Validar que la fecha completa no sea una tarjeta ya vencida
        from datetime import date
        if mes and anio:
            today = date.today()
            tarjeta_fecha = date(year=anio, month=mes, day=1)
            tarjeta_fecha = tarjeta_fecha.replace(day=28)  # poner fin de mes

            if tarjeta_fecha < today.replace(day=1):
                raise forms.ValidationError('La tarjeta no puede estar vencida.')




# forms.py
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={
        'placeholder': 'Ingresa tu correo',
        'class': 'input-field'
    }))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingresa tu contraseña',
        'class': 'input-field'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Ejemplo: validar que ambos campos estén completos
        if not email:
            self.add_error('email', 'Por favor ingresa tu correo electrónico.')
        if not password:
            self.add_error('password', 'Por favor ingresa tu contraseña.')
        
        # Aquí podrías agregar más validaciones personalizadas si quieres (por ejemplo: verificar si el email existe en la BD)



class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña (mín. 8, mayúscula, número, caracter especial)',
            'class': 'input-field'
        })
    )
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre',
            'class': 'input-field'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        widget=forms.TextInput(attrs={
            'placeholder': 'Apellido',
            'class': 'input-field'
        })
    )
    
    class Meta:
        model = UserProfile
        fields = ['email', 'password', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Si no hay email, no continuar (Django ya manejará el error de campo requerido)
        if not email:
            return email

        # 1️⃣ Validar que no esté en la BD
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado. Intenta iniciar sesión o recupera tu contraseña.')

        # 2️⃣ Validar con Abstract API (correo real)
        API_KEY = '83e60704ad924a309ec603243337b8c5'  # REEMPLAZA con tu API KEY
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}"

        try:
            response = requests.get(url, timeout=10)  # Agregar timeout
            
            # Verificar que la respuesta sea exitosa
            if response.status_code != 200:
                print(f"Error en API de validación: Status {response.status_code}")
                # No bloquear el registro si la API falla, solo loguear el error
                return email
            
            result = response.json()

            # Validar formato válido
            if not result.get('is_valid_format', {}).get('value', False):
                raise forms.ValidationError('El correo no tiene un formato válido.')

            # Validar que no sea temporal
            if result.get('is_disposable_email', {}).get('value', False):
                raise forms.ValidationError('No se permiten correos temporales o desechables.')

            # Validar que acepte correos
            if result.get('deliverability') != 'DELIVERABLE':
                raise forms.ValidationError('No se pudo verificar que este correo acepte emails.')

        except forms.ValidationError:
            # Re-lanzar errores de validación
            raise
        except requests.exceptions.Timeout:
            print("Timeout al validar email con API")
            # No bloquear el registro si hay timeout, solo loguear
            return email
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión validando email con API: {e}")
            # No bloquear el registro si hay problemas de conexión
            return email
        except Exception as e:
            print(f"Error inesperado validando email con API: {e}")
            # No bloquear el registro por errores inesperados de la API
            return email

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError('La contraseña debe contener al menos un número.')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|<>,./?]', password):
            raise forms.ValidationError('La contraseña debe contener al menos un caracter especial.')

        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios.')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise forms.ValidationError('El apellido solo puede contener letras y espacios.')

        return last_name

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['email', 'password', 'first_name', 'last_name']

        for field in required_fields:
            # Solo agregar error de "campo obligatorio" si:
            # 1. El campo no tiene valor
            # 2. Y no hay errores previos en ese campo (de clean_<field>)
            value = cleaned_data.get(field)
            if not value and field not in self.errors:
                self.add_error(field, 'Este campo es obligatorio.')

class MonthlyLimitForm(forms.ModelForm):
    monthly_limit = forms.FloatField(
        label='Límite mensual',
        min_value=0
    )
    
    class Meta:
        model = UserProfile
        fields = ['monthly_limit']


from .models import Expense, PaymentMethod
from django import forms

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'payment_method', 'date', 'store_name']
        labels = {
            'amount': 'Monto',
            'category': 'Categoría',
            'payment_method': 'Método de pago',
            'date': 'Fecha',
            'store_name': 'Tienda / Servicio',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'S/. 0.00', 'class': 'input-field'}),
            'category': forms.Select(attrs={'class': 'input-field'}),
            'payment_method': forms.Select(attrs={'class': 'input-field'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'store_name': forms.TextInput(attrs={'placeholder': 'Tienda o servicio', 'class': 'input-field'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['payment_method'].queryset = PaymentMethod.objects.filter(user=user)



class InvestmentForm(forms.Form):
    COMPANY_CHOICES = [
    ('TSLA', 'Tesla'),
    ('AAPL', 'Apple'),
    ('MSFT', 'Microsoft'),
    ('GOOGL', 'Alphabet (Google)'),
    ]

    company = forms.ChoiceField(label='Empresa', choices=COMPANY_CHOICES)
    shares = forms.FloatField(label='Acciones', min_value=0.01)

class UpdateLimitForm(forms.Form):
    nuevo_limite = forms.FloatField(label='Nuevo límite mensual', min_value=0)


# ============================================
# FORMULARIOS PARA INVESTIGACION
# ============================================

from .models import (
    FinancialCompetencyAssessment, CreditSimulator, EmergencySimulator,
    UserContext, EducationalContent
)

class FinancialCompetencyAssessmentForm(forms.ModelForm):
    """Formulario de evaluacion inicial de competencias financieras"""
    class Meta:
        model = FinancialCompetencyAssessment
        fields = [
            'conocimiento_presupuesto', 'conocimiento_ahorro', 'conocimiento_credito',
            'conocimiento_inversiones', 'conocimiento_fraudes',
            'tiene_tarjetas_credito', 'cantidad_tarjetas', 'monto_deuda_actual',
            'frecuencia_pago_minimo', 'experiencia_fraude',
            'conocimiento_teorico', 'aplicacion_practica'
        ]
        widgets = {
            'conocimiento_presupuesto': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'conocimiento_ahorro': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'conocimiento_credito': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'conocimiento_inversiones': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'conocimiento_fraudes': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'conocimiento_teorico': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'aplicacion_practica': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'cantidad_tarjetas': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'monto_deuda_actual': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'frecuencia_pago_minimo': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'tiene_tarjetas_credito': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'experiencia_fraude': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CreditSimulatorForm(forms.ModelForm):
    """Formulario para simulador de credito"""
    class Meta:
        model = CreditSimulator
        fields = ['tipo_credito', 'monto_solicitado', 'plazo_meses', 'tasa_interes_anual', 'tipo_tasa']
        widgets = {
            'tipo_credito': forms.Select(attrs={'class': 'form-control'}),
            'monto_solicitado': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'plazo_meses': forms.NumberInput(attrs={'min': 1, 'max': 360, 'class': 'form-control'}),
            'tasa_interes_anual': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01, 'class': 'form-control'}),
            'tipo_tasa': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_monto_solicitado(self):
        monto = self.cleaned_data.get('monto_solicitado')
        if monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a 0.')
        return monto
    
    def clean_tasa_interes_anual(self):
        tasa = self.cleaned_data.get('tasa_interes_anual')
        if tasa < 0 or tasa > 100:
            raise forms.ValidationError('La tasa de interes debe estar entre 0 y 100%.')
        return tasa


class EmergencySimulatorForm(forms.ModelForm):
    """Formulario para simulador de emergencias"""
    class Meta:
        model = EmergencySimulator
        fields = ['escenario', 'monto_emergencia', 'fondo_emergencia_actual', 'ingresos_mensuales']
        widgets = {
            'escenario': forms.Select(attrs={'class': 'form-control'}),
            'monto_emergencia': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'fondo_emergencia_actual': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'ingresos_mensuales': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
        }
    
    def clean_ingresos_mensuales(self):
        ingresos = self.cleaned_data.get('ingresos_mensuales')
        if ingresos <= 0:
            raise forms.ValidationError('Los ingresos deben ser mayores a 0.')
        return ingresos


class UserContextForm(forms.ModelForm):
    """Formulario para contexto del usuario"""
    class Meta:
        model = UserContext
        fields = [
            'nivel_socioeconomico', 'region', 'ingresos_aproximados',
            'estilo_aprendizaje', 'nivel_conocimiento_actual'
        ]
        labels = {
            'nivel_socioeconomico': 'Nivel socioeconómico',
            'region': 'Región',
            'ingresos_aproximados': 'Ingresos aproximados (S/.)',
            'estilo_aprendizaje': 'Estilo de aprendizaje',
            'nivel_conocimiento_actual': 'Nivel de conocimiento actual',
        }
        widgets = {
            'nivel_socioeconomico': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lima, Cusco, etc.'}),
            'ingresos_aproximados': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'estilo_aprendizaje': forms.Select(attrs={'class': 'form-control'}),
            'nivel_conocimiento_actual': forms.Select(attrs={'class': 'form-control'}),
        }


class PeriodicAssessmentForm(forms.Form):
    """Formulario simplificado para evaluacion periodica (solo competencias basicas)"""
    conocimiento_presupuesto = forms.IntegerField(
        label='Conocimiento sobre Presupuestos (1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    conocimiento_ahorro = forms.IntegerField(
        label='Conocimiento sobre Ahorro (1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    conocimiento_credito = forms.IntegerField(
        label='Conocimiento sobre Crédito (1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    conocimiento_inversiones = forms.IntegerField(
        label='Conocimiento sobre Inversiones (1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    conocimiento_fraudes = forms.IntegerField(
        label='Conocimiento sobre Fraudes Digitales (1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    conocimiento_teorico = forms.IntegerField(
        label='Conocimiento Teórico (auto-evaluación 1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    aplicacion_practica = forms.IntegerField(
        label='Aplicación Práctica (auto-evaluación 1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )