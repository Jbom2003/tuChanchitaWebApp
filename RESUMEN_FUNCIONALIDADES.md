# RESUMEN COMPLETO DE FUNCIONALIDADES - TUCHANCHITA

## DESCRIPCION GENERAL
TuChanchita es una aplicacion web educativa financiera diseñada para jovenes peruanos de 18 a 25 años. Integra gamificacion, inteligencia artificial y educacion financiera para fortalecer competencias financieras practicas y promover comportamientos economicos responsables.

---

## MODULO 1: AUTENTICACION Y REGISTRO

### 1.1 Login (Inicio de Sesion)
**URL:** `/login/` o `/`
**Funcionalidad:** Permite a los usuarios iniciar sesion en la aplicacion.

**Campos del formulario:**
- Email: Correo electronico del usuario
- Contrasea: Contrasea del usuario

**Botones:**
- **Enviar:** Valida credenciales y permite el acceso al dashboard
- **Olvide mi contrasea:** Enlace que redirige a la recuperacion de contrasea
- **Registrarse:** Enlace que redirige al formulario de registro

**Funcionalidades:**
- Validacion de credenciales
- Bloqueo de cuenta tras multiples intentos fallidos (5 intentos)
- Sesion persistente del usuario

---

### 1.2 Registro (Creacion de Cuenta)
**URL:** `/register/`
**Funcionalidad:** Permite crear una nueva cuenta de usuario.

**Campos del formulario:**
- Nombre: Nombre del usuario
- Apellido: Apellido del usuario
- Email: Correo electronico (se valida con API externa)
- Contrasea: Minimo 8 caracteres, debe incluir mayuscula, numero y caracter especial
- Confirmar contrasea: Debe coincidir con la contrasea

**Botones:**
- **Registrarse:** Crea la cuenta y envia email de bienvenida
- **Ya tengo cuenta:** Enlace que redirige al login

**Funcionalidades:**
- Validacion de formato de email con API externa
- Encriptacion de contraseas
- Validacion de contraseas seguras
- Envio de email de bienvenida

---

### 1.3 Recuperacion de Contrasea
**URL:** `/olvide-contrasena/`
**Funcionalidad:** Permite solicitar un enlace para resetear la contrasea.

**Campos del formulario:**
- Email: Correo electronico registrado

**Botones:**
- **Enviar enlace:** Envia email con enlace de recuperacion
- **Volver al login:** Enlace que redirige al login

**Funcionalidades:**
- Genera token seguro para resetear contrasea
- Envia email con enlace de recuperacion
- El enlace expira despues de 24 horas

---

### 1.4 Resetear Contrasea
**URL:** `/resetear/<token>/`
**Funcionalidad:** Permite establecer una nueva contrasea usando el token recibido por email.

**Campos del formulario:**
- Nueva contrasea: Minimo 8 caracteres
- Confirmar contrasea: Debe coincidir

**Botones:**
- **Cambiar contrasea:** Actualiza la contrasea del usuario

---

## MODULO 2: DASHBOARD Y NAVEGACION

### 2.1 Dashboard (Pagina Principal)
**URL:** `/dashboard/`
**Funcionalidad:** Pagina principal del usuario que muestra resumen financiero y acceso rapido a funcionalidades.

**Contenido mostrado:**
- Saludo personalizado con el nombre del usuario
- Puntos acumulados del sistema de gamificacion
- Limite mensual configurado
- Gasto total del mes actual
- Tabla con los ultimos 10 gastos registrados (fecha, tienda/servicio, monto)

**Funcionalidades especiales:**
- Verifica y desbloquea logros automaticamente al cargar
- Muestra alertas si se excede el limite mensual
- Calcula porcentaje de uso del limite

**Accesos rapidos desde navbar:**
- Registrar gasto
- Perfil
- Reportes
- Recomendaciones
- ChatBot
- Inversiones
- Retos
- Juegos (Trivia)
- Evaluacion inicial
- Mi Progreso
- Alertas
- Biblioteca educativa
- Logros
- Narrativa
- Prevencion de fraudes

---

## MODULO 3: GESTION DE GASTOS

### 3.1 Registrar Gasto
**URL:** `/register-expense/`
**Funcionalidad:** Permite registrar un nuevo gasto en el sistema.

