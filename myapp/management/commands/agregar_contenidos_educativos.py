"""
Comando para agregar 15 contenidos educativos adicionales
"""
from django.core.management.base import BaseCommand
from myapp.models import EducationalContent


class Command(BaseCommand):
    help = 'Agrega 15 contenidos educativos adicionales para el logro Bibliotecario'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Agregando contenidos educativos adicionales...'))
        
        nuevos_contenidos = [
            {
                'titulo': 'Planificacion financiera para estudiantes universitarios',
                'tipo_contenido': 'articulo',
                'categoria': 'presupuesto',
                'descripcion': 'Guia practica para manejar finanzas durante la universidad en Peru, incluyendo becas, trabajos part-time y gastos academicos.',
                'contenido': '''# Planificacion financiera para estudiantes universitarios

## La Realidad del Estudiante
Como estudiante en Peru, probablemente tienes ingresos limitados y gastos academicos constantes. La planificacion financiera es crucial.

## Ingresos Comunes de Estudiantes
- Beca o apoyo familiar
- Trabajo part-time (S/. 500-1,200/mes)
- Practicas pre-profesionales
- Freelance o trabajos esporadicos

## Gastos Academicos
- Matricula y pensiones
- Materiales y libros
- Transporte a la universidad
- Alimentacion
- Fotocopias y materiales

## Estrategias de Ahorro
1. **Aprovecha descuentos estudiantiles** en transporte, cines, restaurantes
2. **Compra libros usados** o usa bibliotecas
3. **Cocina en casa** en lugar de comer fuera
4. **Comparte gastos** con compañeros (transporte, materiales)

## Presupuesto Mensual Ejemplo
- Ingresos: S/. 800 (trabajo part-time)
- Pension: S/. 300
- Transporte: S/. 100
- Alimentacion: S/. 250
- Materiales: S/. 50
- Ahorro: S/. 100

## Consejos Importantes
- Evita tarjetas de credito hasta tener ingresos estables
- Ahorra para emergencias academicas
- Busca becas y oportunidades de financiamiento
- Considera trabajos relacionados con tu carrera''',
                'nivel_dificultad': 1,
                'duracion_minutos': 12,
                'incluye_ejemplos_peru': True,
            },
            {
                'titulo': 'Como leer y entender tu estado de cuenta bancario',
                'tipo_contenido': 'articulo',
                'categoria': 'educacion',
                'descripcion': 'Aprende a interpretar cada seccion de tu estado de cuenta bancario en Peru y detectar cargos no autorizados.',
                'contenido': '''# Como leer tu estado de cuenta bancario

## Partes del Estado de Cuenta

### 1. Informacion Personal
- Nombre y numero de cuenta
- Periodo del estado
- Direccion registrada

### 2. Resumen de Movimientos
- Saldo anterior
- Depositos y creditos
- Retiros y debitos
- Saldo actual

### 3. Detalle de Transacciones
Cada movimiento muestra:
- Fecha
- Descripcion
- Monto (cargo o abono)
- Saldo despues de la transaccion

## Conceptos Importantes

### Comisiones
- Mantenimiento de cuenta
- Retiros en otros bancos
- Transferencias
- Consultas en ventanilla

### Intereses
- Intereses ganados (cuentas de ahorro)
- Intereses pagados (creditos)

## Como Revisar tu Estado
1. Verifica todos los movimientos
2. Confirma que reconoces cada transaccion
3. Revisa comisiones y cargos
4. Compara con tus registros personales

## Señales de Alerta
- Movimientos que no reconoces
- Comisiones inesperadas
- Montos que no coinciden
- Fechas incorrectas

## Que Hacer si Encuentras Errores
1. Contacta al banco inmediatamente
2. Guarda el estado de cuenta
3. Presenta una reclamacion formal
4. Si no resuelven, contacta a la SBS''',
                'nivel_dificultad': 1,
                'duracion_minutos': 10,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['SBS'],
            },
            {
                'titulo': 'Fondos mutuos: Inversion accesible para jovenes',
                'tipo_contenido': 'articulo',
                'categoria': 'inversion',
                'descripcion': 'Introduccion a los fondos mutuos en Peru, como funcionan y como empezar a invertir con poco capital.',
                'contenido': '''# Fondos mutuos: Inversion accesible

## ¿Qué son los Fondos Mutuos?
Son instrumentos de inversion donde varias personas juntan su dinero para invertir en conjunto, administrado por profesionales.

## Ventajas para Jovenes
- **Bajo capital inicial:** Desde S/. 100-500
- **Diversificacion automatica**
- **Administracion profesional**
- **Liquidez relativa**

## Tipos de Fondos en Peru

### 1. Fondos de Renta Fija
- Invierten en bonos y depositos
- Menor riesgo, menor rentabilidad
- Ideal para: Principiantes, objetivos a corto plazo

### 2. Fondos de Renta Variable
- Invierten en acciones
- Mayor riesgo, mayor potencial
- Ideal para: Objetivos a largo plazo

### 3. Fondos Balanceados
- Mezcla de renta fija y variable
- Riesgo moderado
- Ideal para: Perfiles intermedios

## Como Empezar
1. Define tu objetivo y plazo
2. Evalua tu perfil de riesgo
3. Investiga fondos disponibles en Peru
4. Lee el prospecto de inversion
5. Abre una cuenta en una administradora

## Costos a Considerar
- Comision de administracion (1-3% anual)
- Comision de suscripcion (0-2%)
- Comision de rescate (si retiras antes de plazo)

## Consejos
- Empieza con montos pequenos
- Invierte regularmente (promedio de costo)
- No inviertas dinero que necesites pronto
- Revisa el rendimiento periodicamente
- Diversifica entre diferentes fondos''',
                'nivel_dificultad': 2,
                'duracion_minutos': 18,
                'incluye_ejemplos_peru': True,
            },
            {
                'titulo': 'Score crediticio: Como construir y mantener un buen historial',
                'tipo_contenido': 'articulo',
                'categoria': 'credito',
                'descripcion': 'Guia completa sobre el score crediticio en Peru, como se calcula y estrategias para mejorarlo.',
                'contenido': '''# Score Crediticio en Peru

## ¿Qué es el Score Crediticio?
Es un numero que representa tu capacidad de pago y riesgo crediticio. En Peru, va de 0 a 1000 puntos.

## ¿Por qué es Importante?
- Determina si te aprueban creditos
- Afecta las tasas de interes que te ofrecen
- Puede requerirse para alquileres
- Algunos empleadores lo revisan

## Como se Calcula

### Factores Principales
1. **Historial de pagos (35%)**
   - Pagos puntuales mejoran el score
   - Atrasos lo reducen significativamente

2. **Utilizacion de credito (30%)**
   - Usar menos del 30% de tu linea es ideal
   - Usar mas del 80% es negativo

3. **Antiguedad del credito (15%)**
   - Cuentas antiguas son positivas
   - No cierres cuentas antiguas innecesariamente

4. **Tipos de credito (10%)**
   - Mezcla de tarjetas y prestamos es positivo

5. **Consultas recientes (10%)**
   - Muchas consultas en poco tiempo es negativo

## Como Mejorar tu Score

### Acciones Inmediatas
- Paga todas tus deudas a tiempo
- Reduce el uso de tarjetas de credito
- No solicites muchos creditos a la vez

### Estrategias a Mediano Plazo
- Manten cuentas antiguas abiertas
- Usa credito regularmente pero responsablemente
- Diversifica tipos de credito

## Como Consultar tu Score
- Central de Riesgos del SBS (gratis, una vez al ano)
- Empresas privadas (Equifax, TransUnion)
- Algunos bancos lo muestran en sus apps

## Errores Comunes
- Cerrar tarjetas antiguas
- Pagar solo el minimo constantemente
- No revisar tu reporte crediticio
- Ignorar deudas pequenas

## Recuperacion de Score
Si tienes un mal score:
1. Paga todas las deudas pendientes
2. Manten pagos puntuales por 6-12 meses
3. Reduce utilizacion de credito
4. El tiempo es tu aliado - mejora gradualmente''',
                'nivel_dificultad': 2,
                'duracion_minutos': 20,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['SBS', 'Equifax', 'TransUnion'],
            },
            {
                'titulo': 'Seguros basicos: Que necesitas y que no',
                'tipo_contenido': 'articulo',
                'categoria': 'riesgo',
                'descripcion': 'Guia sobre seguros esenciales para jovenes en Peru y cuales son realmente necesarios.',
                'contenido': '''# Seguros Basicos: Que Necesitas

## Seguros Esenciales

### 1. SOAT (Obligatorio)
- **Que cubre:** Accidentes de transito
- **Costo:** S/. 50-150 anual
- **Necesario si:** Tienes vehiculo
- **Por que:** Es obligatorio por ley

### 2. EPS (Seguro de Salud)
- **Que cubre:** Atencion medica basica
- **Costo:** Variable segun plan
- **Necesario si:** No tienes seguro del trabajo
- **Por que:** Emergencias medicas son costosas

### 3. Seguro de Vida (Opcional para jovenes)
- **Necesario si:** Tienes dependientes
- **No necesario si:** Eres soltero sin hijos

## Seguros que Puedes Considerar

### Seguro de Vehiculo
- Cubre danos a tu auto
- Costo: S/. 500-2000 anual
- Considera si: Tu vehiculo tiene valor significativo

### Seguro de Renta
- Cubre ingresos si no puedes trabajar
- Costo: Variable
- Considera si: Eres independiente o freelance

## Seguros que Probablemente NO Necesitas

### Seguro de Celular
- Generalmente no vale la pena
- Mejor: Fondo de emergencia

### Seguros de Credito
- A menudo innecesarios
- Lee bien las exclusiones

## Como Elegir un Seguro
1. Evalua tu riesgo real
2. Compara opciones
3. Lee las exclusiones cuidadosamente
4. Verifica la reputacion de la aseguradora
5. No compres por presion

## Consejos
- No asegures lo que puedes pagar de tu bolsillo
- Revisa tu seguro anualmente
- Asegura lo que no puedes reemplazar facilmente
- Considera deducibles mas altos para primas mas bajas''',
                'nivel_dificultad': 2,
                'duracion_minutos': 15,
                'incluye_ejemplos_peru': True,
            },
            {
                'titulo': 'Apps financieras: Herramientas digitales para manejar tu dinero',
                'tipo_contenido': 'articulo',
                'categoria': 'educacion',
                'descripcion': 'Revision de aplicaciones financieras disponibles en Peru y como usarlas para mejorar tus finanzas.',
                'contenido': '''# Apps Financieras en Peru

## Categorias de Apps

### 1. Apps de Bancos
**BCP, BBVA, Interbank, Scotiabank**
- Ventajas: Seguras, oficiales
- Funciones: Transferencias, pagos, consultas
- Uso: Gestion diaria de cuentas

### 2. Apps de Presupuesto
**TuChanchita, YNAB, Mint**
- Ventajas: Tracking de gastos, presupuestos
- Funciones: Categorizacion, reportes
- Uso: Control financiero personal

### 3. Apps de Inversion
**Caja Sullana, Credicorp Capital**
- Ventajas: Acceso a inversiones
- Funciones: Fondos mutuos, depositos
- Uso: Hacer crecer tu dinero

### 4. Apps de Pagos
**Yape, Plin, Tunki**
- Ventajas: Pagos rapidos
- Funciones: Transferencias, pagos
- Uso: Transacciones diarias

## Seguridad en Apps Financieras

### Mejores Practicas
- Usa contraseas fuertes
- Activa autenticacion de dos factores
- No uses WiFi publico
- Manten apps actualizadas
- Revisa permisos de la app

### Señales de Alerta
- Apps no oficiales
- Solicitudes de permisos excesivos
- Resenas negativas
- Sin certificacion bancaria

## Como Elegir una App
1. Verifica que sea oficial
2. Lee las politicas de privacidad
3. Revisa las comisiones
4. Prueba la interfaz
5. Verifica soporte al cliente

## Consejos de Uso
- No guardes contraseas en el telefono
- Revisa movimientos regularmente
- Usa apps oficiales de bancos
- Configura alertas de transacciones
- No compartas codigos de verificacion''',
                'nivel_dificultad': 1,
                'duracion_minutos': 12,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['BCP', 'BBVA', 'Interbank', 'Scotiabank'],
            },
            {
                'titulo': 'Inflacion: Como afecta tu dinero y que hacer',
                'tipo_contenido': 'articulo',
                'categoria': 'educacion',
                'descripcion': 'Explicacion sobre la inflacion en Peru y como proteger tu poder adquisitivo.',
                'contenido': '''# Inflacion: Como Afecta tu Dinero

## ¿Qué es la Inflacion?
Es el aumento generalizado de precios en la economia. En Peru, la meta del Banco Central es mantenerla entre 1% y 3% anual.

## Como Afecta tu Dinero

### Ejemplo Practico
Si la inflacion es 3% anual:
- S/. 100 hoy = S/. 97 de poder adquisitivo en un ano
- Tu dinero "pierde valor" si no lo inviertes

### Impacto Real
- Los precios suben
- Tu sueldo compra menos
- Ahorros sin inversion pierden valor

## Como Protegerte

### 1. Invierte tu Dinero
- Depositos a plazo (4-7% anual)
- Fondos mutuos
- Inversiones que superen la inflacion

### 2. Ajusta tu Presupuesto
- Revisa gastos regularmente
- Busca alternativas mas economicas
- Prioriza necesidades sobre deseos

### 3. Negocia Aumentos
- Si la inflacion sube, tu sueldo deberia subir
- Documenta el aumento del costo de vida
- Presenta argumentos basados en datos

## Inflacion en Peru (Historico)
- 2020-2023: 2-8% anual
- Meta del BCRP: 1-3%
- Promedio historico: 3-4%

## Estrategias Ante Inflacion

### Corto Plazo
- Reduce gastos no esenciales
- Busca ofertas y descuentos
- Compara precios antes de comprar

### Largo Plazo
- Invierte en activos que crezcan
- Diversifica tus inversiones
- Educate sobre finanzas

## Conceptos Relacionados

### Deflacion
- Caida de precios
- Puede ser negativa (menos consumo)
- Rara en Peru

### Estanflacion
- Inflacion + estancamiento economico
- Situacion dificil
- Requiere estrategias especiales

## Conclusion
La inflacion es inevitable, pero puedes protegerte invirtiendo inteligentemente y ajustando tu estilo de vida.''',
                'nivel_dificultad': 2,
                'duracion_minutos': 15,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['BCRP'],
            },
            {
                'titulo': 'Gastos hormiga: Como identificarlos y eliminarlos',
                'tipo_contenido': 'articulo',
                'categoria': 'presupuesto',
                'descripcion': 'Aprende a identificar y eliminar los pequenos gastos que consumen tu presupuesto sin que te des cuenta.',
                'contenido': '''# Gastos Hormiga: El Enemigo Silencioso

## ¿Qué son los Gastos Hormiga?
Son pequenos gastos frecuentes que parecen insignificantes pero suman grandes cantidades al final del mes.

## Ejemplos Comunes
- Cafe diario: S/. 5 x 30 = S/. 150/mes
- Snacks: S/. 3 x 20 = S/. 60/mes
- Taxi/Uber: S/. 10 x 15 = S/. 150/mes
- Comida fuera: S/. 20 x 10 = S/. 200/mes
- **Total: S/. 560/mes = S/. 6,720/ano**

## Como Identificarlos

### 1. Rastrea Todos tus Gastos
- Anota cada compra por 1 mes
- Usa apps de presupuesto
- Revisa estados de cuenta

### 2. Categoriza
- Identifica gastos repetitivos
- Suma los pequenos gastos
- Calcula el total mensual

### 3. Evalua Necesidad
- ¿Realmente necesitas esto?
- ¿Puedes hacerlo mas barato?
- ¿Cada cuanto lo compras?

## Estrategias para Eliminarlos

### 1. Alternativas Mas Economicas
- Cafe: Hazlo en casa (S/. 0.50 vs S/. 5)
- Comida: Cocina mas, come fuera menos
- Transporte: Usa transporte publico cuando sea posible

### 2. Regla de las 24 Horas
- Espera 24 horas antes de compras no esenciales
- Muchas veces la emocion pasa

### 3. Presupuesto para "Gustos"
- Asigna un monto mensual
- Cuando se acaba, se acabo
- Prioriza lo que realmente disfrutas

### 4. Desafios de Ahorro
- Reto de no gastar en X por 30 dias
- Guarda el dinero ahorrado
- Ve el progreso tangible

## Calculadora de Gastos Hormiga
Multiplica tu gasto diario por:
- 30 = Gasto mensual
- 365 = Gasto anual
- 10 = Gasto en 10 anos

**Ejemplo:** S/. 5 diarios en cafe
- Mensual: S/. 150
- Anual: S/. 1,825
- En 10 anos: S/. 18,250

## No Elimines Todo
- Algunos gastos traen felicidad
- El objetivo es ser consciente
- Prioriza lo que realmente valoras

## Consejos Finales
- No todos los gastos pequenos son malos
- El problema es la falta de conciencia
- Pequenos cambios = grandes resultados
- Usa el dinero ahorrado para tus objetivos''',
                'nivel_dificultad': 1,
                'duracion_minutos': 12,
                'incluye_ejemplos_peru': True,
            },
            {
                'titulo': 'Prestamos estudiantiles: Todo lo que debes saber',
                'tipo_contenido': 'articulo',
                'categoria': 'credito',
                'descripcion': 'Guia completa sobre prestamos estudiantiles en Peru, cuando son una buena opcion y como manejarlos.',
                'contenido': '''# Prestamos Estudiantiles en Peru

## Tipos de Prestamos Estudiantiles

### 1. Prestamos del Estado
- **Pronabec:** Para estudios superiores
- **Beca 18:** No es prestamo, es beca
- Ventajas: Tasas preferenciales
- Requisitos: Buen rendimiento academico

### 2. Prestamos Bancarios
- Ofrecidos por bancos privados
- Para matricula y pensiones
- Tasas variables segun el banco

### 3. Prestamos de Instituciones Educativas
- Algunas universidades ofrecen financiamiento
- Condiciones especificas
- Revisa terminos cuidadosamente

## Cuando Considerar un Prestamo

### Situaciones Apropiadas
- Inversion en educacion de calidad
- Mejora significativa de ingresos futuros
- No tienes otras opciones de financiamiento
- Puedes pagar las cuotas

### Situaciones a Evitar
- Solo para "vivir mejor" durante estudios
- Sin plan de pago claro
- Tasas de interes muy altas
- Ya tienes otras deudas

## Como Evaluar un Prestamo

### Factores a Considerar
1. **Tasa de interes (TEA)**
   - Compara entre opciones
   - Prefiere tasas fijas

2. **Plazo de pago**
   - Plazos largos = mas intereses
   - Plazos cortos = cuotas altas

3. **Comisiones**
   - Seguro de desgravamen
   - Comisiones de administracion

4. **Condiciones especiales**
   - Periodo de gracia
   - Reduccion por buen rendimiento

## Estrategias de Pago

### 1. Paga Mientras Estudias
- Reduce intereses acumulados
- Si puedes, paga intereses al menos

### 2. Pago Anticipado
- Reduce el capital pendiente
- Ahorra en intereses totales

### 3. Consolidacion
- Si tienes multiples prestamos
- Unifica en uno con mejor tasa

## Alternativas al Prestamo

### 1. Becas y Ayudas
- Busca becas completas
- Becas parciales
- Ayudas economicas

### 2. Trabajo y Estudio
- Trabajo part-time
- Practicas pre-profesionales
- Freelance

### 3. Ahorro Previo
- Ahorra antes de estudiar
- Planifica con anticipacion

## Consejos Importantes
- Lee todos los terminos
- Calcula el costo total del prestamo
- Asegurate de poder pagar
- Considera el retorno de inversion
- No tomes mas de lo necesario''',
                'nivel_dificultad': 2,
                'duracion_minutos': 18,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['Pronabec'],
            },
            {
                'titulo': 'Criptomonedas: Riesgos y oportunidades para jovenes',
                'tipo_contenido': 'articulo',
                'categoria': 'inversion',
                'descripcion': 'Introduccion a las criptomonedas, riesgos, regulacion en Peru y si son adecuadas para jovenes.',
                'contenido': '''# Criptomonedas: Riesgos y Oportunidades

## ¿Qué son las Criptomonedas?
Son monedas digitales descentralizadas que usan tecnologia blockchain. Las mas conocidas son Bitcoin y Ethereum.

## Estado en Peru
- No son moneda de curso legal
- No estan reguladas por el BCRP
- Operan en un marco legal ambiguo
- Algunos exchanges operan en el pais

## Riesgos Importantes

### 1. Volatilidad Extrema
- Precios pueden subir/bajar 20-50% en dias
- No es para dinero que necesitas pronto
- Puedes perder todo tu capital

### 2. Falta de Regulacion
- No hay proteccion del consumidor
- Exchanges pueden cerrar
- Fraudes comunes

### 3. Complejidad Tecnica
- Requiere conocimiento tecnico
- Riesgo de perder acceso a tu billetera
- Phishing y hackeos frecuentes

### 4. Uso Ilicito
- Algunos usan para actividades ilegales
- Puede afectar tu reputacion
- Regulaciones pueden cambiar

## Oportunidades

### 1. Potencial de Crecimiento
- Algunos han visto ganancias significativas
- Tecnologia con futuro potencial
- Adopcion creciente

### 2. Diversificacion
- Activo no correlacionado con mercados tradicionales
- Puede ser parte de una cartera diversificada

## Si Decides Invertir

### Reglas de Oro
1. **Solo invierte lo que puedes perder completamente**
2. **No mas del 5% de tu cartera**
3. **Educate mucho antes**
4. **Usa exchanges reconocidos**
5. **Almacena en billeteras seguras**

### Como Empezar (Si decides hacerlo)
1. Investiga extensivamente
2. Empieza con montos muy pequenos
3. Usa exchanges regulados internacionalmente
4. Aprende sobre seguridad (billeteras, 2FA)
5. No inviertas por FOMO (miedo a perderte)

## Alternativas Mas Seguras
- Inversiones tradicionales (fondos mutuos)
- Depositos a plazo
- Acciones de empresas establecidas
- Inversiones reguladas

## Conclusion
Las criptomonedas son de ALTO RIESGO. Solo considera si:
- Entiendes completamente los riesgos
- Puedes perder todo el dinero
- Es una porcion muy pequena de tu cartera
- Tienes conocimiento tecnico adecuado

**Para la mayoria de jovenes, hay opciones mas seguras y reguladas.**''',
                'nivel_dificultad': 3,
                'duracion_minutos': 20,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['BCRP'],
            },
            {
                'titulo': 'Emprendimiento: Finanzas para tu primer negocio',
                'tipo_contenido': 'articulo',
                'categoria': 'educacion',
                'descripcion': 'Guia basica de finanzas para jovenes que quieren emprender en Peru.',
                'contenido': '''# Finanzas para Emprendedores Jovenes

## Planificacion Financiera del Negocio

### 1. Capital Inicial
- Calcula cuanto necesitas para empezar
- Incluye: inventario, equipo, marketing, reserva
- No uses todo tu dinero, guarda reserva personal

### 2. Flujo de Caja
- Ingresos esperados vs gastos
- Proyeccion mensual por 6-12 meses
- Identifica meses dificiles

### 3. Separacion de Finanzas
- Cuenta bancaria separada para el negocio
- No mezcles dinero personal y del negocio
- Lleva contabilidad basica

## Fuentes de Financiamiento

### 1. Ahorros Propios
- Ventaja: Sin deudas
- Desventaja: Riesgo personal

### 2. Prestamos Personales
- Revisa tasas cuidadosamente
- Asegurate de poder pagar
- Considera el impacto en tu credito

### 3. Inversion de Familia/Amigos
- Documenta todo por escrito
- Define terminos claros
- Protege relaciones personales

### 4. Creditos para Emprendedores
- Algunos bancos ofrecen creditos especiales
- Requisitos: Plan de negocio, garantias
- Tasas pueden ser preferenciales

## Contabilidad Basica

### Conceptos Clave
- **Ingresos:** Dinero que entra
- **Gastos:** Dinero que sale
- **Utilidad:** Ingresos - Gastos
- **Flujo de caja:** Dinero disponible

### Herramientas
- Excel o Google Sheets
- Apps de contabilidad (QuickBooks, Xero)
- Asesor contable (si el negocio crece)

## Impuestos en Peru

### RUC (Registro Unico de Contribuyente)
- Necesario si facturas
- Tramite en SUNAT
- Obligaciones fiscales

### Impuestos a Considerar
- IGV (18%) si facturas
- Impuesto a la renta (si ganas suficiente)
- Consulta con contador

## Errores Comunes

### 1. No Separar Finanzas
- Mezclar dinero personal y del negocio
- Dificulta saber si el negocio es rentable

### 2. No Tener Reserva
- Gastar todo el capital inicial
- Sin fondo para emergencias del negocio

### 3. No Llevar Contabilidad
- No saber si estas ganando o perdiendo
- Problemas con impuestos

### 4. Crecer Demasiado Rapido
- Invertir antes de validar el negocio
- Quedarse sin capital

## Consejos para el Exito
- Empieza pequeno, valida la idea
- Manten costos bajos inicialmente
- Reinvierte utilidades en el negocio
- Educate constantemente
- Busca mentoria
- Construye un fondo de emergencia del negocio

## Cuando Buscar Ayuda Profesional
- Contador: Para impuestos y contabilidad
- Abogado: Para estructura legal
- Asesor financiero: Para decisiones grandes
- Mentor: Para guia general''',
                'nivel_dificultad': 3,
                'duracion_minutos': 22,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['SUNAT'],
            },
            {
                'titulo': 'Metas financieras: Como establecerlas y alcanzarlas',
                'tipo_contenido': 'articulo',
                'categoria': 'ahorro',
                'descripcion': 'Metodologia SMART para establecer y alcanzar metas financieras realistas.',
                'contenido': '''# Metas Financieras: Como Alcanzarlas

## ¿Por qué tener Metas Financieras?
Sin metas claras, es facil gastar sin direccion. Las metas te dan:
- Enfoque y motivacion
- Medicion de progreso
- Sensacion de logro

## Metodologia SMART

### S - Especifica (Specific)
**Mal:** "Quiero ahorrar dinero"
**Bien:** "Quiero ahorrar S/. 5,000 para un viaje a Europa"

### M - Medible (Measurable)
- Define cantidades exactas
- Puedes trackear el progreso
- Sabes cuando la alcanzaste

### A - Alcanzable (Achievable)
- Realista segun tus ingresos
- No imposible, pero desafiante
- Considera tu situacion actual

### R - Relevante (Relevant)
- Importante para ti
- Alineada con tus valores
- Te motiva realmente

### T - Con Tiempo (Time-bound)
- Fecha limite clara
- Crea urgencia
- Permite planificacion

## Tipos de Metas Financieras

### Corto Plazo (1-12 meses)
- Fondo de emergencia basico
- Vacaciones
- Electrodomesticos
- Cursos o educacion

### Mediano Plazo (1-5 anos)
- Fondo de emergencia completo
- Deposito para vehiculo
- Inversion inicial
- Negocio propio

### Largo Plazo (5+ anos)
- Casa propia
- Jubilacion
- Educacion de hijos
- Libertad financiera

## Como Establecer tus Metas

### Paso 1: Brainstorming
- Lista todo lo que quieres
- No te limites inicialmente
- Incluye sueños grandes y pequenos

### Paso 2: Priorizacion
- ¿Cual es mas importante?
- ¿Cual es mas urgente?
- ¿Cual te da mas felicidad?

### Paso 3: Planificacion
- Calcula cuanto necesitas
- Define plazo
- Calcula ahorro mensual necesario

### Paso 4: Accion
- Crea cuenta de ahorro separada
- Automatiza transferencias
- Revisa progreso mensualmente

## Ejemplo Practico

**Meta:** Viaje a Europa (S/. 8,000)
**Plazo:** 12 meses
**Ahorro mensual:** S/. 667
**Accion:** Transferencia automatica de S/. 700/mes

## Obstaculos Comunes

### 1. Metas Demasiado Ambiciosas
- Solucion: Divide en metas mas pequenas
- Celebra logros intermedios

### 2. Falta de Disciplina
- Solucion: Automatiza ahorros
- Hazlo antes de gastar

### 3. Emergencias
- Solucion: Fondo de emergencia primero
- Ajusta metas si es necesario

## Consejos para el Exito
- Escribe tus metas
- Visualiza el resultado
- Comparte con alguien (accountability)
- Revisa y ajusta regularmente
- Celebra cuando las alcanzas
- Establece nuevas metas continuamente''',
                'nivel_dificultad': 1,
                'duracion_minutos': 15,
                'incluye_ejemplos_peru': True,
            },
            {
                'titulo': 'Comparacion de bancos: Como elegir el mejor para ti',
                'tipo_contenido': 'articulo',
                'categoria': 'educacion',
                'descripcion': 'Guia para comparar y elegir el banco adecuado segun tus necesidades en Peru.',
                'contenido': '''# Como Elegir el Banco Adecuado

## Bancos Principales en Peru

### BCP (Banco de Credito)
- **Ventajas:** Amplia red, buena app, muchas promociones
- **Desventajas:** Comisiones pueden ser altas
- **Ideal para:** Usuarios que valoran conveniencia

### BBVA
- **Ventajas:** Buena atencion, productos innovadores
- **Desventajas:** Menos sucursales en algunas zonas
- **Ideal para:** Usuarios digitales

### Interbank
- **Ventajas:** Buenas ofertas en retail, app funcional
- **Desventajas:** Servicio al cliente variable
- **Ideal para:** Usuarios que compran mucho en retail

### Scotiabank
- **Ventajas:** Buena para viajeros, productos internacionales
- **Desventajas:** Menos presencia en Peru
- **Ideal para:** Usuarios que viajan frecuentemente

## Factores a Considerar

### 1. Comisiones
- Mantenimiento de cuenta
- Retiros en otros bancos
- Transferencias
- Consultas

### 2. Red de Sucursales y ATMs
- ¿Hay sucursales cerca de ti?
- ¿Hay muchos cajeros?
- ¿Cobran por retiros en otros bancos?

### 3. App Movil
- Facilidad de uso
- Funcionalidades
- Seguridad
- Disponibilidad

### 4. Productos Ofrecidos
- Cuentas de ahorro
- Tarjetas de credito
- Prestamos
- Inversiones

### 5. Atencion al Cliente
- Horarios de atencion
- Canales de contacto
- Tiempo de respuesta
- Calidad del servicio

## Tipos de Cuentas

### Cuenta de Ahorros Basica
- Sin comisiones (algunas)
- Interes minimo
- Ideal para: Principiantes

### Cuenta Corriente
- Comisiones mensuales
- Cheques y otros servicios
- Ideal para: Negocios, mayores ingresos

### Cuenta Joven/Estudiante
- Sin comisiones
- Beneficios especiales
- Ideal para: Jovenes, estudiantes

## Como Comparar

### 1. Lista tus Necesidades
- ¿Que usaras mas?
- ¿Cuantas transacciones?
- ¿Que productos necesitas?

### 2. Investiga Opciones
- Visita webs de bancos
- Compara comisiones
- Lee terminos y condiciones

### 3. Pregunta a Conocidos
- Experiencias de otros usuarios
- Problemas comunes
- Recomendaciones

### 4. Prueba la App
- Descarga apps de prueba
- Verifica funcionalidades
- Evalua facilidad de uso

## Consejos Importantes
- No necesitas solo un banco
- Puedes tener cuentas en diferentes bancos
- Considera bancos digitales (nuevas opciones)
- Revisa promociones especiales
- Lee las letras pequenas
- No te dejes llevar solo por promociones

## Cambiar de Banco
Si no estas satisfecho:
1. Investiga alternativas
2. Abre nueva cuenta
3. Transfiere automaticos
4. Cierra cuenta antigua (despues de verificar)

## Conclusion
El mejor banco es el que mejor se adapta a TUS necesidades. No hay una respuesta unica para todos.''',
                'nivel_dificultad': 1,
                'duracion_minutos': 16,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['BCP', 'BBVA', 'Interbank', 'Scotiabank'],
            },
            {
                'titulo': 'Retiro y jubilacion: Empieza a planificar temprano',
                'tipo_contenido': 'articulo',
                'categoria': 'inversion',
                'descripcion': 'Por que y como empezar a planificar tu jubilacion desde joven, incluso en tus 20s.',
                'contenido': '''# Planificacion de Jubilacion para Jovenes

## ¿Por qué Planificar Ahora?

### El Poder del Tiempo
- Invertir desde joven = mas tiempo para crecer
- Interes compuesto trabaja mejor con tiempo
- Pequenos montos ahora = grandes resultados despues

### Ejemplo Real
**Persona A:** Empieza a los 25, invierte S/. 200/mes por 40 anos
**Persona B:** Empieza a los 35, invierte S/. 400/mes por 30 anos

A los 65, Persona A tiene MAS dinero a pesar de invertir menos total.

## Sistema de Pensiones en Peru

### AFP (Administradoras de Fondos de Pensiones)
- Obligatorio si trabajas formalmente
- Descuento del 10% de tu sueldo
- Puedes elegir entre varias AFP
- Rendimiento variable

### ONP (Opcional)
- Sistema de reparto
- Menos comun para jovenes
- Considera si trabajas independiente

## Estrategias de Ahorro para Jubilacion

### 1. Aprovecha tu AFP
- Elige la AFP con mejor rendimiento historico
- Revisa comisiones
- No retires antes de tiempo

### 2. Ahorro Complementario
- Invierte adicionalmente
- Fondos mutuos de largo plazo
- Depositos a plazo para objetivos especificos

### 3. Inversiones Personales
- Diversifica fuera del sistema formal
- Inmuebles (a largo plazo)
- Negocios propios

## Cuanto Necesitas para Jubilarte

### Calculo Basico
- Estima gastos mensuales en jubilacion
- Multiplica por 12 (gasto anual)
- Multiplica por 25 (para 25 anos de jubilacion)
- Ajusta por inflacion

**Ejemplo:**
- Gasto mensual: S/. 3,000
- Gasto anual: S/. 36,000
- Necesitas: S/. 900,000 (aprox)

### Factores a Considerar
- Inflacion (2-3% anual)
- Expectativa de vida
- Gastos medicos
- Actividades en jubilacion

## Como Empezar

### Paso 1: Calcula tu Necesidad
- Usa calculadoras online
- Considera tu estilo de vida deseado
- Ajusta por inflacion

### Paso 2: Evalua tu Situacion Actual
- ¿Cuanto tienes en AFP?
- ¿Cuanto estas ahorrando?
- ¿Cuanto necesitas aumentar?

### Paso 3: Crea un Plan
- Define cuanto ahorrar mensualmente
- Automatiza transferencias
- Revisa anualmente

## Errores Comunes

### 1. Pensar que es Muy Temprano
- Nunca es demasiado temprano
- El tiempo es tu mejor aliado

### 2. No Considerar Inflacion
- S/. 1,000 hoy no es lo mismo que en 40 anos
- Ajusta tus calculos

### 3. Depender Solo del AFP
- Puede no ser suficiente
- Diversifica

### 4. Retirar Antes de Tiempo
- Pierdes beneficios
- Penalizaciones fiscales

## Consejos para Jovenes
- Empieza ahora, aunque sea poco
- Aumenta tu ahorro cuando ganes mas
- Invierte en educacion financiera
- Revisa tu plan anualmente
- No toques ese dinero hasta jubilarte
- Considera asesoria profesional cuando crezca

## Recursos
- Calculadoras de AFP
- Simuladores de jubilacion
- Asesores financieros
- Contenido educativo continuo

**Recuerda: Tu yo del futuro te lo agradecera.**''',
                'nivel_dificultad': 2,
                'duracion_minutos': 20,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['AFP', 'ONP'],
            },
            {
                'titulo': 'Fraudes digitales: Proteccion avanzada',
                'tipo_contenido': 'articulo',
                'categoria': 'fraudes',
                'descripcion': 'Tecnicas avanzadas de proteccion contra fraudes digitales y como mantenerte seguro online.',
                'contenido': '''# Proteccion Avanzada Contra Fraudes Digitales

## Autenticacion de Dos Factores (2FA)

### ¿Qué es?
Metodo de seguridad que requiere dos formas de verificacion:
1. Algo que sabes (contrasea)
2. Algo que tienes (telefono, app)

### Como Activar
- Apps bancarias: Configuracion > Seguridad
- Correo electronico: Configuracion de cuenta
- Redes sociales: Configuracion de privacidad

### Tipos de 2FA
- SMS (menos seguro pero mejor que nada)
- Apps autenticadoras (Google Authenticator, Authy)
- Notificaciones push (mas seguro)

## Contraseas Seguras

### Caracteristicas de Buena Contrasea
- Minimo 12 caracteres
- Mayusculas y minusculas
- Numeros y simbolos
- No palabras del diccionario
- Unica para cada cuenta

### Administradores de Contraseas
- LastPass, 1Password, Bitwarden
- Generan contraseas seguras
- Las almacenan encriptadas
- Solo necesitas recordar una contrasea maestra

## Navegacion Segura

### HTTPS
- Siempre verifica el candado en la URL
- No ingreses datos en sitios sin HTTPS
- Especialmente importante en transacciones

### WiFi Publico
- No uses para transacciones bancarias
- Usa VPN si es necesario
- Mejor: Usa datos moviles

### Actualizaciones
- Manten sistema operativo actualizado
- Actualiza navegadores
- Actualiza apps bancarias

## Phishing Avanzado

### Tecnicas Modernas
- Spear phishing (personalizado)
- Vishing (por telefono)
- Smishing (por SMS/WhatsApp)

### Como Protegerte
- Verifica siempre el remitente
- No hagas clic en enlaces sospechosos
- Contacta directamente a la institucion
- Desconfia de urgencia excesiva

## Monitoreo de Cuentas

### Alertas Bancarias
- Activa notificaciones de transacciones
- Configura limites de transaccion
- Revisa estados de cuenta regularmente

### Monitoreo de Credito
- Revisa tu reporte crediticio periodicamente
- Activa alertas de nuevos creditos
- Detecta actividad sospechosa temprano

## Backup y Recuperacion

### Backup de Datos
- Guarda copias importantes
- Usa almacenamiento en la nube seguro
- Manten backups actualizados

### Plan de Recuperacion
- ¿Que harias si te hackean?
- Lista de contactos importantes
- Procedimientos de emergencia

## Consejos Avanzados
- Usa tarjetas virtuales para compras online
- Considera seguros de fraude
- Educate continuamente
- Comparte conocimiento con otros
- Mantente actualizado sobre nuevas amenazas

## Recursos en Peru
- SBS: Superintendencia de Banca
- Indecopi: Proteccion al consumidor
- Policia Nacional: Division de Cibercrimen
- Bancos: Lineas de emergencia 24/7

**La mejor proteccion es la educacion y la vigilancia constante.**''',
                'nivel_dificultad': 3,
                'duracion_minutos': 18,
                'incluye_ejemplos_peru': True,
                'instituciones_mencionadas': ['SBS', 'Indecopi', 'PNP'],
            },
        ]
        
        creados = 0
        for contenido in nuevos_contenidos:
            obj, created = EducationalContent.objects.get_or_create(
                titulo=contenido['titulo'],
                defaults=contenido
            )
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creado: {obj.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {obj.titulo}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n[OK] {creados} contenidos nuevos agregados'))
        self.stdout.write(self.style.SUCCESS(f'Total contenidos educativos: {EducationalContent.objects.count()}'))


