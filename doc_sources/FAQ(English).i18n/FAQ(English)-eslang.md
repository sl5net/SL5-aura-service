### Preguntas frecuentes (inglés) 3.8.'2025 dom

**1. P: ¿Qué es SL5 Aura?**
R: Es un programa de conversión de voz a texto fuera de línea para todo el sistema. Le permite dictar en cualquier aplicación de su computadora (Windows, macOS, Linux) sin necesidad de una conexión a Internet.

**2. P: ¿Por qué debería usar esto? ¿Qué lo hace especial?**
R: **Privacidad.** Sus datos de voz se procesan al 100% en su máquina local y nunca se envían a la nube. Esto lo hace completamente privado y compatible con GDPR.

**3. P: ¿Es gratis?**
R: Sí, la Community Edition es completamente gratuita y de código abierto. Puede encontrar el código y el instalador en nuestro GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. P: ¿Qué necesito para usarlo?**
R: Una computadora y un micrófono. Para obtener la mayor precisión, recomendamos encarecidamente un micrófono de diadema exclusivo en lugar de un micrófono integrado para computadora portátil.

**5. P: La precisión no es perfecta. ¿Cómo puedo mejorarlo?**
R: Intente hablar claramente a un volumen y ritmo constantes. Reducir el ruido de fondo y utilizar un mejor micrófono marca la mayor diferencia.
Personalización del software (potencia avanzada): para una precisión de nivel superior, SL5 Aura utiliza una potente función llamada FuzzyMaps. Piense en estos como su diccionario personal e inteligente. Puede crear archivos de texto simples con reglas para corregir errores de reconocimiento comunes y recurrentes.

Ejemplo: si el software escucha con frecuencia "get hap" en lugar de "GitHub", puede agregar una regla que corrija esto automáticamente cada vez.

Beneficio: Esto le permite "enseñar" al software su jerga técnica específica, nombres de productos, abreviaturas o incluso crear conjuntos de reglas para vocabularios únicos. Al personalizar estos mapas, puede mejorar significativamente la precisión para su caso de uso específico.

***

#### **Parte 1: Preguntas generales**

**P: ¿Qué es SL5 Auro?**
R: SL5 Auro es un programa de conversión de voz a texto fuera de línea para todo el sistema. Le permite dictar texto en cualquier aplicación de su computadora (por ejemplo, su cliente de correo electrónico, un procesador de textos, un editor de código) sin necesidad de una conexión a Internet.

**P: ¿Qué significa "sin conexión" y por qué es importante?**
R: "Sin conexión" significa que todo el procesamiento de voz se realiza directamente en su computadora. Tus datos de voz **nunca** se envían a un servidor en la nube (como Google, Amazon u OpenAI). Esto proporciona máxima privacidad y seguridad, lo que lo hace ideal para información confidencial (por ejemplo, para abogados, médicos, periodistas) y cumple totalmente con las normas de protección de datos como GDPR.