**Campos del formulario:**
- Monto: Cantidad en soles (S/.)
- Categoria: Dropdown con categorias (Alimentacion, Transporte, Entretenimiento, Ahorro, Servicios, Otros)
- Metodo de pago: Dropdown con tarjetas registradas del usuario
- Fecha: Calendario para seleccionar fecha
- Tienda/Servicio: Nombre del establecimiento o servicio

**Botones:**
- **Registrar gasto:** Guarda el gasto en la base de datos
- **Volver al Dashboard:** Enlace que redirige al dashboard

**Funcionalidades:**
- Valida que el metodo de pago pertenezca al usuario
- Actualiza el limite mensual utilizado
- Verifica logros relacionados con gastos (ej: Primer Ahorro)
- Muestra popup de logro desbloqueado si corresponde

---

### 3.2 Reportes
**URL:** `/reports/`
**Funcionalidad:** Muestra reportes graficos y estadisticas de gastos del usuario.

**Contenido mostrado:**
- Grafico circular (pie chart) con distribucion de gastos por categoria del mes actual
- Tabla con resumen mensual de gastos (mes y total)
- Visualizacion de tendencias de gasto

**Botones:**
- **Exportar como PDF:** Genera y descarga un PDF con el reporte completo
- **Volver al Dashboard:** Enlace que redirige al dashboard

**Funcionalidades:**
- Calcula totales por categoria
- Muestra historico mensual
- Exportacion a PDF con formato profesional

---

## MODULO 4: PERFIL Y CONFIGURACION

### 4.1 Perfil
**URL:** `/profile/`
**Funcionalidad:** Permite visualizar y gestionar la informacion del perfil del usuario.

**Informacion mostrada:**
- Puntos acumulados
- Nombre completo
- Email
- Limite mensual actual
- Foto de perfil (si esta configurada)

**Secciones:**
1. **Foto de perfil:**
   - Muestra foto actual o foto por defecto
   - Boton para subir/cambiar foto
   - Formato: Imagen (jpg, png)
   
2. **Tarjetas registradas:**
   - Lista todas las tarjetas de credito/debito registradas
   - Muestra tipo de tarjeta, banco, ultimos 4 digitos, fecha de vencimiento
   - Iconos de Visa o Mastercard segun corresponda
   - Boton de eliminar (icono de papelera) para cada tarjeta

**Botones:**
- **Subir foto de perfil:** Abre formulario para subir/cambiar foto
- **Actualizar limite mensual:** Redirige a pagina de actualizacion de limite
- **Agregar nueva tarjeta:** Redirige a formulario de registro de tarjeta
- **Volver al Dashboard:** Enlace que redirige al dashboard

**Funcionalidades:**
- Eliminacion de tarjetas con confirmacion via popup
- Validacion de formato de imagen
- Almacenamiento seguro de informacion de tarjetas

---

### 4.2 Agregar Tarjeta
**URL:** `/add-card/`
**Funcionalidad:** Permite registrar una nueva tarjeta de credito o debito.

**Campos del formulario:**
- Tipo de tarjeta: Credito o Debito
- Banco: Nombre del banco emisor
- Sistema de pago: Visa o Mastercard
- Numero de tarjeta: 16 digitos (se guardan solo ultimos 4)
- Mes de vencimiento: Mes (MM)
- Ano de vencimiento: Ano (YYYY)

**Botones:**
- **Registrar tarjeta:** Guarda la tarjeta asociada al usuario
- **Cancelar:** Vuelve al perfil sin guardar

**Funcionalidades:**
- Solo guarda ultimos 4 digitos por seguridad
- Valida formato de numero de tarjeta
- Asocia la tarjeta al usuario autenticado

---

### 4.3 Actualizar Limite Mensual
**URL:** `/update-limit/`
**Funcionalidad:** Permite modificar el limite mensual de gastos del usuario.

**Campos del formulario:**
- Nuevo limite mensual: Monto en soles (S/.)

**Botones:**
- **Actualizar limite:** Guarda el nuevo limite
- **Volver al Dashboard:** Enlace que redirige al dashboard

---

## MODULO 5: GAMIFICACION

### 5.1 Retos
**URL:** `/retos/`
**Funcionalidad:** Sistema de retos financieros que el usuario puede aceptar y completar.

**Contenido mostrado:**
- Lista de retos disponibles (no iniciados)
- Retos activos con barra de progreso
- Top 5 usuarios con mas puntos
- Progreso de cada reto activo

