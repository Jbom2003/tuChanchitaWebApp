"""
Comando de management para poblar la base de datos con:
- Contenido de prevencion de fraudes (contextualizado al Peru)
- Logros del sistema
"""
from django.core.management.base import BaseCommand
from myapp.models import FraudPreventionContent, Achievement


class Command(BaseCommand):
    help = 'Pobla la base de datos con contenido de fraudes y logros'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando poblacion de datos...'))
        
        # ============================================
        # PREVENCION DE FRAUDES
        # ============================================
        fraudes_data = [
            {
                'titulo': 'Phishing: El Fraude del Correo Falso',
                'tipo_fraude': 'phishing',
                'descripcion': 'El phishing es una tecnica fraudulenta donde los estafadores envian correos electronicos, mensajes de texto o llamadas que parecen ser de instituciones financieras legitimas (como bancos peruanos), pero que en realidad buscan robar tu informacion personal y financiera.',
                'ejemplo_real': '''Caso Real en Peru (2024):
Un usuario recibio un correo aparentemente de Interbank que decia:
"Su cuenta ha sido suspendida. Haga clic aqui para verificar su identidad"

Al hacer clic, fue redirigido a una pagina falsa que imitaba el portal de Interbank, donde ingreso su numero de tarjeta y clave. Horas despues, se realizaron compras fraudulentas por mas de S/. 5,000.

La pagina falsa tenia errores ortograficos y la URL no era oficial (.com.pe en lugar de .pe).''',
                'como_protegerse': '''COMO PROTEGERTE:
1. NUNCA hagas clic en enlaces de correos sospechosos. Ingresa directamente al sitio web del banco escribiendo la URL
2. Verifica siempre la URL completa antes de ingresar datos. Los bancos peruanos usan dominios .pe
3. Los bancos NUNCA te pediran tu clave por correo o telefono
4. Si recibes un correo sospechoso, contacta directamente al banco por telefono oficial
5. Activa la autenticacion de dos factores (2FA) en todas tus cuentas
6. Revisa regularmente los movimientos de tu cuenta bancaria

SEÑALES DE ALERTA:
- Errores ortograficos en el correo
- Urgencia excesiva ("Actue ahora o perdera su cuenta")
- Direcciones de correo que no coinciden con el banco oficial
- Enlaces que no llevan al dominio oficial del banco''',
                'nivel_dificultad': 2
            },
            {
                'titulo': 'Smishing: Fraudes por WhatsApp y SMS',
                'tipo_fraude': 'smishing',
                'descripcion': 'El smishing es phishing a traves de mensajes de texto (SMS) o aplicaciones de mensajeria como WhatsApp. Los estafadores envian mensajes que parecen ser de empresas conocidas, servicios publicos o bancos, pidiendo que hagas clic en un enlace o que respondas con informacion personal.',
                'ejemplo_real': '''Caso Real en Peru (2024):
Usuarios recibieron mensajes de WhatsApp aparentemente de Movistar:
"Movistar: Su factura esta lista. Pague ahora y obtenga 50% descuento. [enlace]"

Al hacer clic, fueron dirigidos a una pagina que solicitaba numero de tarjeta y CVV. Varias personas perdieron entre S/. 300 y S/. 2,000 en este fraude.

Tambien circulan mensajes falsos sobre "paquetes de datos ilimitados" o "promociones especiales" que requieren ingresar datos bancarios.''',
                'como_protegerse': '''COMO PROTEGERTE:
1. NUNCA hagas clic en enlaces de mensajes no solicitados
2. Verifica siempre los numeros de telefono. Los bancos y empresas usan numeros oficiales cortos
3. No respondas a mensajes que piden informacion personal o bancaria
4. Contacta directamente a la empresa por sus canales oficiales para verificar
5. Los bancos peruanos NUNCA te contactaran por WhatsApp para pedir claves o datos
6. Si recibes un mensaje sospechoso, reportalo bloqueando el numero

SEÑALES DE ALERTA:
- Mensajes de numeros desconocidos o no oficiales
- Ofertas "demasiado buenas para ser verdad"
- Urgencia para que actues inmediatamente
- Errores ortograficos o mensajes mal redactados
- Enlaces acortados que no muestran el destino real''',
                'nivel_dificultad': 2
            },
            {
                'titulo': 'Vishing: Estafas Telefonicas Bancarias',
                'tipo_fraude': 'vishing',
                'descripcion': 'El vishing es phishing por voz (telefono). Los estafadores llaman haciendose pasar por personal del banco, la policia, SUNAT u otras instituciones, pidiendo informacion personal o que realices acciones que comprometen tu seguridad financiera.',
                'ejemplo_real': '''Caso Real en Peru (2024):
Una persona recibio una llamada aparentemente del BCP:
"Buenos dias, soy de seguridad del BCP. Hemos detectado actividad sospechosa en su cuenta. Necesito que confirme sus datos para bloquear las transacciones fraudulentas."

El estafador supo el nombre completo y parte del DNI (informacion obtenida de bases de datos filtradas). La victima proporciono su numero completo de tarjeta, clave de cajero y codigo CVV. Al dia siguiente, se realizaron retiros y compras por S/. 8,500.

Los estafadores usan tecnicas de ingenieria social, crean urgencia y usan informacion parcial real para ganar confianza.''',
                'como_protegerse': '''COMO PROTEGERTE:
1. Los bancos NUNCA te llamaran para pedir tu clave completa, CVV o codigos de seguridad
2. Si recibes una llamada sospechosa, cuelga y llama tu mismo al banco por el numero oficial
3. NUNCA proporciones informacion personal por telefono si tu no iniciaste la llamada
4. No confies en el numero que aparece en tu pantalla (se puede falsificar)
5. Los bancos tienen procedimientos oficiales; si hay un problema real, te pediran que vayas a la sucursal
6. Manten la calma. Los estafadores crean urgencia para que no pienses con claridad

QUE HACER SI RECIBES UNA LLAMADA SOSPECHOSA:
- Cuelga inmediatamente
- No proporciones NINGUNA informacion
- Llama directamente a tu banco al numero oficial de atencion
- Si es urgente, ve a la sucursal del banco en persona
- Reporta el numero a la Superintendencia de Banca (SBS)''',
                'nivel_dificultad': 3
            },
            {
                'titulo': 'Skimming: Clonacion de Tarjetas en Cajeros',
                'tipo_fraude': 'skimming',
                'descripcion': 'El skimming es una tecnica donde los delincuentes instalan dispositivos ilegales en cajeros automaticos, terminales de pago o bombas de combustible para copiar la informacion de la banda magnetica de tu tarjeta y capturar tu PIN.',
                'ejemplo_real': '''Caso Real en Lima (2024):
Usuarios reportaron retiros no autorizados de sus cuentas. La investigacion revelo que varios cajeros automaticos en distritos de Lima tenian dispositivos skimmer instalados.

Los delincuentes instalaron:
- Un lector falso sobre la ranura del cajero (para copiar la tarjeta)
- Una camara oculta sobre el teclado (para grabar el PIN)
- Un teclado falso que guardaba las teclas presionadas

Mas de 50 personas fueron victimas, con perdidas entre S/. 500 y S/. 5,000 por persona.

El fraude se detecto cuando usuarios notaron que el cajero "se veia diferente" o que la tarjeta quedaba atascada.''',
                'como_protegerse': '''COMO PROTEGERTE:
1. Inspecciona el cajero antes de usarlo. Busca dispositivos sueltos o que se vean diferentes
2. Tapa siempre el teclado con tu mano al ingresar el PIN
3. Tira suavemente de la ranura donde insertas la tarjeta. Si se mueve o se desprende, NO la uses
4. Usa cajeros dentro de bancos o lugares bien iluminados y vigilados
5. Prefiere pagos con tarjeta sin contacto (contactless) o apps de pago
6. Revisa regularmente los movimientos de tu cuenta para detectar cargos no autorizados
7. Si tu tarjeta queda atascada, contacta inmediatamente al banco

SEÑALES DE ALERTA EN CAJEROS:
- Dispositivos que parecen agregados al cajero original
- La ranura para la tarjeta se mueve o se ve diferente
- Teclados que se ven nuevos o diferentes
- Camaras pequeñas cerca del teclado
- Advertencias de "fuera de servicio" que pueden ser para instalar skimmers''',
                'nivel_dificultad': 3
            },
            {
                'titulo': 'Robo de Identidad: Suplantacion de Identidad',
                'tipo_fraude': 'identity_theft',
                'descripcion': 'El robo de identidad ocurre cuando alguien obtiene tu informacion personal (DNI, numero de tarjeta, datos bancarios) y la usa para abrir cuentas, hacer compras o solicitar creditos a tu nombre. En Peru, este tipo de fraude ha aumentado significativamente con el crecimiento del comercio digital.',
                'ejemplo_real': '''Caso Real en Peru (2024):
Una persona descubrio que alguien habia abierto una cuenta de credito a su nombre usando su DNI y datos personales filtrados de una compra online. El estafador:

1. Obtuvo el DNI y datos basicos de una base de datos filtrada
2. Solicito una tarjeta de credito online usando esos datos
3. Cambio la direccion de correo y telefono asociados
4. Realizo compras por mas de S/. 15,000 antes de que la victima se diera cuenta

La victima descubrio el fraude cuando intento solicitar un credito y le dijeron que ya tenia una cuenta morosa. Tardo meses en limpiar su historial crediticio.''',
                'como_protegerse': '''COMO PROTEGERTE:
1. Protege tu DNI y documentos personales. No compartas fotos de tu DNI en redes sociales
2. Revisa regularmente tu reporte crediticio en la Central de Riesgos del SBS
3. Activa alertas de credito en instituciones financieras para que te notifiquen de nuevos creditos
4. Usa contraseñas fuertes y diferentes para cada cuenta online
5. No compartas informacion personal en sitios web no seguros (busca el candado en la URL)
6. Destruye documentos fisicos con informacion personal antes de desecharlos
7. Monitorea tus cuentas bancarias y creditos regularmente

QUE HACER SI ERES VICTIMA:
- Contacta inmediatamente a las instituciones financieras afectadas
- Presenta una denuncia en la Policia Nacional
- Solicita un bloqueo preventivo en la Central de Riesgos del SBS
- Cambia todas tus contraseñas
- Considera congelar tus reportes crediticios temporalmente''',
                'nivel_dificultad': 4
            },
            {
                'titulo': 'Pharming: Redireccion a Sitios Falsos',
                'tipo_fraude': 'pharming',
                'descripcion': 'El pharming es una tecnica mas sofisticada donde los estafadores redirigen el trafico de internet de sitios legitimos a sitios falsos, incluso cuando escribes correctamente la URL. Esto se logra infectando tu computadora con malware o comprometiendo servidores DNS.',
                'ejemplo_real': '''Caso Real en Peru (2023):
Usuarios que intentaron acceder a bancos peruanos fueron redirigidos a paginas falsas que imitaban perfectamente los sitios oficiales. Algunos usuarios ingresaron sus credenciales y perdieron acceso a sus cuentas.

Los estafadores instalaron malware en las computadoras de las victimas que modificaba el archivo "hosts" del sistema, redirigiendo dominios de bancos peruanos a servidores controlados por los delincuentes.

Las victimas pensaban estar en el sitio oficial porque escribian la URL correcta, pero en realidad estaban en un sitio falso.''',
                'como_protegerse': '''COMO PROTEGERTE:
1. Verifica siempre que la URL tenga "https://" y el candado de seguridad
2. Verifica el certificado SSL haciendo clic en el candado en la barra de direcciones
3. Manten tu antivirus y sistema operativo actualizados
4. Usa un DNS seguro como Google DNS (8.8.8.8) o Cloudflare (1.1.1.1)
5. No descargues software de fuentes no confiables
6. Ten cuidado con las conexiones WiFi publicas (usa VPN si es necesario)
7. Si algo se ve diferente en un sitio que visitas frecuentemente, verifica con cuidado

SEÑALES DE ALERTA:
- El sitio pide informacion que normalmente no solicita
- Errores de certificado SSL
- El sitio se ve ligeramente diferente al habitual
- Mensajes de error inesperados al intentar acceder
- Redirecciones inesperadas a otras paginas''',
                'nivel_dificultad': 4
            },
        ]
        
        self.stdout.write(self.style.WARNING('Creando contenido de prevencion de fraudes...'))
        for fraude_data in fraudes_data:
            fraude, created = FraudPreventionContent.objects.get_or_create(
                titulo=fraude_data['titulo'],
                defaults=fraude_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creado: {fraude.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {fraude.titulo}'))
        
        # ============================================
        # LOGROS
        # ============================================
        logros_data = [
            {
                'codigo': 'primer_paso',
                'titulo': 'Primer Paso',
                'descripcion': 'Completa tu evaluacion inicial de competencias financieras',
                'icono': '🎯',
                'puntos_bonus': 50,
                'categoria': 'educacion',
                'requisito': {'tipo': 'evaluacion_completada'}
            },
            {
                'codigo': 'primer_ahorro',
                'titulo': 'Primer Ahorro',
                'descripcion': 'Registra tu primer gasto en la categoria Ahorro',
                'icono': '💰',
                'puntos_bonus': 100,
                'categoria': 'ahorro',
                'requisito': {'tipo': 'primer_ahorro'}
            },
            {
                'codigo': 'semanario_consistente',
                'titulo': 'Semana Consistente',
                'descripcion': 'Registra gastos durante 7 dias consecutivos',
                'icono': '📅',
                'puntos_bonus': 150,
                'categoria': 'consistencia',
                'requisito': {'tipo': 'dias_consecutivos', 'valor': 7}
            },
            {
                'codigo': 'maestro_presupuesto',
                'titulo': 'Maestro del Presupuesto',
                'descripcion': 'Cumple con tu presupuesto mensual durante 3 meses seguidos',
                'icono': '📊',
                'puntos_bonus': 300,
                'categoria': 'presupuesto',
                'requisito': {'tipo': 'meses_presupuesto', 'valor': 3}
            },
            {
                'codigo': 'ahorrador_estelar',
                'titulo': 'Ahorrador Estelar',
                'descripcion': 'Ahorra mas de S/. 1000 en un mes',
                'icono': '⭐',
                'puntos_bonus': 200,
                'categoria': 'ahorro',
                'requisito': {'tipo': 'ahorro_mensual', 'valor': 1000}
            },
            {
                'codigo': 'experto_fraudes',
                'titulo': 'Experto en Fraudes',
                'descripcion': 'Completa todos los contenidos sobre prevencion de fraudes',
                'icono': '🛡️',
                'puntos_bonus': 250,
                'categoria': 'educacion',
                'requisito': {'tipo': 'contenidos_fraudes_completados'}
            },
            {
                'codigo': 'bibliotecario',
                'titulo': 'Bibliotecario',
                'descripcion': 'Visualiza 10 contenidos educativos diferentes',
                'icono': '📚',
                'puntos_bonus': 200,
                'categoria': 'educacion',
                'requisito': {'tipo': 'contenidos_vistos', 'valor': 10}
            },
            {
                'codigo': 'cazador_alertas',
                'titulo': 'Cazador de Alertas',
                'descripcion': 'Revisa y resuelve 5 alertas de riesgo crediticio',
                'icono': '🚨',
                'puntos_bonus': 200,
                'categoria': 'riesgo',
                'requisito': {'tipo': 'alertas_resueltas', 'valor': 5}
            },
            {
                'codigo': 'leyenda_financiera',
                'titulo': 'Leyenda Financiera',
                'descripcion': 'Desbloquea todos los logros disponibles',
                'icono': '👑',
                'puntos_bonus': 500,
                'categoria': 'educacion',
                'requisito': {'tipo': 'todos_los_logros'}
            },
        ]
        
        self.stdout.write(self.style.WARNING('Creando logros...'))
        for logro_data in logros_data:
            logro, created = Achievement.objects.get_or_create(
                codigo=logro_data['codigo'],
                defaults=logro_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creado: {logro.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {logro.titulo}'))
        
        self.stdout.write(self.style.SUCCESS('\n¡Poblacion de datos completada exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'Total fraudes: {FraudPreventionContent.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total logros: {Achievement.objects.count()}'))

