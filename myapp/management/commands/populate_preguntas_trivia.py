"""
Comando de management para poblar la base de datos con 90 preguntas adicionales de trivia financiera
"""
from django.core.management.base import BaseCommand
from myapp.models import PreguntaTrivia


class Command(BaseCommand):
    help = 'Pobla la base de datos con 90 preguntas adicionales de trivia financiera'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando poblacion de preguntas de trivia...'))
        
        preguntas_data = [
            {
                'pregunta': '¿Qué significa la sigla TEA en finanzas?',
                'opciones': {'a': 'Tasa Efectiva Anual', 'b': 'Tasa Efectiva Aplicada', 'c': 'Tasa de Egreso Anual', 'd': 'Tasa de Entrada Anual'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Cuál es el objetivo principal de un fondo de emergencia?',
                'opciones': {'a': 'Invertir en acciones', 'b': 'Cubrir gastos inesperados', 'c': 'Pagar deudas', 'd': 'Comprar bienes raíces'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué porcentaje de tus ingresos se recomienda ahorrar mensualmente?',
                'opciones': {'a': '5%', 'b': '10%', 'c': '20%', 'd': '50%'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es el interés compuesto?',
                'opciones': {'a': 'Interés que se calcula una vez', 'b': 'Interés que se calcula sobre el capital más intereses acumulados', 'c': 'Interés fijo', 'd': 'Interés variable'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un presupuesto personal?',
                'opciones': {'a': 'Un plan de gastos', 'b': 'Un plan para tu dinero', 'c': 'Una lista de deseos', 'd': 'Un registro de deudas'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Cuál es la regla 50-30-20?',
                'opciones': {'a': '50% necesidades, 30% deseos, 20% ahorro', 'b': '50% ahorro, 30% gastos, 20% inversión', 'c': '50% ingresos, 30% gastos, 20% ahorro', 'd': '50% gastos, 30% ahorro, 20% inversión'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es el phishing?',
                'opciones': {'a': 'Un tipo de inversión', 'b': 'Un fraude por correo electrónico', 'c': 'Un método de ahorro', 'd': 'Un tipo de crédito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Cuántos meses de gastos se recomienda tener en un fondo de emergencia?',
                'opciones': {'a': '1-2 meses', 'b': '3-6 meses', 'c': '7-12 meses', 'd': 'Más de 12 meses'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la diversificación en inversiones?',
                'opciones': {'a': 'Invertir todo en una sola opción', 'b': 'Distribuir inversiones en diferentes opciones', 'c': 'Invertir solo en acciones', 'd': 'No invertir nada'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué significa TCEA?',
                'opciones': {'a': 'Tasa de Costo Efectiva Anual', 'b': 'Tasa de Crédito Efectiva Anual', 'c': 'Tasa de Capital Efectiva Anual', 'd': 'Tasa de Cálculo Efectiva Anual'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es un depósito a plazo fijo?',
                'opciones': {'a': 'Una cuenta de ahorro', 'b': 'Un préstamo bancario', 'c': 'Una inversión con plazo determinado', 'd': 'Una tarjeta de crédito'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es el historial crediticio?',
                'opciones': {'a': 'Un registro de tus ahorros', 'b': 'Un registro de tus préstamos y pagos', 'c': 'Un registro de tus inversiones', 'd': 'Un registro de tus gastos'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: pagar el mínimo o el total de la tarjeta de crédito?',
                'opciones': {'a': 'Pagar el mínimo', 'b': 'Pagar el total', 'c': 'No pagar nada', 'd': 'Pagar la mitad'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la inflación?',
                'opciones': {'a': 'Aumento del valor del dinero', 'b': 'Aumento generalizado de precios', 'c': 'Disminución de precios', 'd': 'Estabilidad de precios'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un fondo mutuo?',
                'opciones': {'a': 'Un préstamo', 'b': 'Una inversión colectiva', 'c': 'Una cuenta de ahorro', 'd': 'Una tarjeta de crédito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el smishing?',
                'opciones': {'a': 'Un tipo de inversión', 'b': 'Phishing por SMS', 'c': 'Un método de ahorro', 'd': 'Un tipo de crédito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor para construir historial crediticio?',
                'opciones': {'a': 'No usar crédito', 'b': 'Usar crédito responsablemente', 'c': 'Solicitar muchas tarjetas', 'd': 'Solo pagar el mínimo'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el skimming?',
                'opciones': {'a': 'Un tipo de inversión', 'b': 'Clonación de tarjetas', 'c': 'Un método de ahorro', 'd': 'Un tipo de crédito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Cuál es el riesgo de retirar efectivo con tarjeta de crédito?',
                'opciones': {'a': 'No hay riesgo', 'b': 'Comisiones e intereses altos', 'c': 'Es gratis', 'd': 'Mejora el historial crediticio'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la TREA?',
                'opciones': {'a': 'Tasa de Rendimiento Efectiva Anual', 'b': 'Tasa de Retorno Efectiva Anual', 'c': 'Tasa de Recuperación Efectiva Anual', 'd': 'Tasa de Reembolso Efectiva Anual'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es un presupuesto de caja?',
                'opciones': {'a': 'Un presupuesto de ingresos', 'b': 'Un presupuesto de flujo de efectivo', 'c': 'Un presupuesto de gastos', 'd': 'Un presupuesto de ahorro'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la capitalización?',
                'opciones': {'a': 'Proceso de agregar intereses al capital', 'b': 'Proceso de restar intereses', 'c': 'Proceso de calcular gastos', 'd': 'Proceso de ahorrar dinero'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: ahorro o inversión?',
                'opciones': {'a': 'Solo ahorro', 'b': 'Solo inversión', 'c': 'Ambos según objetivos', 'd': 'Ninguno'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es el vishing?',
                'opciones': {'a': 'Un tipo de inversión', 'b': 'Phishing por llamada telefónica', 'c': 'Un método de ahorro', 'd': 'Un tipo de crédito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Cuál es el porcentaje máximo recomendado de utilización de tarjeta de crédito?',
                'opciones': {'a': '50%', 'b': '30%', 'c': '80%', 'd': '100%'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un activo?',
                'opciones': {'a': 'Algo que genera deuda', 'b': 'Algo que tiene valor económico', 'c': 'Algo que cuesta dinero', 'd': 'Algo que no vale nada'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un pasivo?',
                'opciones': {'a': 'Algo que genera ingresos', 'b': 'Una deuda u obligación', 'c': 'Un activo', 'd': 'Una inversión'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el patrimonio neto?',
                'opciones': {'a': 'Activos menos pasivos', 'b': 'Pasivos menos activos', 'c': 'Solo activos', 'd': 'Solo pasivos'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es la liquidez?',
                'opciones': {'a': 'Facilidad para convertir en efectivo', 'b': 'Dificultad para convertir en efectivo', 'c': 'Tipo de inversión', 'd': 'Tipo de crédito'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es el pharming?',
                'opciones': {'a': 'Un tipo de inversión', 'b': 'Redirección a sitios falsos', 'c': 'Un método de ahorro', 'd': 'Un tipo de crédito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor para emergencias: cuenta de ahorro o depósito a plazo?',
                'opciones': {'a': 'Depósito a plazo', 'b': 'Cuenta de ahorro', 'c': 'Ambos iguales', 'd': 'Ninguno'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de interés nominal?',
                'opciones': {'a': 'Tasa sin incluir comisiones', 'b': 'Tasa sin incluir capitalización', 'c': 'Tasa real', 'd': 'Tasa efectiva'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un crédito rotativo?',
                'opciones': {'a': 'Un crédito de una sola vez', 'b': 'Un crédito que se puede usar repetidamente', 'c': 'Un crédito fijo', 'd': 'Un crédito variable'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el método bola de nieve para pagar deudas?',
                'opciones': {'a': 'Pagar la deuda más grande primero', 'b': 'Pagar la deuda más pequeña primero', 'c': 'Pagar todas igual', 'd': 'No pagar nada'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el método avalancha para pagar deudas?',
                'opciones': {'a': 'Pagar la deuda más pequeña primero', 'b': 'Pagar la deuda con mayor tasa primero', 'c': 'Pagar todas igual', 'd': 'No pagar nada'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la SBS?',
                'opciones': {'a': 'Superintendencia de Banca y Seguros', 'b': 'Sistema Bancario Seguro', 'c': 'Servicio Bancario Simple', 'd': 'Sistema de Banca Social'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es el SMV?',
                'opciones': {'a': 'Superintendencia del Mercado de Valores', 'b': 'Sistema de Mercado Virtual', 'c': 'Servicio de Mercado de Valores', 'd': 'Sistema de Mercado Variable'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: interés simple o compuesto?',
                'opciones': {'a': 'Interés simple', 'b': 'Interés compuesto', 'c': 'Ambos iguales', 'd': 'Ninguno'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un activo líquido?',
                'opciones': {'a': 'Un activo difícil de vender', 'b': 'Un activo fácil de convertir en efectivo', 'c': 'Un activo físico', 'd': 'Un activo intangible'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la rentabilidad?',
                'opciones': {'a': 'Pérdida de una inversión', 'b': 'Ganancia de una inversión', 'c': 'Costo de una inversión', 'd': 'Riesgo de una inversión'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el riesgo en inversiones?',
                'opciones': {'a': 'La certeza de ganar', 'b': 'La posibilidad de perder', 'c': 'La garantía de retorno', 'd': 'La falta de inversión'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la diversificación de riesgo?',
                'opciones': {'a': 'Invertir todo en una opción', 'b': 'Distribuir inversiones para reducir riesgo', 'c': 'No invertir nada', 'd': 'Invertir solo en acciones'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un activo fijo?',
                'opciones': {'a': 'Un activo que se mueve', 'b': 'Un activo de largo plazo', 'c': 'Un activo líquido', 'd': 'Un activo variable'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el flujo de caja?',
                'opciones': {'a': 'Movimiento de dinero', 'b': 'Dinero estático', 'c': 'Solo ingresos', 'd': 'Solo gastos'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: pagar deudas o ahorrar?',
                'opciones': {'a': 'Solo ahorrar', 'b': 'Solo pagar deudas', 'c': 'Depende de la tasa de interés', 'd': 'Ninguno'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un crédito de consumo?',
                'opciones': {'a': 'Crédito para empresas', 'b': 'Crédito para consumo personal', 'c': 'Crédito hipotecario', 'd': 'Crédito vehicular'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la amortización?',
                'opciones': {'a': 'Aumento de deuda', 'b': 'Pago gradual de deuda', 'c': 'Cancelación de deuda', 'd': 'Aumento de intereses'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un crédito pre-aprobado?',
                'opciones': {'a': 'Un crédito garantizado', 'b': 'Una oferta de crédito condicional', 'c': 'Un crédito sin interés', 'd': 'Un crédito gratuito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: tarjeta de crédito o débito?',
                'opciones': {'a': 'Solo crédito', 'b': 'Solo débito', 'c': 'Ambas según uso', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es el cashback?',
                'opciones': {'a': 'Devolución de dinero', 'b': 'Reembolso por compras', 'c': 'Ambos anteriores', 'd': 'Cargo adicional'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es una cuenta de ahorro programada?',
                'opciones': {'a': 'Ahorro automático', 'b': 'Ahorro manual', 'c': 'Ahorro sin plan', 'd': 'Ahorro temporal'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es el seguro de depósitos?',
                'opciones': {'a': 'Seguro que protege depósitos bancarios', 'b': 'Seguro de vida', 'c': 'Seguro de salud', 'd': 'Seguro vehicular'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: inversión a corto o largo plazo?',
                'opciones': {'a': 'Solo corto plazo', 'b': 'Solo largo plazo', 'c': 'Depende de objetivos', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo corriente?',
                'opciones': {'a': 'Activo de largo plazo', 'b': 'Activo que se convierte en efectivo en un año', 'c': 'Activo fijo', 'd': 'Activo intangible'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un pasivo corriente?',
                'opciones': {'a': 'Pasivo de largo plazo', 'b': 'Pasivo que se paga en un año', 'c': 'Pasivo fijo', 'd': 'Pasivo intangible'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la solvencia?',
                'opciones': {'a': 'Capacidad de pagar deudas', 'b': 'Incapacidad de pagar', 'c': 'Falta de activos', 'd': 'Exceso de pasivos'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es la renta fija?',
                'opciones': {'a': 'Inversión con retorno variable', 'b': 'Inversión con retorno conocido', 'c': 'Inversión sin retorno', 'd': 'Inversión riesgosa'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la renta variable?',
                'opciones': {'a': 'Inversión con retorno fijo', 'b': 'Inversión con retorno variable', 'c': 'Inversión sin retorno', 'd': 'Inversión segura'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un dividendo?',
                'opciones': {'a': 'Pago a accionistas', 'b': 'Pago de deuda', 'c': 'Pago de intereses', 'd': 'Pago de impuestos'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: ahorro tradicional o inversión?',
                'opciones': {'a': 'Solo ahorro', 'b': 'Solo inversión', 'c': 'Ambos según objetivos', 'd': 'Ninguno'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es el apalancamiento?',
                'opciones': {'a': 'Usar deuda para invertir', 'b': 'Usar solo capital propio', 'c': 'No invertir', 'd': 'Solo ahorrar'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es un activo intangible?',
                'opciones': {'a': 'Activo físico', 'b': 'Activo sin forma física', 'c': 'Activo líquido', 'd': 'Activo fijo'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la depreciación?',
                'opciones': {'a': 'Aumento de valor', 'b': 'Pérdida de valor en el tiempo', 'c': 'Mantenimiento de valor', 'd': 'Ganancia de valor'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: crédito con tasa fija o variable?',
                'opciones': {'a': 'Solo fija', 'b': 'Solo variable', 'c': 'Depende de situación', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un crédito garantizado?',
                'opciones': {'a': 'Crédito sin garantía', 'b': 'Crédito con garantía colateral', 'c': 'Crédito sin interés', 'd': 'Crédito gratuito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la morosidad?',
                'opciones': {'a': 'Pago puntual', 'b': 'Atraso en pagos', 'c': 'Pago anticipado', 'd': 'Pago completo'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el score crediticio?',
                'opciones': {'a': 'Calificación crediticia', 'b': 'Puntuación de ahorro', 'c': 'Puntuación de inversión', 'd': 'Puntuación de gastos'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: pagar deudas con alta o baja tasa primero?',
                'opciones': {'a': 'Alta tasa primero', 'b': 'Baja tasa primero', 'c': 'Ambas igual', 'd': 'Ninguna'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es un activo financiero?',
                'opciones': {'a': 'Activo físico', 'b': 'Activo con valor monetario', 'c': 'Activo sin valor', 'd': 'Activo intangible'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la capitalización mensual?',
                'opciones': {'a': 'Interés calculado anualmente', 'b': 'Interés calculado mensualmente', 'c': 'Interés calculado diariamente', 'd': 'Interés calculado semanalmente'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: inversión conservadora o agresiva?',
                'opciones': {'a': 'Solo conservadora', 'b': 'Solo agresiva', 'c': 'Depende de perfil de riesgo', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un fondo de inversión?',
                'opciones': {'a': 'Inversión individual', 'b': 'Inversión colectiva', 'c': 'Ahorro simple', 'd': 'Crédito'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la rentabilidad nominal?',
                'opciones': {'a': 'Rentabilidad sin ajustar inflación', 'b': 'Rentabilidad ajustada por inflación', 'c': 'Rentabilidad real', 'd': 'Rentabilidad efectiva'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es la rentabilidad real?',
                'opciones': {'a': 'Rentabilidad sin ajustar inflación', 'b': 'Rentabilidad ajustada por inflación', 'c': 'Rentabilidad nominal', 'd': 'Rentabilidad efectiva'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: ahorro en soles o dólares?',
                'opciones': {'a': 'Solo soles', 'b': 'Solo dólares', 'c': 'Diversificar según objetivos', 'd': 'Ninguno'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo productivo?',
                'opciones': {'a': 'Activo que genera ingresos', 'b': 'Activo que genera gastos', 'c': 'Activo sin valor', 'd': 'Activo fijo'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es un pasivo productivo?',
                'opciones': {'a': 'Deuda que genera ingresos', 'b': 'Deuda que solo genera gastos', 'c': 'Deuda sin interés', 'd': 'Deuda gratuita'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es la tasa de descuento?',
                'opciones': {'a': 'Tasa para calcular valor futuro', 'b': 'Tasa para calcular valor presente', 'c': 'Tasa de interés', 'd': 'Tasa de inflación'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es el valor presente?',
                'opciones': {'a': 'Valor futuro descontado', 'b': 'Valor futuro', 'c': 'Valor nominal', 'd': 'Valor real'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es el valor futuro?',
                'opciones': {'a': 'Valor presente', 'b': 'Valor de una inversión en el futuro', 'c': 'Valor nominal', 'd': 'Valor real'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: inversión activa o pasiva?',
                'opciones': {'a': 'Solo activa', 'b': 'Solo pasiva', 'c': 'Depende de conocimiento y tiempo', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo de reserva?',
                'opciones': {'a': 'Activo para emergencias', 'b': 'Activo para inversión', 'c': 'Activo para gastos', 'd': 'Activo para deudas'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es la tasa de retorno?',
                'opciones': {'a': 'Pérdida de inversión', 'b': 'Ganancia porcentual de inversión', 'c': 'Costo de inversión', 'd': 'Riesgo de inversión'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: crédito personal o tarjeta de crédito?',
                'opciones': {'a': 'Solo crédito personal', 'b': 'Solo tarjeta', 'c': 'Depende de necesidad', 'd': 'Ninguno'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo depreciable?',
                'opciones': {'a': 'Activo que mantiene valor', 'b': 'Activo que pierde valor', 'c': 'Activo que gana valor', 'd': 'Activo intangible'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la amortización de préstamo?',
                'opciones': {'a': 'Aumento de deuda', 'b': 'Pago gradual de capital e intereses', 'c': 'Cancelación inmediata', 'd': 'Aumento de intereses'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: ahorro programado o esporádico?',
                'opciones': {'a': 'Solo programado', 'b': 'Solo esporádico', 'c': 'Programado es mejor', 'd': 'Ambos iguales'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un crédito revolvente?',
                'opciones': {'a': 'Crédito de una vez', 'b': 'Crédito renovable', 'c': 'Crédito fijo', 'd': 'Crédito variable'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de usura?',
                'opciones': {'a': 'Tasa máxima permitida', 'b': 'Tasa excesivamente alta', 'c': 'Tasa normal', 'd': 'Tasa baja'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: inversión en bienes raíces o acciones?',
                'opciones': {'a': 'Solo bienes raíces', 'b': 'Solo acciones', 'c': 'Diversificar', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo de fácil realización?',
                'opciones': {'a': 'Activo difícil de vender', 'b': 'Activo fácil de convertir en efectivo', 'c': 'Activo fijo', 'd': 'Activo intangible'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de interés real?',
                'opciones': {'a': 'Tasa nominal menos inflación', 'b': 'Tasa nominal más inflación', 'c': 'Tasa nominal', 'd': 'Tasa efectiva'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: crédito a corto o largo plazo?',
                'opciones': {'a': 'Solo corto plazo', 'b': 'Solo largo plazo', 'c': 'Depende de necesidad', 'd': 'Ninguno'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo de reserva de valor?',
                'opciones': {'a': 'Activo que mantiene valor', 'b': 'Activo que pierde valor', 'c': 'Activo que gana valor', 'd': 'Activo sin valor'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es la tasa de interés efectiva?',
                'opciones': {'a': 'Tasa nominal', 'b': 'Tasa que incluye capitalización', 'c': 'Tasa simple', 'd': 'Tasa fija'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: ahorro en banco o bajo el colchón?',
                'opciones': {'a': 'Bajo el colchón', 'b': 'En banco', 'c': 'Ambos iguales', 'd': 'Ninguno'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un crédito con garantía hipotecaria?',
                'opciones': {'a': 'Crédito sin garantía', 'b': 'Crédito garantizado con propiedad', 'c': 'Crédito personal', 'd': 'Crédito vehicular'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de interés preferencial?',
                'opciones': {'a': 'Tasa alta', 'b': 'Tasa baja para clientes preferenciales', 'c': 'Tasa normal', 'd': 'Tasa variable'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: inversión en moneda nacional o extranjera?',
                'opciones': {'a': 'Solo nacional', 'b': 'Solo extranjera', 'c': 'Diversificar', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo de inversión?',
                'opciones': {'a': 'Activo para consumo', 'b': 'Activo para generar retorno', 'c': 'Activo sin valor', 'd': 'Activo fijo'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de interés variable?',
                'opciones': {'a': 'Tasa que no cambia', 'b': 'Tasa que cambia según mercado', 'c': 'Tasa fija', 'd': 'Tasa única'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: ahorro con interés o sin interés?',
                'opciones': {'a': 'Sin interés', 'b': 'Con interés', 'c': 'Ambos iguales', 'd': 'Ninguno'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es un crédito de libre disponibilidad?',
                'opciones': {'a': 'Crédito con restricciones', 'b': 'Crédito para usar libremente', 'c': 'Crédito específico', 'd': 'Crédito limitado'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de interés fija?',
                'opciones': {'a': 'Tasa que cambia', 'b': 'Tasa que no cambia', 'c': 'Tasa variable', 'd': 'Tasa única'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: inversión de bajo o alto riesgo?',
                'opciones': {'a': 'Solo bajo riesgo', 'b': 'Solo alto riesgo', 'c': 'Diversificar según perfil', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo de consumo?',
                'opciones': {'a': 'Activo para inversión', 'b': 'Activo para consumo personal', 'c': 'Activo productivo', 'd': 'Activo de reserva'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de interés moratoria?',
                'opciones': {'a': 'Tasa por pago puntual', 'b': 'Tasa por pago atrasado', 'c': 'Tasa normal', 'd': 'Tasa preferencial'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es mejor: crédito con cuota fija o variable?',
                'opciones': {'a': 'Solo fija', 'b': 'Solo variable', 'c': 'Depende de preferencia', 'd': 'Ninguna'},
                'respuesta_correcta': 'c'
            },
            {
                'pregunta': '¿Qué es un activo financiero líquido?',
                'opciones': {'a': 'Activo difícil de vender', 'b': 'Activo fácil de convertir en efectivo', 'c': 'Activo fijo', 'd': 'Activo intangible'},
                'respuesta_correcta': 'b'
            },
            {
                'pregunta': '¿Qué es la tasa de interés compensatoria?',
                'opciones': {'a': 'Tasa por uso del crédito', 'b': 'Tasa por ahorro', 'c': 'Tasa por inversión', 'd': 'Tasa por depósito'},
                'respuesta_correcta': 'a'
            },
            {
                'pregunta': '¿Qué es mejor: ahorro a corto o largo plazo?',
                'opciones': {'a': 'Solo corto plazo', 'b': 'Solo largo plazo', 'c': 'Ambos según objetivos', 'd': 'Ninguno'},
                'respuesta_correcta': 'c'
            },
        ]
        
        self.stdout.write(self.style.WARNING('Creando preguntas de trivia...'))
        creadas = 0
        existentes = 0
        
        for pregunta_data in preguntas_data:
            obj, created = PreguntaTrivia.objects.get_or_create(
                pregunta=pregunta_data['pregunta'],
                defaults=pregunta_data
            )
            if created:
                creadas += 1
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creada: {obj.pregunta[:50]}...'))
            else:
                existentes += 1
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {obj.pregunta[:50]}...'))
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal preguntas creadas: {creadas}'))
        self.stdout.write(self.style.WARNING(f'Preguntas que ya existían: {existentes}'))
        self.stdout.write(self.style.SUCCESS(f'Total preguntas en BD: {PreguntaTrivia.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('¡Poblacion de preguntas completada!'))