**Tipos de retos:**
- **Reto de ahorro:** Ahorrar un monto especifico en un plazo determinado
- **Reto de no gastos:** No exceder un monto limite durante un periodo

**Informacion por reto:**
- Titulo y descripcion
- Tipo de reto
- Meta (monto o condicion)
- Plazo (dias)
- Puntos de recompensa
- Progreso actual (porcentaje y barra visual)

**Botones:**
- **Aceptar reto:** Crea una instancia del reto para el usuario (boton en retos disponibles)
- Ver progreso en retos activos (sin boton, solo visual)

**Funcionalidades:**
- Calculo automatico de progreso
- Actualizacion en tiempo real del progreso
- Otorga puntos automaticamente al completar
- Marca retos como fallidos si se excede el plazo

---

### 5.2 Historial de Retos
**URL:** `/historial-retos/`
**Funcionalidad:** Muestra el historial de retos completados o fallidos del usuario.

**Contenido mostrado:**
- Lista de ultimos 10 retos completados o fallidos
- Estado de cada reto (Completado/Fallido)
- Tipo de reto
- Fecha de inicio
- Puntos ganados (si completado)

**Informacion por reto:**
- Titulo
- Tipo (Ahorro o No gastar)
- Estado (Completado/Fallido)
- Fecha de inicio

---

### 5.3 Logros (Achievements)
**URL:** `/logros/`
**Funcionalidad:** Sistema de logros desbloqueables que reconocen hitos financieros del usuario.

**Contenido mostrado:**
- Barra de progreso general (porcentaje de logros completados)
- Contador de logros (ej: "5 de 12 completados")
- Seccion "Logros Desbloqueados": Logros ya obtenidos
- Seccion "Logros Pendientes": Logros aun no alcanzados

**Informacion por logro:**
- Icono emoji
- Titulo del logro
- Descripcion
- Puntos bonus otorgados
- Categoria (educacion, ahorro, consistencia, etc.)
- Estado (desbloqueado/bloqueado)

**Logros disponibles:**
- **Primer Paso:** Completa evaluacion inicial
- **Primer Ahorro:** Registra primer gasto en categoria Ahorro
- **Semana Consistente:** Registra gastos durante 7 dias consecutivos
- **Maestro Presupuesto:** Completa varios retos de presupuesto
- Y mas logros relacionados con uso de la aplicacion

**Funcionalidades:**
- Verificacion automatica de logros al realizar acciones
- Popup global que aparece cuando se desbloquea un logro
- Popup muestra icono, titulo, descripcion y puntos otorgados
- Boton "Cerrar" en el popup que elimina el mensaje

**Nota:** El popup de logros aparece en cualquier pagina cuando se desbloquea un logro nuevo.

---

### 5.4 Trivia (Juegos)
**URL:** `/trivia/`
**Funcionalidad:** Sistema de preguntas y respuestas sobre educacion financiera.

**Funcionalidades:**
- Presenta preguntas aleatorias sobre finanzas
- Opciones multiple choice
- Sistema de puntuacion
- Feedback inmediato (correcto/incorrecto)

**Botones:**
- Opciones de respuesta (botones clickeables)
- **Continuar:** Avanza a la siguiente pregunta o resultado final

**Resultados:**
- Muestra puntuacion final
- Puntos obtenidos segun respuestas correctas
- Comparacion con otros usuarios

---

### 5.5 Ranking de Trivia
**URL:** `/trivia-ranking/`
**Funcionalidad:** Muestra el ranking de usuarios con mejores puntuaciones en trivia.

**Contenido mostrado:**
- Top usuarios ordenados por puntuacion
- Posicion, nombre, puntuacion total
- Puntuacion del usuario actual y su posicion

---

## MODULO 6: HERRAMIENTAS FINANCIERAS

### 6.1 Inversiones
**URL:** `/inversiones/`
**Funcionalidad:** Permite registrar y rastrear inversiones en acciones.

**Contenido mostrado:**
- Formulario para registrar nueva inversion
- Lista de inversiones registradas
- Precio actual de cada accion (obtenido via API)
- Ganancia/perdida calculada

**Campos del formulario:**
- Empresa: Dropdown con opciones (Tesla, Apple, Microsoft, Alphabet/Google)
- Acciones: Numero de acciones a registrar

