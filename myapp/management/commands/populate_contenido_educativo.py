"""
Comando de management para poblar la base de datos con:
- Contenido educativo (biblioteca educativa)
- Narrativa progresiva (storylines)
- Contenido adicional de prevencion de fraudes
"""
from django.core.management.base import BaseCommand
from myapp.models import EducationalContent, Storyline, FraudPreventionContent


class Command(BaseCommand):
    help = 'Pobla la base de datos con contenido educativo, narrativa y fraudes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando poblacion de contenido educativo...'))
        
        # ============================================
        # CONTENIDO EDUCATIVO - BIBLIOTECA
        # ============================================
        contenido_data = [
            {
                'titulo': 'Como crear tu primer presupuesto personal',
                'tipo_contenido': 'articulo',
                'categoria': 'presupuesto',
                'descripcion': 'Guia completa paso a paso para crear y mantener un presupuesto personal efectivo, adaptado a la realidad economica peruana.',
                'contenido': '''# Como crear tu primer presupuesto personal

## Introduccion
Un presupuesto personal es la herramienta fundamental para tomar control de tus finanzas. En Peru, donde el costo de vida puede variar significativamente entre regiones, tener un presupuesto te ayudara a planificar mejor tus gastos.

## Paso 1: Identifica tus ingresos
- Lista todas tus fuentes de ingresos mensuales (sueldo, freelance, alquileres, etc.)
- Si tus ingresos son variables, calcula un promedio de los ultimos 6 meses
- En Peru, considera el pago de aguinaldo y gratificaciones si aplica

## Paso 2: Lista tus gastos fijos
- Alquiler o cuota hipotecaria
- Servicios publicos (luz, agua, internet, telefonia)
- Alimentacion basica
- Transporte
- Seguros (EPS, SOAT, etc.)
- Deudas fijas (tarjetas, prestamos)

## Paso 3: Identifica gastos variables
- Entretenimiento
- Comidas fuera de casa
- Compras no esenciales
- Emergencias

## Paso 4: Aplica la regla 50-30-20
- 50% para necesidades basicas (gastos fijos)
- 30% para deseos (gastos variables)
- 20% para ahorro e inversion

## Ejemplo practico en Peru
Si ganas S/. 3,000 al mes:
- Necesidades: S/. 1,500 (alquiler S/. 800, comida S/. 500, servicios S/. 200)
- Deseos: S/. 900 (entretenimiento, ropa, salidas)
- Ahorro: S/. 600 (fondo de emergencia, inversion)

## Herramientas utiles
- Usa aplicaciones como TuChanchita para rastrear tus gastos
- Revisa tu presupuesto mensualmente
- Ajusta segun tus necesidades y cambios en ingresos

## Consejos adicionales
- Siempre ahorra primero antes de gastar
- Revisa tus gastos bancarios regularmente
- Considera inflacion anual del 2-3% en tus calculos''',
                'nivel_dificultad': 1,
                'duracion_minutos': 15,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['SBS', 'BCP', 'BBVA'],
            },
            {
                'titulo': 'Ahorro inteligente: Estrategias para jovenes en Peru',
                'tipo_contenido': 'articulo',
                'categoria': 'ahorro',
                'descripcion': 'Estrategias practicas de ahorro adaptadas a jovenes peruanos, incluyendo herramientas y cuentas de ahorro disponibles en el pais.',
                'contenido': '''# Ahorro inteligente: Estrategias para jovenes

## ¿Por qué ahorrar?
Ahorrar te da libertad financiera y te prepara para emergencias. En Peru, tener un fondo de emergencia es crucial debido a la informalidad laboral.

## Estrategias de ahorro

### 1. Fondo de emergencia
- Objetivo: 3-6 meses de gastos basicos
- Ejemplo: Si gastas S/. 2,000/mes, ahorra S/. 6,000 - S/. 12,000
- Mantenlo en una cuenta de ahorro separada

### 2. Ahorro automatico
- Programa transferencias automaticas a una cuenta de ahorro
- "Paga primero a ti mismo" - ahorra antes de gastar
- Muchos bancos peruanos ofrecen cuentas de ahorro sin comisiones

### 3. Metodos de ahorro populares en Peru

**Regla del sobre:**
- Divide tu dinero en sobres para cada categoria
- Solo gasta lo que esta en cada sobre

**Reto de las 52 semanas:**
- Semana 1: S/. 1
- Semana 2: S/. 2
- ...
- Semana 52: S/. 52
- Total ahorrado: S/. 1,378

**Ahorro por objetivos:**
- Define metas claras (viaje, carro, casa)
- Calcula cuanto necesitas ahorrar mensualmente
- Usa apps para trackear progreso

## Cuentas de ahorro en Peru
- **Cuenta de ahorro tradicional:** BCP, BBVA, Interbank
- **Caja de ahorros:** Para montos menores, sin comisiones
- **Depositos a plazo fijo:** Para metas a mediano plazo (6-12 meses)

## Errores comunes
- No tener un fondo de emergencia
- Ahorrar lo que "sobra" en lugar de priorizar
- No diferenciar entre ahorro e inversion

## Consejos finales
- Empieza pequeno, pero empieza ya
- Ahorra al menos el 20% de tus ingresos
- Revisa y ajusta tus estrategias periodicamente''',
                'nivel_dificultad': 2,
                'duracion_minutos': 20,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['BCP', 'BBVA', 'Interbank', 'SBS'],
            },
            {
                'titulo': 'Todo sobre tarjetas de credito: Guia completa',
                'tipo_contenido': 'articulo',
                'categoria': 'credito',
                'descripcion': 'Aprende todo sobre tarjetas de credito en Peru: como funcionan, como usarlas responsablemente y como evitar el sobreendeudamiento.',
                'contenido': '''# Todo sobre tarjetas de credito: Guia completa

## ¿Qué es una tarjeta de crédito?
Una tarjeta de credito es una herramienta financiera que te permite hacer compras a credito. En Peru, las principales son Visa, Mastercard y Amex.

## ¿Cómo funciona?

### 1. Linea de credito
- Es el monto maximo que puedes gastar
- Se te asigna segun tu capacidad de pago
- Puede aumentar con buen historial crediticio

### 2. Fecha de corte y pago
- **Fecha de corte:** Ultimo dia del periodo de facturacion
- **Fecha de pago:** Fecha limite para pagar sin intereses
- Ejemplo: Corte dia 15, pago hasta dia 10 del mes siguiente

### 3. Opciones de pago
- **Pago total:** Pagas todo sin intereses (RECOMENDADO)
- **Pago minimo:** Solo una parte, generas intereses (EVITAR)
- **Pago diferido:** Pagas en cuotas con intereses

## Tasas y comisiones en Peru

### Tasa de interes efectiva anual (TEA)
- Promedio en Peru: 60-120% anual
- Una de las mas altas del mundo
- Por eso es crucial pagar el total cada mes

### Comisiones comunes
- Anualidad: S/. 100 - S/. 500 anual
- Mantenimiento: Variable
- Retiro de efectivo: Comision + intereses altos

## ¿Cómo usar responsablemente?

### Reglas de oro
1. **Solo gasta lo que puedes pagar en efectivo**
2. **Paga el total cada mes**
3. **Nunca retires efectivo de la tarjeta**
4. **Usa para construir historial crediticio, no para vivir a credito**

### Situaciones donde SÍ usar tarjeta
- Compras grandes planificadas (pagando total)
- Emergencias (si tienes fondo de emergencia)
- Compras online (mayor proteccion)
- Beneficios y millas (si pagas total)

### Situaciones donde NO usar tarjeta
- Si no puedes pagar el total
- Para retirar efectivo
- Para cubrir gastos mensuales basicos sin presupuesto
- Por impulso o emocion

## Construir buen historial crediticio
- Usa la tarjeta regularmente
- Paga siempre a tiempo
- Manten tu utilizacion por debajo del 30% de tu linea
- No solicites muchas tarjetas a la vez

## ¿Cómo salir de deuda?

### Metodo bola de nieve
1. Lista todas tus deudas de menor a mayor
2. Paga minimo en todas excepto la menor
3. Paga todo lo posible en la menor
4. Repite hasta salir de todas

### Metodo avalancha
1. Lista deudas por tasa de interes (mayor a menor)
2. Paga minimo en todas excepto la de mayor tasa
3. Paga todo lo posible en la de mayor tasa

## Comparacion de tarjetas en Peru
- **BCP:** Buenas promociones, app movil excelente
- **BBVA:** Buena atencion al cliente
- **Interbank:** Buenas ofertas en retail
- **Scotiabank:** Buena para viajeros

## Alertas importantes
- El pago minimo solo cubre intereses, no reduce deuda significativamente
- Los intereses se calculan diariamente sobre saldo pendiente
- Tener muchas tarjetas puede afectar tu score crediticio''',
                'nivel_dificultad': 3,
                'duracion_minutos': 25,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['BCP', 'BBVA', 'Interbank', 'Scotiabank', 'SBS'],
            },
            {
                'titulo': 'Inversiones para principiantes en Peru',
                'tipo_contenido': 'articulo',
                'categoria': 'inversion',
                'descripcion': 'Introduccion a las inversiones disponibles en Peru para jovenes que estan empezando, desde depositos a plazo hasta fondos mutuos.',
                'contenido': '''# Inversiones para principiantes en Peru

## ¿Por qué invertir?
Invertir permite que tu dinero trabaje para ti. Con inflacion del 2-3% anual en Peru, dejar dinero "debajo del colchon" hace que pierdas poder adquisitivo.

## Antes de invertir
1. **Fondo de emergencia:** 3-6 meses de gastos
2. **Sin deudas de alto interes:** Paga tarjetas primero
3. **Conocimiento basico:** Educate antes de invertir

## Opciones de inversion en Peru

### 1. Depositos a plazo fijo
- **Riesgo:** Bajo
- **Rentabilidad:** 4-7% anual
- **Plazo minimo:** 30 dias
- **Liquidez:** Baja (plazo fijo)
- **Ideal para:** Principiantes, fondos de emergencia parciales

### 2. Cuentas de ahorro remuneradas
- **Riesgo:** Muy bajo
- **Rentabilidad:** 1-3% anual
- **Liquidez:** Alta
- **Ideal para:** Fondo de emergencia

### 3. Fondos mutuos
- **Riesgo:** Variable (conservador a agresivo)
- **Rentabilidad:** 5-15% anual (historico)
- **Liquidez:** Variable (dias a semanas)
- **Ideal para:** Inversion a mediano-largo plazo

### 4. Acciones peruanas
- **Riesgo:** Alto
- **Rentabilidad:** Variable (-20% a +30% anual)
- **Liquidez:** Alta (mercado abierto)
- **Requisito:** Conocimiento avanzado, capital mayor

### 5. Bienes raices
- **Riesgo:** Medio
- **Rentabilidad:** 8-12% anual (renta) + plusvalia
- **Liquidez:** Baja
- **Requisito:** Capital significativo (S/. 50,000+)

## Reglas basicas de inversion

### 1. Diversificacion
No pongas todos los huevos en una canasta:
- Distribuye entre diferentes tipos de inversion
- Combina bajo riesgo (plazo fijo) con medio riesgo (fondos)

### 2. Horizonte de tiempo
- Corto plazo (1-2 años): Depositos a plazo, cuentas de ahorro
- Mediano plazo (3-5 años): Fondos mutuos, bienes raices
- Largo plazo (5+ años): Acciones, fondos de inversion

### 3. Tolerancia al riesgo
Evalua cuanto riesgo puedes soportar:
- **Conservador:** Depositos, cuentas de ahorro (90-100%)
- **Moderado:** 60% conservador, 40% fondos mutuos
- **Agresivo:** 40% conservador, 60% fondos/acciones

## Calculadora de inversion simple

Ejemplo: Inviertes S/. 10,000 al 6% anual por 5 años
- **Interes simple:** S/. 10,000 + (S/. 600 x 5) = S/. 13,000
- **Interes compuesto:** S/. 10,000 x (1.06)^5 = S/. 13,382

El interes compuesto es tu mejor amigo en inversion.

## Errores comunes
1. Invertir sin fondo de emergencia
2. Invertir dinero que necesitas pronto
3. No diversificar
4. Invertir por emocion (FOMO - Fear Of Missing Out)
5. No investigar antes de invertir

## Como empezar

### Paso 1: Define tu objetivo
- ¿Para qué quieres invertir? (viaje, casa, retiro)
- ¿Cuánto tiempo tienes?
- ¿Cuánto necesitas?

### Paso 2: Elige tu perfil de inversion
- Conservador, moderado o agresivo

### Paso 3: Abre cuenta de inversion
- Bancos peruanos ofrecen fondos mutuos
- Plataformas online como Renta4, Interfondos

### Paso 4: Empieza pequeno
- Invierte S/. 500-1,000 inicialmente
- Aprende mientras inviertes
- Aumenta gradualmente

## Recursos utiles
- **SBS (Superintendencia de Banca):** Regulacion y educacion
- **SMV (Superintendencia del Mercado de Valores):** Info sobre inversiones
- **Apps:** TuChanchita, Renta4, BCP Movil

## Recordatorio importante
Toda inversion tiene riesgo. Nunca inviertas mas de lo que puedes permitirte perder. La educacion financiera es tu mejor herramienta.''',
                'nivel_dificultad': 4,
                'duracion_minutos': 30,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['SBS', 'SMV', 'BCP', 'Interfondos', 'Renta4'],
            },
            {
                'titulo': 'Fraudes digitales: Protege tu dinero online',
                'tipo_contenido': 'articulo',
                'categoria': 'fraude',
                'descripcion': 'Guia completa sobre fraudes digitales comunes en Peru y como protegerte, incluyendo phishing, smishing y otros metodos de estafa.',
                'contenido': '''# Fraudes digitales: Protege tu dinero online

## Introduccion
Los fraudes digitales aumentan cada ano en Peru. En 2024, se reportaron mas de 10,000 casos. Conocer estos fraudes te protege.

## Tipos de fraudes digitales

### 1. Phishing (Correo falso)
**¿Qué es?** Correos que imitan bancos o empresas legítimas.

**¿Cómo identificar?**
- Errores ortograficos
- URLs sospechosas (.com.pe en lugar de .pe)
- Solicitud urgente de informacion
- Adjuntos sospechosos

**¿Cómo protegerte?**
- Nunca hagas clic en enlaces de correos bancarios
- Escribe la URL del banco directamente
- Verifica el remitente cuidadosamente

### 2. Smishing (Mensajes de texto falsos)
**¿Qué es?** SMS que parecen ser de tu banco.

**Ejemplo real en Peru:**
"BCP: Tu cuenta ha sido bloqueada. Verifica aqui: [enlace]"

**¿Cómo protegerte?**
- Los bancos NUNCA piden claves por SMS
- Llama directamente al banco si hay duda
- No hagas clic en enlaces de mensajes

### 3. Vishing (Llamadas falsas)
**¿Qué es?** Llamadas donde se hacen pasar por personal del banco.

**Red flags:**
- Te piden claves completas
- Solicitan transferencias urgentes
- Amenazan con cerrar tu cuenta
- Te piden instalar aplicaciones

**¿Cómo protegerte?**
- Cuelga y llama tú al banco
- Nunca des informacion por telefono
- Los bancos tienen protocolos de seguridad

### 4. Skimming (Clonación de tarjetas)
**¿Qué es?** Dispositivos que copian la información de tu tarjeta.

**¿Dónde ocurre?**
- Cajeros automaticos
- Terminales de pago en tiendas
- Gasolineras

**¿Cómo protegerte?**
- Cubre el teclado al ingresar PIN
- Revisa que no haya dispositivos sospechosos
- Usa tarjetas contactless cuando sea posible
- Revisa tus estados de cuenta regularmente

### 5. Pharming (Redirección a sitios falsos)
**¿Qué es?** Redirige tu navegador a sitios falsos aunque escribas la URL correcta.

**¿Cómo protegerte?**
- Verifica el candado (HTTPS) en la barra de direcciones
- Revisa que la URL sea exactamente la correcta
- Usa navegadores actualizados
- Evita WiFi publicos para transacciones bancarias

## Estadisticas en Peru (2024)
- Phishing: 45% de los casos
- Smishing: 30% de los casos
- Skimming: 15% de los casos
- Otros: 10% de los casos

## Reglas de oro de seguridad

### 1. Los bancos NUNCA:
- Te piden claves completas
- Te llaman para pedir transferencias urgentes
- Te piden instalar aplicaciones por telefono
- Te amenazan con cerrar tu cuenta

### 2. Tu SIEMPRE debes:
- Verificar la identidad de quien te contacta
- Usar aplicaciones oficiales del banco
- Revisar estados de cuenta regularmente
- Reportar actividad sospechosa inmediatamente

### 3. Proteccion de cuentas:
- Usa contraseas fuertes y unicas
- Activa autenticacion de dos factores (2FA)
- No compartas informacion bancaria
- Manten actualizadas tus apps bancarias

## ¿Qué hacer si fuiste víctima?

### Paso 1: Reporta inmediatamente
- Llama a tu banco en menos de 24 horas
- Bloquea tus tarjetas
- Reporta a la Policia Nacional

### Paso 2: Documenta todo
- Guarda capturas de pantalla
- Guarda correos/mensajes
- Anota fechas y horas

### Paso 3: Cambia credenciales
- Cambia todas tus contraseas
- Actualiza preguntas de seguridad
- Revisa otras cuentas

## Recursos utiles
- **Indecopi:** Para reportar fraudes comerciales
- **Policia Nacional:** Divison de Cibercrimen
- **Bancos:** Lineas de emergencia 24/7

## Conclusion
La mejor proteccion es la educacion. Conoce los fraudes comunes y siempre se escéptico de solicitudes no solicitadas de informacion financiera.''',
                'nivel_dificultad': 2,
                'duracion_minutos': 20,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['BCP', 'BBVA', 'Interbank', 'Indecopi', 'PNP'],
            },
        ]
        
        self.stdout.write(self.style.WARNING('Creando contenido educativo...'))
        for contenido in contenido_data:
            obj, created = EducationalContent.objects.get_or_create(
                titulo=contenido['titulo'],
                defaults=contenido
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creado: {obj.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {obj.titulo}'))
        
        # ============================================
        # NARRATIVA PROGRESIVA - STORYLINES
        # ============================================
        narrativa_data = [
            {
                'titulo': 'Capitulo 1: El Despertar Financiero',
                'descripcion': 'Tu viaje hacia la libertad financiera comienza aqui. Aprende los fundamentos y completa tu evaluacion inicial.',
                'capitulo_numero': 1,
                'contenido_educativo': '''# El Despertar Financiero

## Bienvenido a TuChanchita

Hola! Soy Chanchita, tu guia en este viaje hacia la libertad financiera. Hoy comenzamos una aventura que cambiara tu forma de ver el dinero.

## La Realidad

Imagina esto: estas en el ultimo ano de universidad. Tienes un trabajo part-time que te da S/. 800 al mes. Vives con tus padres, asi que no pagas alquiler... pero aun asi, al final del mes no sabes a donde se fue tu dinero.

**¿Te suena familiar?**

## El Problema

La mayoria de jovenes peruanos no aprendemos sobre finanzas personales. Nuestros padres no nos enseñaron porque ellos tampoco lo aprendieron. Entonces, repetimos los mismos errores:

- Gastamos mas de lo que ganamos
- No tenemos ahorros
- Nos endeudamos sin entender las consecuencias
- Vivimos de quincena en quincena

## La Solucion

Pero hoy, todo eso cambia. Durante los proximos capitulos, aprenderas:
- Como crear y mantener un presupuesto
- Estrategias de ahorro que funcionan
- Como usar el credito inteligentemente
- Como protegerte de fraudes digitales
- Como empezar a invertir

## Tu Primera Mision

Antes de continuar, completa tu evaluacion inicial. Esto nos ayudara a entender tu situacion actual y crear un plan personalizado para ti.

**¿Estás listo para cambiar tu futuro financiero?**

Sigue al siguiente capitulo cuando completes tu evaluacion inicial.''',
                'requisitos_desbloqueo': {},
            },
            {
                'titulo': 'Capitulo 2: Tu Primer Presupuesto',
                'descripcion': 'Aprende a crear y mantener tu primer presupuesto personal usando la regla 50-30-20.',
                'capitulo_numero': 2,
                'contenido_educativo': '''# Tu Primer Presupuesto

## El Secreto que Nadie Te Dijo

¿Sabías que las personas más exitosas financieramente no son necesariamente las que ganan más dinero? Son las que mejor lo administran.

## ¿Qué es un Presupuesto?

Un presupuesto es simplemente un plan para tu dinero. Te dice:
- Cuanto dinero entra (ingresos)
- Cuanto dinero sale (gastos)
- A donde va cada sol

## ¿Por qué es Importante?

Sin presupuesto, es como manejar un carro sin volante. Puedes llegar a algun lado, pero probablemente no sera donde quieres ir.

**Beneficios de tener presupuesto:**
- Sabes exactamente a donde va tu dinero
- Puedes planificar para tus objetivos
- Evitas gastos innecesarios
- Tienes control sobre tus finanzas

## La Regla 50-30-20

Esta es una regla simple que funciona para la mayoria:

- **50% para necesidades:** Alquiler, comida, transporte, servicios
- **30% para deseos:** Entretenimiento, salidas, compras no esenciales
- **20% para ahorro:** Fondo de emergencia, inversion, deudas

## Ejemplo Practico

Supongamos que ganas S/. 2,500 al mes:

**Necesidades (50% = S/. 1,250):**
- Alquiler: S/. 700
- Comida: S/. 400
- Transporte: S/. 100
- Servicios: S/. 50

**Deseos (30% = S/. 750):**
- Salidas: S/. 300
- Entretenimiento: S/. 200
- Compras: S/. 250

**Ahorro (20% = S/. 500):**
- Fondo de emergencia: S/. 300
- Inversion: S/. 200

## Tu Tarea

Usa la herramienta de presupuesto en TuChanchita para crear tu primer presupuesto. No tiene que ser perfecto, solo empieza.

**Recuerda:** Un presupuesto imperfecto que sigues es mejor que un presupuesto perfecto que ignoras.

En el siguiente capitulo, aprenderas como ahorrar dinero de forma efectiva.''',
                'requisitos_desbloqueo': {'tipo': 'evaluacion_completada'},
            },
            {
                'titulo': 'Capitulo 3: El Arte de Ahorrar',
                'descripcion': 'Aprende estrategias practicas para ahorrar dinero y construir un fondo de emergencia.',
                'capitulo_numero': 3,
                'contenido_educativo': '''# El Arte de Ahorrar

## La Mentalidad de Ahorro

Ahorrar no es sobre privarte de cosas. Es sobre darte opciones y libertad en el futuro.

## ¿Por qué Ahorrar?

### 1. Emergencias
La vida es impredecible. Un fondo de emergencia te protege cuando:
- Pierdes tu trabajo
- Tienes un gasto medico inesperado
- Necesitas reparar algo urgente

### 2. Oportunidades
A veces aparecen oportunidades que requieren dinero:
- Un curso que acelera tu carrera
- Una inversion que vale la pena
- Un viaje que siempre quisiste hacer

### 3. Paz Mental
Saber que tienes dinero ahorrado reduce el estres y la ansiedad financiera.

## El Fondo de Emergencia

**Objetivo:** 3-6 meses de gastos basicos

**Ejemplo:** Si gastas S/. 2,000 al mes en necesidades basicas:
- Fondo minimo: S/. 6,000
- Fondo ideal: S/. 12,000

**¿Dónde guardarlo?**
- Cuenta de ahorro separada
- Facil acceso pero no demasiado facil
- No lo toques excepto en emergencias reales

## Estrategias de Ahorro

### 1. Pagate Primero
Antes de pagar cualquier cosa, transfiere dinero a tu cuenta de ahorro. Tratalo como un gasto fijo.

### 2. El Reto de las 52 Semanas
- Semana 1: S/. 1
- Semana 2: S/. 2
- Semana 3: S/. 3
- ...
- Semana 52: S/. 52
- **Total: S/. 1,378 en un ano**

### 3. Ahorro Automatico
Configura transferencias automaticas el dia que recibes tu sueldo. Si no lo ves, no lo gastaras.

### 4. Regla de las 24 Horas
Antes de comprar algo no esencial, espera 24 horas. Muchas veces, la emocion pasa y te das cuenta que no lo necesitabas.

## Reducir Gastos sin Sufrir

No se trata de vivir como un monje, sino de ser inteligente:

- **Comida:** Cocina mas en casa, lleva lonchera
- **Transporte:** Usa transporte publico cuando sea posible
- **Entretenimiento:** Busca actividades gratuitas, comparte cuentas de streaming
- **Compras:** Espera ofertas, compara precios

## Tu Desafio

Esta semana, identifica 3 gastos que puedas reducir o eliminar. Usa ese dinero para empezar tu fondo de emergencia.

En el siguiente capitulo, hablaremos sobre credito y como usarlo inteligentemente.''',
                'requisitos_desbloqueo': {'tipo': 'presupuesto_creado'},
            },
            {
                'titulo': 'Capitulo 4: Credito: ¿Amigo o Enemigo?',
                'descripcion': 'Aprende como usar el credito de forma inteligente y evitar el sobreendeudamiento.',
                'capitulo_numero': 4,
                'contenido_educativo': '''# Credito: Amigo o Enemigo?

## La Paradoja del Credito

El credito puede ser tu mejor aliado o tu peor enemigo. La diferencia esta en como lo uses.

## ¿Qué es el Crédito?

El credito es dinero que alguien te presta con la promesa de que lo devolveras, generalmente con intereses.

**Tipos comunes en Peru:**
- Tarjetas de credito
- Prestamos personales
- Prestamos de vehiculo
- Prestamos hipotecarios

## El Buen Credito

El credito es bueno cuando:
- Te ayuda a construir historial crediticio
- Te permite hacer compras grandes planificadas (pagando total)
- Te da proteccion en compras (garantias extendidas)
- Te ofrece beneficios (millas, cashback)

## El Mal Credito

El credito es malo cuando:
- Lo usas para vivir por encima de tus posibilidades
- Pagas solo el minimo y acumulas intereses
- No tienes control sobre tus gastos
- Te endeudas mas alla de tu capacidad

## Las Tarjetas de Credito en Peru

### Tasas de Interes
- Promedio: 60-120% anual (muy altas!)
- Por eso es CRUCIAL pagar el total cada mes

### Comisiones
- Anualidad: S/. 100-500
- Retiro de efectivo: Comision + intereses altos
- Mantenimiento: Variable

## Reglas de Oro del Credito

### 1. Solo gasta lo que puedes pagar en efectivo
Si no tienes el dinero en tu cuenta, no lo gastes con tarjeta.

### 2. Pagar el total cada mes
El pago minimo solo cubre intereses. Nunca reduce la deuda real.

### 3. Nunca retires efectivo de la tarjeta
Es la forma mas cara de obtener dinero. Evitala a toda costa.

### 4. Usa para construir historial
Usa la tarjeta regularmente pero siempre pagando el total.

## ¿Cómo Salir de Deuda?

Si ya estas endeudado, no te desanimes. Tienes opciones:

### Metodo Bola de Nieve
1. Lista todas tus deudas de menor a mayor
2. Paga minimo en todas excepto la menor
3. Paga todo lo posible en la menor
4. Repite hasta salir de todas

### Metodo Avalancha
1. Lista deudas por tasa de interes (mayor a menor)
2. Paga minimo en todas excepto la de mayor tasa
3. Paga todo lo posible en la de mayor tasa

## Tu Mision

Si tienes tarjeta de credito:
- Revisa cuanto debes actualmente
- Crea un plan para pagarla
- Comprometete a pagar el total cada mes de ahora en adelante

En el siguiente capitulo, aprenderas como protegerte de fraudes digitales.''',
                'requisitos_desbloqueo': {'tipo': 'ahorro_iniciado'},
            },
            {
                'titulo': 'Capitulo 5: Proteccion Contra Fraudes',
                'descripcion': 'Protege tu dinero y tu identidad aprendiendo sobre fraudes digitales comunes.',
                'capitulo_numero': 5,
                'contenido_educativo': '''# Proteccion Contra Fraudes

## Un Mundo Digital, Nuevos Riesgos

Vivimos en la era digital. Compras online, pagos moviles, banca electronica... pero tambien nuevos tipos de estafas.

## Los Fraudes Mas Comunes en Peru

### 1. Phishing (Correos Falsos)
Correos que parecen ser de tu banco pero son falsos.

**Señales de alerta:**
- Errores ortograficos
- URLs sospechosas
- Solicitudes urgentes de informacion
- Amenazas de cerrar tu cuenta

### 2. Smishing (Mensajes Falsos)
SMS que parecen ser de tu banco.

**Recuerda:** Los bancos NUNCA te piden claves por mensaje de texto.

### 3. Vishing (Llamadas Falsas)
Llamadas donde se hacen pasar por personal del banco.

**Red flags:**
- Te piden claves completas
- Solicitan transferencias urgentes
- Te piden instalar aplicaciones

### 4. Skimming (Clonación)
Dispositivos que copian la información de tu tarjeta en cajeros o tiendas.

**¿Cómo protegerte?**
- Cubre el teclado al ingresar PIN
- Revisa que no haya dispositivos sospechosos
- Usa tarjetas contactless cuando sea posible

## Reglas de Seguridad

### Los Bancos NUNCA:
- Te piden claves completas
- Te llaman para pedir transferencias urgentes
- Te piden instalar aplicaciones por telefono
- Te amenazan con cerrar tu cuenta

### Tu SIEMPRE debes:
- Verificar la identidad de quien te contacta
- Usar aplicaciones oficiales del banco
- Revisar estados de cuenta regularmente
- Reportar actividad sospechosa inmediatamente

## Proteccion de Cuentas

### 1. Contraseas Fuertes
- Minimo 12 caracteres
- Combinacion de letras, numeros y simbolos
- Unica para cada cuenta
- Cambiala regularmente

### 2. Autenticacion de Dos Factores (2FA)
Activa 2FA en todas tus cuentas importantes. Agrega una capa extra de seguridad.

### 3. Aplicaciones Oficiales
Solo descarga aplicaciones bancarias desde tiendas oficiales (App Store, Google Play).

### 4. WiFi Publicos
NUNCA hagas transacciones bancarias en WiFi publicos. Usa tu plan de datos moviles.

## Que Hacer si Fuiste Victima

### Paso 1: Reporta Inmediatamente
- Llama a tu banco en menos de 24 horas
- Bloquea tus tarjetas
- Reporta a la Policia Nacional

### Paso 2: Documenta Todo
- Guarda capturas de pantalla
- Guarda correos/mensajes
- Anota fechas y horas

### Paso 3: Cambia Credenciales
- Cambia todas tus contraseas
- Actualiza preguntas de seguridad
- Revisa otras cuentas

## Tu Tarea

Esta semana:
1. Activa 2FA en tu cuenta bancaria
2. Revisa tus ultimos 3 estados de cuenta
3. Cambia tu contrasea bancaria si tiene menos de 12 caracteres

En el siguiente capitulo, aprenderas los fundamentos de inversion.''',
                'requisitos_desbloqueo': {'tipo': 'credito_entendido'},
            },
            {
                'titulo': 'Capitulo 6: Tu Futuro Financiero',
                'descripcion': 'Completa tu viaje aprendiendo sobre inversion y planificacion a largo plazo.',
                'capitulo_numero': 6,
                'contenido_educativo': '''# Tu Futuro Financiero

## Has Llegado Lejos

Felicidades! Has completado los fundamentos de la educacion financiera. Ahora tienes las herramientas para tomar control de tu futuro.

## Resumen del Viaje

A lo largo de estos capitulos, aprendiste:

1. **Presupuesto:** Planificar tu dinero
2. **Ahorro:** Construir un fondo de emergencia
3. **Credito:** Usarlo inteligentemente
4. **Proteccion:** Defenderte de fraudes
5. **Y ahora... Inversion**

## ¿Por qué Invertir?

Ahorrar es bueno, pero invertir es mejor. Con inflacion del 2-3% anual en Peru, dejar dinero "debajo del colchon" hace que pierdas poder adquisitivo.

**La inversion permite:**
- Que tu dinero crezca con el tiempo
- Alcanzar objetivos a largo plazo
- Construir riqueza para el futuro

## Opciones de Inversion en Peru

### Para Principiantes:
- **Depositos a plazo:** 4-7% anual, bajo riesgo
- **Cuentas de ahorro remuneradas:** 1-3% anual, muy bajo riesgo
- **Fondos mutuos:** 5-15% anual, riesgo variable

### Para Intermedios:
- Acciones peruanas
- Fondos de inversion
- Bienes raices (con capital significativo)

## Reglas Basicas

1. **Diversificacion:** No pongas todos los huevos en una canasta
2. **Horizonte de tiempo:** Define cuanto tiempo tienes
3. **Tolerancia al riesgo:** Conoce cuanto riesgo puedes soportar

## Antes de Invertir

Asegurate de tener:
- ✅ Fondo de emergencia completo
- ✅ Sin deudas de alto interes
- ✅ Conocimiento basico sobre inversion
- ✅ Objetivos claros

## El Poder del Interes Compuesto

Ejemplo: Inviertes S/. 10,000 al 6% anual por 10 años
- Sin reinvertir: S/. 16,000
- Con interes compuesto: S/. 17,908

El tiempo es tu mejor aliado en inversion.

## Tu Camino Adelante

La educacion financiera es un viaje, no un destino. Sigue aprendiendo:

1. Lee sobre finanzas regularmente
2. Sigue a expertos confiables
3. Practica lo que aprendes
4. Ajusta tu estrategia cuando sea necesario

## Recursos Continuos

- Biblioteca educativa en TuChanchita
- Contenido de prevencion de fraudes
- Alertas y recomendaciones personalizadas
- Tu progreso individual

## El Compromiso

Ahora que sabes mas, tienes la responsabilidad de:
- Tomar mejores decisiones financieras
- Compartir conocimiento con otros
- Construir un futuro mejor para ti y tu familia

**El viaje apenas comienza. ¿Estás listo para construir tu futuro financiero?**

---

## Felicidades!

Has completado todos los capitulos de la narrativa. Eres ahora parte de una comunidad de jovenes que esta tomando control de sus finanzas.

**Sigue aprendiendo, sigue creciendo, sigue prosperando.**

- Chanchita, tu guia financiera''',
                'requisitos_desbloqueo': {'tipo': 'proteccion_implementada'},
            },
        ]
        
        self.stdout.write(self.style.WARNING('Creando narrativa progresiva...'))
        for capitulo in narrativa_data:
            obj, created = Storyline.objects.get_or_create(
                titulo=capitulo['titulo'],
                defaults=capitulo
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creado: {obj.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {obj.titulo}'))
        
        # ============================================
        # CONTENIDO ADICIONAL DE FRAUDES
        # ============================================
        fraudes_adicionales = [
            {
                'titulo': 'Robo de Identidad: Protege tu Informacion Personal',
                'tipo_fraude': 'identity_theft',
                'descripcion': 'El robo de identidad ocurre cuando alguien usa tu informacion personal sin permiso. Aprende como protegerte y que hacer si eres victima.',
                'ejemplo_real': '''Caso Real en Lima (2023):
Una estudiante universitaria compartio su DNI en una encuesta online falsa. Los estafadores usaron su informacion para:
- Abrir cuentas bancarias a su nombre
- Solicitar tarjetas de credito
- Realizar compras fraudulentas

Cuando intento abrir una cuenta bancaria real, descubrio que ya habia una cuenta "suya" con deudas. Tardo 8 meses en limpiar su historial crediticio.

**Leccion:** Nunca compartas tu DNI completo en internet, especialmente en sitios no verificados.''',
                'como_protegerse': '''
## ¿Cómo Protegerte?

### 1. Proteccion de Documentos
- Nunca compartas tu DNI completo en internet
- Manten documentos fisicos en lugar seguro
- Destruye documentos antiguos correctamente

### 2. Informacion en Redes Sociales
- No compartas informacion personal publica
- Configura privacidad en tus redes
- No aceptes solicitudes de personas desconocidas

### 3. Monitoreo Regular
- Revisa tu historial crediticio en la SBS cada 6 meses
- Monitorea tus estados de cuenta bancarios
- Activa alertas de transacciones

### 4. Uso Seguro de Internet
- No uses WiFi publicos para transacciones importantes
- Verifica que los sitios sean HTTPS
- No compartas informacion en sitios no verificados

## Que Hacer si Eres Victima

1. **Reporta inmediatamente** a la Policia Nacional (Divison de Cibercrimen)
2. **Contacta a las instituciones** donde se uso tu identidad
3. **Congela tu credito** temporalmente
4. **Documenta todo** para el proceso legal
5. **Reporta a Indecopi** si es fraude comercial''',
                'nivel_dificultad': 3,
            },
        ]
        
        self.stdout.write(self.style.WARNING('Agregando contenido adicional de fraudes...'))
        for fraude in fraudes_adicionales:
            obj, created = FraudPreventionContent.objects.get_or_create(
                titulo=fraude['titulo'],
                defaults=fraude
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creado: {obj.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {obj.titulo}'))
        
        self.stdout.write(self.style.SUCCESS('\nPoblacion completada exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'- Contenido educativo: {EducationalContent.objects.count()} items'))
        self.stdout.write(self.style.SUCCESS(f'- Capitulos de narrativa: {Storyline.objects.count()} items'))
        self.stdout.write(self.style.SUCCESS(f'- Contenido de fraudes: {FraudPreventionContent.objects.count()} items'))

