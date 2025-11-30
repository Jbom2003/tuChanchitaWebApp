"""
Comando de management para poblar la base de datos con frases de economía para completar
"""
from django.core.management.base import BaseCommand
from myapp.models import FraseCompletar


class Command(BaseCommand):
    help = 'Pobla la base de datos con frases de economía para completar'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando poblacion de frases para completar...'))
        
        frases_data = [
            {
                'frase_completa': 'La TREA es la Tasa de Rendimiento Efectiva Anual que permite igualar el monto que se ha depositado con el valor actual del monto que se recibe al vencimiento del plazo.',
                'palabra_clave': 'Tasa de Rendimiento Efectiva Anual',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La TEA es la Tasa Efectiva Anual que incluye todos los costos y comisiones de un crédito.',
                'palabra_clave': 'Tasa Efectiva Anual',
                'categoria': 'credito',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El interés compuesto es el interés que se calcula sobre el capital inicial más los intereses acumulados.',
                'palabra_clave': 'interés compuesto',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un fondo de emergencia debe cubrir entre 3 y 6 meses de gastos básicos.',
                'palabra_clave': '3 y 6 meses',
                'categoria': 'ahorro',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'La regla 50-30-20 establece que el 50% de los ingresos debe destinarse a necesidades, el 30% a deseos y el 20% a ahorro.',
                'palabra_clave': '50-30-20',
                'categoria': 'presupuesto',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El phishing es un fraude digital que consiste en enviar correos electrónicos falsos que imitan instituciones legítimas.',
                'palabra_clave': 'phishing',
                'categoria': 'fraudes',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'La diversificación es una estrategia de inversión que consiste en distribuir el dinero en diferentes tipos de activos.',
                'palabra_clave': 'diversificación',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La inflación es el aumento generalizado y sostenido de los precios de bienes y servicios en una economía.',
                'palabra_clave': 'inflación',
                'categoria': 'economia',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El historial crediticio es un registro de todos tus préstamos y pagos que determina tu capacidad de obtener crédito.',
                'palabra_clave': 'historial crediticio',
                'categoria': 'credito',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'Un depósito a plazo fijo es una inversión donde depositas dinero por un período determinado a cambio de una tasa de interés.',
                'palabra_clave': 'depósito a plazo fijo',
                'categoria': 'inversiones',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El smishing es un tipo de fraude que utiliza mensajes de texto SMS para obtener información personal.',
                'palabra_clave': 'smishing',
                'categoria': 'fraudes',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'La TCEA es la Tasa de Costo Efectiva Anual que incluye todos los costos de un crédito incluyendo intereses y comisiones.',
                'palabra_clave': 'Tasa de Costo Efectiva Anual',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un fondo mutuo es una inversión colectiva donde varios inversionistas aportan dinero que se invierte en diferentes activos.',
                'palabra_clave': 'fondo mutuo',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El skimming es un fraude donde se clona la información de tu tarjeta usando dispositivos ilegales en cajeros o terminales.',
                'palabra_clave': 'skimming',
                'categoria': 'fraudes',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La capitalización es el proceso de agregar intereses al capital para que generen más intereses en el siguiente período.',
                'palabra_clave': 'capitalización',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El patrimonio neto se calcula restando los pasivos de los activos.',
                'palabra_clave': 'patrimonio neto',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La liquidez es la facilidad con la que un activo puede convertirse en efectivo sin perder valor.',
                'palabra_clave': 'liquidez',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El pharming es un fraude que redirige tu navegador a sitios falsos aunque escribas la URL correcta.',
                'palabra_clave': 'pharming',
                'categoria': 'fraudes',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'El método bola de nieve consiste en pagar primero la deuda más pequeña para generar motivación.',
                'palabra_clave': 'método bola de nieve',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El método avalancha consiste en pagar primero la deuda con mayor tasa de interés para ahorrar más dinero.',
                'palabra_clave': 'método avalancha',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La SBS es la Superintendencia de Banca y Seguros que regula el sistema financiero en Perú.',
                'palabra_clave': 'Superintendencia de Banca y Seguros',
                'categoria': 'regulacion',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El SMV es la Superintendencia del Mercado de Valores que regula las inversiones en Perú.',
                'palabra_clave': 'Superintendencia del Mercado de Valores',
                'categoria': 'regulacion',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'Un activo es cualquier bien o derecho que tiene valor económico y puede generar ingresos.',
                'palabra_clave': 'activo',
                'categoria': 'finanzas',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'Un pasivo es una deuda u obligación que debes pagar en el futuro.',
                'palabra_clave': 'pasivo',
                'categoria': 'finanzas',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'La rentabilidad es la ganancia o retorno que obtienes de una inversión expresada como porcentaje.',
                'palabra_clave': 'rentabilidad',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El riesgo en inversiones es la posibilidad de perder parte o todo el capital invertido.',
                'palabra_clave': 'riesgo',
                'categoria': 'inversiones',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El vishing es un fraude que utiliza llamadas telefónicas para obtener información personal haciéndose pasar por instituciones legítimas.',
                'palabra_clave': 'vishing',
                'categoria': 'fraudes',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La tasa de interés nominal es la tasa que no incluye el efecto de la capitalización.',
                'palabra_clave': 'tasa de interés nominal',
                'categoria': 'credito',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'La tasa de interés efectiva es la tasa que incluye el efecto de la capitalización de intereses.',
                'palabra_clave': 'tasa de interés efectiva',
                'categoria': 'credito',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'Un crédito rotativo es un crédito que puedes usar repetidamente hasta un límite establecido.',
                'palabra_clave': 'crédito rotativo',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La amortización es el proceso de pagar gradualmente una deuda mediante cuotas que incluyen capital e intereses.',
                'palabra_clave': 'amortización',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El score crediticio es una calificación numérica que refleja tu historial de pagos y capacidad crediticia.',
                'palabra_clave': 'score crediticio',
                'categoria': 'credito',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'La rentabilidad nominal es la rentabilidad sin ajustar por el efecto de la inflación.',
                'palabra_clave': 'rentabilidad nominal',
                'categoria': 'inversiones',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'La rentabilidad real es la rentabilidad ajustada por el efecto de la inflación.',
                'palabra_clave': 'rentabilidad real',
                'categoria': 'inversiones',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'Un activo corriente es un activo que se espera convertir en efectivo dentro de un año.',
                'palabra_clave': 'activo corriente',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un pasivo corriente es una deuda que debe pagarse dentro de un año.',
                'palabra_clave': 'pasivo corriente',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La solvencia es la capacidad de una persona o empresa para cumplir con sus obligaciones financieras.',
                'palabra_clave': 'solvencia',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La renta fija es un tipo de inversión que ofrece un retorno conocido y predecible.',
                'palabra_clave': 'renta fija',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La renta variable es un tipo de inversión donde el retorno no está garantizado y puede variar.',
                'palabra_clave': 'renta variable',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un dividendo es el pago que reciben los accionistas de una empresa como parte de las ganancias.',
                'palabra_clave': 'dividendo',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El apalancamiento es el uso de deuda para aumentar el potencial retorno de una inversión.',
                'palabra_clave': 'apalancamiento',
                'categoria': 'inversiones',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'La depreciación es la pérdida de valor de un activo a lo largo del tiempo debido al uso o desgaste.',
                'palabra_clave': 'depreciación',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La morosidad es el atraso en el pago de una obligación financiera más allá de la fecha de vencimiento.',
                'palabra_clave': 'morosidad',
                'categoria': 'credito',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El flujo de caja es el movimiento de dinero que entra y sale de tus finanzas personales o de una empresa.',
                'palabra_clave': 'flujo de caja',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un crédito garantizado es un préstamo que requiere una garantía colateral como respaldo.',
                'palabra_clave': 'crédito garantizado',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La tasa de interés real es la tasa nominal menos la tasa de inflación.',
                'palabra_clave': 'tasa de interés real',
                'categoria': 'credito',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'El valor presente es el valor actual de una cantidad futura de dinero descontada a una tasa de interés.',
                'palabra_clave': 'valor presente',
                'categoria': 'inversiones',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'El valor futuro es el valor que tendrá una inversión en una fecha futura considerando el interés compuesto.',
                'palabra_clave': 'valor futuro',
                'categoria': 'inversiones',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'La tasa de descuento es la tasa de interés utilizada para calcular el valor presente de flujos futuros.',
                'palabra_clave': 'tasa de descuento',
                'categoria': 'inversiones',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'Un activo productivo es un activo que genera ingresos o beneficios económicos.',
                'palabra_clave': 'activo productivo',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La tasa de retorno es el porcentaje de ganancia o pérdida de una inversión en relación al capital invertido.',
                'palabra_clave': 'tasa de retorno',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un crédito de libre disponibilidad es un préstamo que puedes usar para cualquier propósito sin restricciones.',
                'palabra_clave': 'crédito de libre disponibilidad',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La tasa de interés moratoria es la tasa adicional que se cobra cuando no pagas una obligación a tiempo.',
                'palabra_clave': 'tasa de interés moratoria',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La tasa de interés compensatoria es la tasa que pagas por el uso del dinero prestado.',
                'palabra_clave': 'tasa de interés compensatoria',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo de reserva de valor es un activo que mantiene su valor a lo largo del tiempo.',
                'palabra_clave': 'activo de reserva de valor',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La tasa de interés preferencial es una tasa más baja ofrecida a clientes con buen historial crediticio.',
                'palabra_clave': 'tasa de interés preferencial',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un crédito con garantía hipotecaria es un préstamo respaldado por una propiedad inmueble.',
                'palabra_clave': 'crédito con garantía hipotecaria',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo financiero es un activo que representa un derecho sobre un valor monetario.',
                'palabra_clave': 'activo financiero',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La capitalización mensual significa que los intereses se calculan y agregan al capital cada mes.',
                'palabra_clave': 'capitalización mensual',
                'categoria': 'inversiones',
                'nivel_dificultad': 3
            },
            {
                'frase_completa': 'Un fondo de inversión es una inversión colectiva donde varios inversionistas aportan dinero para invertir en conjunto.',
                'palabra_clave': 'fondo de inversión',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo intangible es un activo que no tiene forma física pero tiene valor económico.',
                'palabra_clave': 'activo intangible',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un crédito revolvente es un crédito que se renueva automáticamente después de cada pago.',
                'palabra_clave': 'crédito revolvente',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La tasa de usura es una tasa de interés excesivamente alta que puede ser considerada ilegal.',
                'palabra_clave': 'tasa de usura',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo de fácil realización es un activo que puede convertirse rápidamente en efectivo sin perder valor.',
                'palabra_clave': 'activo de fácil realización',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo de inversión es un activo adquirido con el propósito de generar retorno o ganancia.',
                'palabra_clave': 'activo de inversión',
                'categoria': 'inversiones',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo de consumo es un activo adquirido para uso personal y no para generar ingresos.',
                'palabra_clave': 'activo de consumo',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo depreciable es un activo que pierde valor con el tiempo debido al uso o desgaste.',
                'palabra_clave': 'activo depreciable',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo financiero líquido es un activo financiero que puede convertirse fácilmente en efectivo.',
                'palabra_clave': 'activo financiero líquido',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un activo de reserva es un activo mantenido para cubrir necesidades futuras o emergencias.',
                'palabra_clave': 'activo de reserva',
                'categoria': 'finanzas',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'La amortización de préstamo es el proceso de pagar gradualmente el capital e intereses de un préstamo mediante cuotas.',
                'palabra_clave': 'amortización de préstamo',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'Un crédito pre-aprobado es una oferta de crédito condicional basada en una evaluación preliminar de tu historial.',
                'palabra_clave': 'crédito pre-aprobado',
                'categoria': 'credito',
                'nivel_dificultad': 2
            },
            {
                'frase_completa': 'El cashback es un beneficio que te devuelve un porcentaje del dinero gastado en compras con tarjeta.',
                'palabra_clave': 'cashback',
                'categoria': 'credito',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'Una cuenta de ahorro programada es una cuenta que realiza transferencias automáticas de ahorro.',
                'palabra_clave': 'cuenta de ahorro programada',
                'categoria': 'ahorro',
                'nivel_dificultad': 1
            },
            {
                'frase_completa': 'El seguro de depósitos es una protección que garantiza tus depósitos bancarios hasta cierto monto.',
                'palabra_clave': 'seguro de depósitos',
                'categoria': 'ahorro',
                'nivel_dificultad': 2
            },
        ]
        
        self.stdout.write(self.style.WARNING('Creando frases para completar...'))
        creadas = 0
        existentes = 0
        
        for frase_data in frases_data:
            obj, created = FraseCompletar.objects.get_or_create(
                frase_completa=frase_data['frase_completa'],
                defaults=frase_data
            )
            if created:
                creadas += 1
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creada: {obj.frase_completa[:50]}...'))
            else:
                existentes += 1
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {obj.frase_completa[:50]}...'))
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal frases creadas: {creadas}'))
        self.stdout.write(self.style.WARNING(f'Frases que ya existían: {existentes}'))
        self.stdout.write(self.style.SUCCESS(f'Total frases en BD: {FraseCompletar.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('¡Poblacion de frases completada!'))