**Informacion mostrada por inversion:**
- Nombre de la empresa
- Simbolo de la accion
- Numero de acciones
- Precio de compra
- Precio actual (actualizado via API)
- Valor total actual
- Ganancia/perdida (con color: verde si positivo, rojo si negativo)

**Botones:**
- **Registrar inversion:** Guarda la nueva inversion
- **Eliminar:** Boton de eliminar para cada inversion (con confirmacion)

**Funcionalidades:**
- Obtiene precio actual via API de Twelve Data
- Calcula ganancia/perdida automaticamente
- Valida que el precio sea valido antes de guardar

---

### 6.2 Recomendaciones
**URL:** `/recomendaciones/`
**Funcionalidad:** Muestra videos educativos recomendados sobre finanzas personales.

**Contenido mostrado:**
- Lista de videos educativos
- Cada video muestra titulo, descripcion y enlace

**Funcionalidades:**
- Acceso a contenido educativo externo
- Recomendaciones basadas en el perfil del usuario

---

### 6.3 ChatBot (Asistente Financiero)
**URL:** `/chatbot/`
**Funcionalidad:** Asistente virtual de inteligencia artificial para consultas financieras.

**Tecnologia:** Google Gemini AI (modelo gemini-2.0-flash)

**Funcionalidades:**
- Conversacion en tiempo real
- Mantiene historial de conversacion en la sesion
- Responde preguntas sobre finanzas personales
- Proporciona consejos sobre presupuesto, ahorro, credito
- Adaptado al contexto peruano

**Interfaz:**
- Campo de texto para escribir mensaje
- Boton "Enviar" para enviar mensaje
- Historial de conversacion mostrado en burbujas
- Mensajes del usuario alineados a la derecha
- Respuestas del bot alineadas a la izquierda
- Indicador de "escribiendo..." mientras procesa

**Caracteristicas especiales:**
- Limpia automaticamente errores previos del historial
- Manejo robusto de errores con mensajes claros
- Intenta multiples modelos de Gemini como fallback

---

## MODULO 7: INVESTIGACION Y EDUCACION FINANCIERA

### 7.1 Evaluacion Inicial
**URL:** `/evaluacion-inicial/`
**Funcionalidad:** Cuestionario inicial que diagnostica el nivel de competencias financieras del usuario.

**Campos del formulario:**
- **Competencias Basicas (escala 1-5):**
  - Conocimiento de presupuesto
  - Conocimiento de ahorro
  - Conocimiento de credito
  - Conocimiento de inversiones
  - Conocimiento de fraudes

- **Comportamientos de Endeudamiento:**
  - Tiene tarjetas de credito (si/no)
  - Cantidad de tarjetas
  - Monto de deuda actual
  - Frecuencia de pago minimo (veces al ano)

- **Vulnerabilidad Digital:**
  - Conocimiento sobre fraudes
  - Ha tenido experiencia con fraude (si/no)

- **Brecha Teorico-Practica:**
  - Conocimiento teorico (escala 1-5)
  - Aplicacion practica (escala 1-5)

**Botones:**
- **Enviar evaluacion:** Guarda la evaluacion y muestra resultados

**Funcionalidades:**
- Calcula puntaje total automaticamente
- Determina nivel de competencia (bajo, medio, alto)
- Solo permite una evaluacion por usuario (actualiza si ya existe)
- Redirige a pagina de resultados con analisis

**Resultados mostrados:**
- Puntaje total
- Nivel de competencia
- Analisis de brecha teorico-practica
- Recomendaciones personalizadas

---

### 7.2 Mi Progreso
**URL:** `/progreso-individual/`
**Funcionalidad:** Dashboard que muestra las metricas y progreso individual del usuario.

**Contenido mostrado:**
- **Metricas de usuario:**
  - Puntaje inicial y actual
  - Mejora porcentual en competencias
  - Reduccion de riesgo crediticio
  - Dias activos en la aplicacion
  - Sesiones totales

- **Alertas recientes:**
  - Lista de las 5 alertas de riesgo mas recientes no vistas
  - Tipo de alerta
  - Severidad
  - Descripcion breve

- **Graficos de progreso:**
  - Evolucion del puntaje de competencias
  - Tendencias de comportamiento