**P: ¿Es realmente gratis? ¿Cuál es el truco?**
R: La "Edición comunitaria" es 100% gratuita y de código abierto. No hay trampa. Creemos en el poder de las herramientas de código abierto. Si considera que el software es valioso y desea respaldar su desarrollo continuo, puede hacerlo a través de nuestro [Ko-fi page](https://ko-fi.com/sl5).

**P: ¿Para quién es este software?**
R: Es para cualquiera que escriba mucho y quiera aumentar su eficiencia: escritores, estudiantes, programadores, profesionales médicos y legales, personas con limitaciones físicas o cualquiera que simplemente prefiera hablar a escribir.

#### **Parte 2: Instalación y configuración**

**P: ¿Qué sistemas operativos son compatibles?**
R: Se prueba y se confirma que el software funciona en Windows 11, Manjaro Linux, Ubuntu y macOS.

**P: ¿Cómo lo instalo en Windows?**
R: Proporcionamos un instalador sencillo con un solo clic. Es un script .Bat que requiere derechos administrativos para configurar el entorno y descargar los modelos necesarios. Una vez ejecutado, se encargará de todo por usted.

**P: La descarga de los modelos es muy grande. ¿Por qué?**
R: Los modelos de reconocimiento de voz son los que permiten que el software funcione sin conexión. Contienen todos los datos necesarios para que la IA comprenda su idioma. Los modelos más grandes y precisos pueden tener un tamaño de varios gigabytes. Nuestro nuevo programa de descarga los divide en partes más pequeñas y verificables para garantizar una descarga confiable.

**P: Estoy en Linux. ¿Cuál es el proceso?**
R: En Linux, normalmente clonarás el repositorio de GitHub y ejecutarás un script de configuración. Este script crea un entorno virtual Python, instala dependencias e inicia el servicio de dictado.

**P: Cuando hago doble clic en un archivo `.py` en Windows, se abre en un editor de texto. ¿Cómo lo ejecuto?**
R: Este es un problema común de Windows donde los archivos `.py` no están asociados con el intérprete de Python. No debe ejecutar los scripts de Python individuales directamente. Utilice siempre el script de inicio principal proporcionado (por ejemplo, un archivo `.bat`), ya que esto garantiza que se active primero el entorno correcto.

#### **Parte 3: Uso y características**

**P: ¿Cómo lo uso realmente para dictar?**
R: Primero, inicia el "servicio de dictado" ejecutando el script apropiado. Se ejecutará en segundo plano. Luego, usa un disparador (como una tecla de acceso rápido o un script dedicado) para iniciar y detener la grabación. El texto reconocido se escribirá automáticamente en cualquier ventana que esté actualmente activa.

**P: ¿Cómo puedo mejorar la precisión?**
R: 1. **Utilice un buen micrófono:** Un micrófono de diadema es mucho mejor que el micrófono integrado de una computadora portátil. 2. **Minimiza el ruido de fondo:** Un ambiente tranquilo es clave. 3. **Hable claramente:** Hable a un ritmo y volumen constantes. No murmures ni te apresures.
Personalización del software (potencia avanzada): para una precisión de nivel superior, SL5 Auro utiliza una potente función llamada FuzzyMaps. Piense en estos como su diccionario personal e inteligente. Puede crear archivos de texto simples con reglas para corregir errores de reconocimiento comunes y recurrentes.

Ejemplo: si el software escucha con frecuencia "get hap" en lugar de "GitHub", puede agregar una regla que corrija esto automáticamente cada vez.

Beneficio: Esto le permite "enseñar" al software su jerga técnica específica, nombres de productos, abreviaturas o incluso crear conjuntos de reglas para vocabularios únicos. Al personalizar estos mapas, puede mejorar significativamente la precisión para su caso de uso específico.

**P: ¿Puedo cambiar de idioma?**
R: Sí. El sistema admite la "recarga en caliente" en vivo de archivos de configuración. Puede cambiar el modelo de idioma en la configuración y el servicio cambiará a él instantáneamente sin necesidad de reiniciar.

**P: ¿Qué es "LanguageTool"?**
R: LanguageTool es un corrector gramatical y de estilo de código abierto que hemos integrado. Después de convertir su discurso en texto, LanguageTool corrige automáticamente los errores de transcripción comunes (por ejemplo, "correcto" frente a "escribir") y corrige la puntuación, lo que mejora significativamente el resultado final.

#### **Parte 4: Solución de problemas y soporte**

**P: Inicié el servicio, pero no ocurre nada cuando intento dictar.**
R: Verifique lo siguiente:
1. ¿El servicio sigue ejecutándose en su terminal/consola? Busque cualquier mensaje de error.
2. ¿Está seleccionado correctamente su micrófono como dispositivo de entrada predeterminado en su sistema operativo?
3. ¿Está el micrófono silenciado o el volumen demasiado bajo?

**P: Encontré un error o tengo una idea para una nueva característica. ¿Qué tengo que hacer?**
R: ¡Eso es genial! El mejor lugar para informar errores o sugerir funciones es abriendo un "Problema" en nuestro [GitHub repository](https://github.com/sl5net/Vosk-System-Listener).



**5. P: La precisión no es perfecta. ¿Cómo puedo mejorarlo?**
R: La precisión depende tanto de la configuración como de la personalización del software.

* **Su configuración (conceptos básicos):** Intente hablar claramente a un volumen y ritmo constantes. Reducir el ruido de fondo y utilizar un buen micrófono de diadema en lugar del micrófono integrado de una computadora portátil marca una gran diferencia.

* **Personalización de software (potencia avanzada):** Para una precisión de nivel superior, SL5 Auro utiliza una potente función llamada **FuzzyMaps**. Piense en estos como su diccionario personal e inteligente. Puede crear archivos de texto simples con reglas para corregir errores de reconocimiento comunes y recurrentes.

* **Ejemplo:** Si el software escucha con frecuencia "get hap" en lugar de "GitHub", puede agregar una regla que corrija esto automáticamente cada vez.
* **Beneficio:** Esto le permite "enseñar" al software su jerga técnica específica, nombres de productos, abreviaturas o incluso crear conjuntos de reglas para vocabularios únicos. Al personalizar estos mapas, puede mejorar significativamente la precisión para su caso de uso específico.




### Análisis profundo de la arquitectura: lograr una grabación continua al estilo "Walkie-Talkie"

Nuestro servicio de dictado implementa una arquitectura robusta basada en estados para brindar una experiencia de grabación continua y fluida, similar al uso de un walkie-talkie. El sistema siempre está listo para capturar audio, pero solo lo procesa cuando se activa explícitamente, lo que garantiza una alta capacidad de respuesta y un bajo uso de recursos.

Esto se logra desacoplando el bucle de escucha de audio del hilo de procesamiento y administrando el estado del sistema con dos componentes clave: un indicador de evento `active_session` y nuestro `audio_manager` para el control del micrófono a nivel del sistema operativo.

**La lógica de la máquina de estados:**

El sistema opera en un bucle perpetuo, administrado por una única tecla de acceso rápido que alterna entre dos estados principales:

1. **Estado ESCUCHANDO (Predeterminado/Listo):**
* **Condición:** El indicador `active_session` es `False`.
* **Estado del micrófono:** El micrófono está **silenciado** para "activar el micrófono()". El oyente Vosk está activo y esperando entrada de audio.
* **Acción:** Cuando el usuario presiona la tecla de acceso rápido, el estado cambia. El indicador `active_session` está establecido en `True`, lo que indica el inicio de un dictado "real".

2. **Estado PROCESANDO (El usuario ha terminado de hablar):**
* **Condición:** El usuario presiona la tecla de acceso rápido mientras el indicador `active_session` es `True`.
* **Estado del micrófono:** La **primera acción** es **silenciar** inmediatamente el micrófono mediante `mute_microphone()`. Esto detiene instantáneamente la transmisión de audio al motor Vosk.
*   **Acción:**
* El indicador `active_session` está establecido en `False`.
* El fragmento de audio final reconocido se recupera de Vosk.
* Con este texto final se abre el hilo de tramitación.
* Fundamentalmente, dentro de un bloque "finalmente", el hilo de procesamiento ejecuta "unmute_microphone()" al finalizar.

**La "Magia" de la señal de activación del silencio:**

La clave del bucle sin fin es la llamada final a `unmute_microphone()`. Tan pronto como finaliza el procesamiento del dictado "A" y se activa el micrófono, el sistema vuelve automática e instantáneamente al estado **ESCUCHA**. El oyente de Vosk, que estaba esperando pacientemente, inmediatamente comienza a recibir audio nuevamente, listo para capturar el dictado "B".

Esto crea un ciclo altamente receptivo:
`Presione -> Hablar -> Presione -> (Silenciar y procesar) -> (Activar silencio y escuchar)`

Esta arquitectura garantiza que el micrófono solo esté silenciado durante el breve período de procesamiento de texto, lo que hace que el sistema parezca instantáneo para el usuario, manteniendo un control sólido y evitando grabaciones fuera de control.