**Botones:**
- **Volver al Dashboard:** Boton que redirige al dashboard

**Funcionalidades:**
- Calcula metricas automaticamente
- Actualiza datos en tiempo real
- Identifica mejoras en competencias financieras

---

### 7.3 Alertas de Riesgo
**URL:** `/alertas-riesgo/`
**Funcionalidad:** Muestra alertas automaticas sobre comportamientos de riesgo crediticio.

**Contenido mostrado:**
- Lista completa de alertas generadas para el usuario
- Ordenadas por fecha (mas recientes primero)

**Informacion por alerta:**
- Tipo de alerta:
  - Gasto excesivo
  - Limite proximo
  - Deuda alta
  - Solo pago minimo
  - Sin ahorro mensual
- Severidad (Baja, Media, Alta)
- Descripcion detallada del riesgo
- Fecha de creacion
- Recomendaciones para mitigar el riesgo
- Estado (vista/no vista)

**Funcionalidades:**
- Generacion automatica de alertas basadas en comportamiento
- Sistema de severidad para priorizar alertas
- Recomendaciones personalizadas por tipo de alerta

---

### 7.4 Biblioteca Educativa
**URL:** `/biblioteca-educativa/`
**Funcionalidad:** Biblioteca con contenido educativo sobre finanzas personales organizado por categorias.

**Contenido mostrado:**
- Grid de contenido educativo disponible
- Filtros por categoria:
  - Presupuesto
  - Credito
  - Ahorro
  - Inversion
  - Fraude Digital
  - General

**Informacion por contenido:**
- Titulo
- Tipo (Articulo, Video, Infografia, Curso Interactivo)
- Categoria
- Descripcion breve
- Nivel de dificultad (1-5)
- Duracion estimada (minutos)
- Numero de visualizaciones

**Contenidos disponibles:**
1. Como crear tu primer presupuesto personal
2. Ahorro inteligente: Estrategias para jovenes en Peru
3. Todo sobre tarjetas de credito: Guia completa
4. Inversiones para principiantes en Peru
5. Fraudes digitales: Protege tu dinero online

**Botones:**
- **Ver contenido:** Boton en cada tarjeta que lleva al contenido completo
- Filtros por categoria (enlaces clickeables)

**Funcionalidades:**
- Contenido contextualizado al Peru
- Menciona instituciones peruanas (SBS, BCP, BBVA, etc.)
- Incrementa contador de visualizaciones al ver contenido
- Contenido detallado con ejemplos practicos

---

### 7.5 Ver Contenido Educativo
**URL:** `/contenido/<id>/`
**Funcionalidad:** Muestra el contenido completo de un articulo educativo.

**Contenido mostrado:**
- Titulo completo
- Tipo y categoria
- Contenido completo formateado (Markdown)
- Nivel de dificultad
- Duracion estimada
- Ejemplos peruanos incluidos
- Instituciones mencionadas

**Botones:**
- **Volver a Biblioteca:** Regresa a la lista de contenido
- **Dashboard:** Redirige al dashboard

**Funcionalidades:**
- Renderiza contenido en formato Markdown
- Incrementa visualizaciones
- Formato legible y organizado

---

### 7.6 Narrativa (Historia Progresiva)
**URL:** `/narrativa/`
**Funcionalidad:** Historia interactiva que guia al usuario a traves de un viaje educativo financiero con capitulos desbloqueables.

**Contenido mostrado:**
- Lista de todos los capitulos disponibles
- Estado de cada capitulo:
  - **Desbloqueado:** Puede ser leido (borde verde)
  - **Bloqueado:** Aun no disponible (borde gris, opaco)
  - **Completado:** Ya fue leido (badge de completado)

**Informacion por capitulo:**
- Numero de capitulo
- Titulo
- Descripcion breve
- Estado (Disponible, Bloqueado, Completado)
- Progreso (si esta en progreso)

**Capitulos disponibles:**
1. **El Despertar Financiero** - Introduccion al viaje (desbloqueado desde el inicio)
2. **Tu Primer Presupuesto** - Aprende a crear presupuestos
3. **El Arte de Ahorrar** - Estrategias de ahorro
4. **Credito: Amigo o Enemigo?** - Uso inteligente del credito
5. **Proteccion Contra Fraudes** - Seguridad digital
6. **Tu Futuro Financiero** - Introduccion a inversion

**Botones:**
- **Leer capitulo:** Boton en capitulos desbloqueados que lleva al contenido
- Capitulos bloqueados muestran requisitos para desbloquear

**Funcionalidades:**
- Desbloqueo progresivo segun acciones del usuario
- Requisitos para desbloquear (ej: completar evaluacion inicial, crear presupuesto)
- Sistema de recompensas (puntos) al completar capitulos
- Marca capitulos como completados

---

### 7.7 Ver Capitulo de Narrativa
**URL:** `/narrativa/capitulo/<id>/`
**Funcionalidad:** Muestra el contenido completo de un capitulo de la narrativa.

**Contenido mostrado:**
- Titulo del capitulo
- Numero de capitulo
- Contenido educativo completo formateado
- Informacion sobre el siguiente capitulo

**Botones:**
- **Marcar como completado:** Marca el capitulo como leido y otorga puntos
- **Volver a Narrativa:** Regresa a la lista de capitulos
- **Siguiente capitulo:** Si esta desbloqueado, lleva al siguiente

**Funcionalidades:**
- Solo accesible si el capitulo esta desbloqueado
- Otorga puntos al completar
- Desbloquea el siguiente capitulo si cumple requisitos

---

### 7.8 Prevencion de Fraudes
**URL:** `/prevencion-fraudes/`
**Funcionalidad:** Biblioteca de contenido educativo sobre fraudes digitales comunes en Peru.

**Contenido mostrado:**
- Grid de fraudes disponibles
- Filtros por tipo de fraude:
  - Todos
  - Phishing
  - Pharming
  - Smishing
  - Vishing
  - Skimming
  - Robo de Identidad

**Informacion por fraude:**
- Tipo de fraude (badge con color)
- Titulo
- Descripcion breve (truncada a 25 palabras)
- Nivel de dificultad

**Tipos de fraudes disponibles:**
1. Phishing: El Fraude del Correo Falso
2. Smishing: Fraudes por WhatsApp y SMS
3. Vishing: Estafas Telefonicas Bancarias
4. Skimming: Clonacion de Tarjetas en Cajeros
5. Robo de Identidad: Suplantacion de Identidad
6. Pharming: Redireccion a Sitios Falsos
7. Robo de Identidad: Protege tu Informacion Personal

**Botones:**
- **Aprender Mas:** Boton en cada tarjeta que lleva al contenido detallado
- Filtros por tipo (enlaces clickeables)

**Funcionalidades:**
- Filtrado por tipo de fraude
- Contenido contextualizado con casos reales en Peru
- Ejemplos practicos de estafas comunes

---

### 7.9 Ver Fraude (Detalle)
**URL:** `/fraude/<id>/`
**Funcionalidad:** Muestra informacion detallada sobre un tipo especifico de fraude.

**Contenido mostrado:**
- Titulo del fraude
- Tipo de fraude
- **Seccion "Que es?":** Descripcion completa del fraude
- **Seccion "Ejemplo Real en el Peru":** Caso real de fraude ocurrido en Peru con detalles
- **Seccion "Como Protegerse":** Guia detallada de proteccion con pasos especificos
- Video explicativo (si esta disponible)

**Botones:**
- **Volver a Prevencion de Fraudes:** Regresa a la lista de fraudes
- **Dashboard:** Redirige al dashboard

**Funcionalidades:**
- Contenido completo y detallado
- Ejemplos reales contextualizados
- Guias practicas de proteccion
- Formato legible con secciones claras

---

### 7.10 Reporte de Impacto (Admin)
**URL:** `/reporte-impacto/`
**Funcionalidad:** Panel administrativo que muestra metricas generales del sistema para investigacion.

**Contenido mostrado:**
- Total de usuarios registrados
- Total de evaluaciones completadas
- Total de logros desbloqueados
- Metricas agregadas de mejora
- Estadisticas de uso de la aplicacion

**Funcionalidades:**
- Recopila datos para analisis de investigacion
- Mide impacto de la aplicacion
- Permite exportar datos para analisis estadistico

---

## RESUMEN DE BOTONES Y ACCIONES PRINCIPALES

### Botones de Navegacion (Navbar)
- **Dashboard:** Va a la pagina principal
- **Registrar gasto:** Formulario para nuevo gasto
- **Perfil:** Gestion de perfil y tarjetas
- **Reportes:** Estadisticas y graficos de gastos
- **Recomendaciones:** Videos educativos
- **ChatBot:** Asistente virtual financiero
- **Inversiones:** Registro y seguimiento de inversiones
- **Retos:** Sistema de retos financieros
- **Juegos:** Trivia financiera
- **Evaluacion:** Evaluacion inicial de competencias
- **Mi Progreso:** Metricas y progreso individual
- **Alertas:** Alertas de riesgo crediticio
- **Biblioteca:** Contenido educativo
- **Logros:** Sistema de achievements
- **Narrativa:** Historia progresiva educativa
- **Fraudes:** Prevencion de fraudes digitales
- **Salir:** Cierra sesion

### Botones de Accion Comunes
- **Guardar/Registrar:** Guarda informacion en formularios
- **Cancelar:** Cancela la accion actual
- **Volver al Dashboard:** Navegacion rapida al inicio
- **Eliminar:** Elimina registros (con confirmacion)
- **Exportar PDF:** Genera reportes en PDF
- **Aprender Mas/Ver contenido:** Accede a contenido detallado
- **Completar:** Marca tareas como completadas
- **Aceptar reto:** Inicia un nuevo reto
- **Enviar:** Envia mensajes o formularios
- **Cerrar:** Cierra popups o ventanas modales

---

## FUNCIONALIDADES AUTOMATICAS

### Sistema de Logros
- Se verifican automaticamente al realizar acciones
- Popup global aparece cuando se desbloquea un logro nuevo
- Se verifica en:
  - Registro de gastos
  - Acceso al dashboard
  - Completar evaluaciones
  - Completar retos
  - Completar capitulos de narrativa

### Sistema de Alertas
- Generacion automatica de alertas cuando se detecta:
  - Gasto excesivo (excede limite mensual significativamente)
  - Limite proximo (cerca de alcanzar limite)
  - Deuda alta (si se registra informacion de deuda)
  - Solo pago minimo (patron detectado)
  - Sin ahorro mensual (no hay gastos en categoria Ahorro)

### Actualizacion de Metricas
- Se actualizan automaticamente:
  - Puntos del usuario
  - Progreso en retos
  - Visualizaciones de contenido
  - Dias activos
  - Sesiones totales

---

## METRICAS CAPTURADAS PARA INVESTIGACION

El sistema captura automaticamente:

1. **Competencias Financieras:**
   - Puntaje inicial y actual
   - Mejora porcentual
   - Brecha teorico-practica

2. **Comportamientos de Riesgo:**
   - Frecuencia de gastos excesivos
   - Uso de limite mensual
   - Patrones de endeudamiento

3. **Engagement:**
   - Dias activos en la aplicacion
   - Sesiones totales
   - Contenido visualizado
   - Capitulos completados
   - Logros desbloqueados

4. **Mejoras Observadas:**
   - Reduccion de riesgo crediticio
   - Aumento de ahorro
   - Mejora en competencias

---

## INTEGRACIONES EXTERNAS

### APIs Utilizadas:
1. **Twelve Data API:** Obtiene precios actuales de acciones para inversiones
2. **Abstract API:** Valida formato de emails en registro
3. **Google Gemini AI:** Asistente virtual financiero (chatbot)

### Servicios de Email:
- **SMTP Gmail:** Envio de emails de bienvenida y recuperacion de contrasea

---

## SISTEMA DE PUNTOS Y GAMIFICACION

### Puntos se otorgan por:
- Completar evaluacion inicial
- Registrar gastos (especialmente ahorros)
- Completar retos
- Completar capitulos de narrativa
- Desbloquear logros
- Responder correctamente en trivia

### Uso de Puntos:
- Ranking de usuarios
- Medida de progreso
- Motivacion para uso continuo

---

## SEGURIDAD Y PRIVACIDAD

- Encriptacion de contraseas
- Solo ultimos 4 digitos de tarjetas guardados
- Validacion de sesion en todas las vistas protegidas
- Tokens seguros para recuperacion de contrasea
- Proteccion CSRF en formularios

---

Este resumen cubre todas las funcionalidades principales de TuChanchita. Cada modulo esta diseñado para apoyar los objetivos de investigacion: mejorar competencias financieras, reducir comportamientos de riesgo, y promover educacion financiera practica en jovenes peruanos.

