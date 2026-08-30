# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/it-terms/de-DE/FUZZY_MAP_pre.py

# archivo de configuración/maps/plugins/it-terms/FUZZY_MAP_pr.py

# Beispiel: https://www.it-begriffe.de/#L

import re

# desde pathlib importar ruta como p; importar sistema operativo como o

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


# config/maps/plugins/it-terms/de-DE/FUZZY_MAP_pre.py:17

FUZZY_MAP_pre = [
    # EXAMPLE: depurarABZ

    ('debugABZxxx', r'depurarABZ'),  # ← komplett standalone, keine Gruppe

    # Regla de inicio: activa el grupo 'sandbox_test' en "iniciar sandbox"

    # EXAMPLE: caja de personal

    ('Sandbox', r'^personal\w* .*caja.*', 100, {'group_start': 'sandbox_test'}),

    # Regla interna 1: Reemplazar “manzana” por “pera” (si está disponible)

    # EXAMPLE: manzana

    ('birne', r'manzana'),

    # Regla interna 2: Reemplace "plátano" (si está presente); de lo contrario, se agrega "plátano".

    # EXAMPLE: banana

    ('banane', r'banana'),

    # Marcador final pasivo para 'sandbox_test'

    (None, r'', 100, {'group_end': 'sandbox_test'}),
    (None, r'', 100, {'group_end': 'sandbox_test'}),

    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.



    # EXAMPLE: archivo JSON


    ('JSON Datei', r'^\b(JSON(\sArchivo)?|caza|jacen|jason|deambular)\s*(archivo|detalle)(\b)$', 80, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Exportación JSON


    ('JSON Export', r'^\b(JSON exportar|jacen exportar)(\b)$', 80, {'command_flags': re.IGNORECASE}),


    # Pruébalo


    # la silla liquida

    # EXAMPLE: la herramienta de idioma

    # IdiomaHerramienta

    # EXAMPLE: heces liquidas

    ('das LanguageTool', r'\b(el) (IdiomaHerramienta|líquido Silla)(\b)', 80, {'command_flags': re.IGNORECASE}),
    ('LanguageTool', r'\b(líquido Silla)(\b)', 80, {'command_flags': re.IGNORECASE}),

    # del enlace que herramientas

    # EXAMPLE: IdiomaHerramienta


    ("des LanguageTool's", r'\b(IdiomaHerramienta|des enlace w\w+ herramientas)(\b)', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Manjaro


    ('Manjaro Linux', r'^(Manjaro|qué chado|monje|matcha dónde) (linux|carolina\w*)$', 80, {'command_flags': re.IGNORECASE}),

    # Monk CarolinCon CarolinIf CarolineManjaro Linux

    # EXAMPLE: Manjaro Linux

    ('Linux Manjaro', r'^(linux) (Manjaro|hombre Controlar|justo jaro|se convierte jaro|matcha frotar)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Manjaro Linux

    ('Linux Manjaro', r'^(linux) mamá\w*\s*\w*a\s*r[UNED]m?$', 80, {'command_flags': re.IGNORECASE}),


    # Monk CarolinCon CarolinIf CarolineManjaro Linux

    # EXAMPLE: Linux Manjarovelux

    ('Linux Manjaro', r'^(linux|velux) (Manjaro|matcha|se convierte jaro|se convierte jaro|con jaro)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Linux Manjarovelux

    ('Linux Manjaro', r'^velux m\w+\s*[UNED]$', 80, {'command_flags': re.IGNORECASE}),

    # velux m\w+\s*[ou]


    # velux matcha r u

    # velux con jaro


    # partido velux


    # Linux Manjaro Velux veces Karo

    # coincide con Linux




    # EXAMPLE: temas de debate

    ('Debug-Ausgaben', r'^(debate gasto)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: programa cargado

    ('Programm geladen. Viel Spaß', r'^(Programa[m]+ cargado)$', 80, {'command_flags': re.IGNORECASE}),




    # EXAMPLE: Archivo de registro

    ('Logdatei', r'^(Archivo de registro|archivo de cocina|registro-archivo)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Archivo de registro

    ('Logfile', r'^(\b)(Archivo de registro)(\b)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: alivio

    ('release', r'^(\b)(liberar|alivio|liberar|alivio|OMS este)(\b)$', 75, {'command_flags': re.IGNORECASE}),

# Prácticamente en mujeres

# Ritual en Deibel

# virtual en weibel

# Prácticamente a distancia

# virtuales en blanco

# Ritual en Weimarvirtual en Weimar

# Entorno virtual

# virtual en viudas blancas en WeimarRitual en blanco#Entorno virtual

# Ritual en Deibelvirtual en weibelVirtual en DeibelYa estará en vino

# Ya estará en vino, será difícil en cálido.

# se vuelve difícil en la economía cálida en Weimar economía en Weimar Entorno virtual

# viudo de blanco con

# Cada uno de los paganos conectará a una mujer virtual. Será en Deibel.

# Bachelorette DeibelVirtual en el cortejoVirtual en el giro Jabalíes en las habitaciones Entorno virtual Aquí se utiliza Titán en un entorno ritual

# virtual en blancovirtual en habitaciones


    # EXAMPLE: Virtual

    ('Virtual environment', r'\b(Virtual|virtual|viuda\w*|viudo|se convierte ya|se convierte difícil|negocio|jabalí)\w* (en |blanco |en el )?(mujer|blanco|weima|metal|blanco|cálido|blanco con|giro|claro|pruebas|billetera)\w*\b', 75, {'command_flags': re.IGNORECASE,
            'skip_list': ['LanguageTool'],
    }),


# El titanio se utiliza aquí de forma virtual en blanco.

# Entorno virtual Titán se conectará aquí en un entorno ritual

# Biden se confunde aquí con una mujer virtual

# El titanio se utiliza en todas las esposas de viudas.

# Titán será, aquí yace una persona no, ambos aquí serán tu unción de viuda para convertirse en ambos aquí tu unción de viuda será para quien estúpido

# Biden se confunde aquí con una mujer virtual

# Ambos se unirán aquí en un paseo por el cuerpo.

# Aquí se utiliza titanio en una mujer virtual.

# titán estará en weibel

# Ambos se utilizan aquí en un caso.

# Además, aquí se utiliza una entrada virtual.

# Cada viuda usará de su esposa.

# Aquí se utiliza titanio en un metal blanco virtual.

# Los tiempos se conectarán aquí en una viuda en Weimar.

# Los tiempos se conectarán aquí en una viuda en Weimar.

# El fracaso aquíSkaterTitan alguna vez se usará en un viudo con

# El titanio alguna vez se usará en un viudo en blanco

# Times se utiliza aquí en un jabalí en hembra.

# ützensagTitan se utiliza aquí en un entorno ritual


    # EXAMPLE: Brighton

    ('Python', r'^(\b)(B2026-0131-2125derecho|amplio ya|Paracaídas|látigo)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ambos se utilizan aquí en un entorno virtual.

    ('Python wird hier in einer Virtual environment verwendet', r'^(ambos se convierte aquí en uno Virtual ambiente también usado|Ambos se convierte aquí en uno se convierte para el caer usado|Además se convierte aquí en uno virtual en en con usado|Sostener se convierte alguien viuda se convierte mujer usar|titanio se convierte aquí en uno virtual en mujer usado|ambos se convierte aquí en uno virtual en blanco también usado)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: sdf b bytes encanto b

    ('PyCharm', r'^sdf(\b)(bytes encanto)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: pálido

    ('default', r'^(\b)(d pálido)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Penetrar

    ('String', r'^(\b)(Penetrar)(\b)$', 75, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: heces cortadas

    ('Code Abschnitt', r'\bkot\s*secciones\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: alaba el caso

    ('lowerCase', r'\manchas\s*Caso\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: botón de parada

    ('StopButton', r'\bstob\s*botón\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: alaba el caso

    ('lowerCase', r'\manchas\s*Caso\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Clave automática

    ('AutoKey', r'\bCoche\s*k\w+\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 0 d.C.

    ('0 A.D.', r'\o zewa d\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Juego 0 d.C.

    ('0 A.D. spiel', r'\o zewa d juego\W*\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Juego 0 d.C.

    ('GitHub SL5', r'\github él son 5\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: guerra x

    ('regex', r'\b(guerra x|rekik|Micro x|almiar x|Resúmenes)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: proceso de imagen

    ('Build Prozess', r'\imagen proceso\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: fuente abierta

    ('opensource', r'\fuente abierta\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: tubo

    ('|', r'\b(tubo|tubo símbolo|pagado símbolo|conducir símbolo|PayPal símbolo|energía|deberes Simba|conducir Simba|PayPal Simba)\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: tubo

    ('|', r'\b(tubo|tubo|pagado|conducir|PayPal|energía|deberes|conducir|PayPal) (símbolo|Simba|simple|sencillo|brillar|SIM)\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: en

    ('@', r'\b(en|ed) (símbolo|Simba|simple|sencillo|brillar|SIM|champú|mala palabra|Firmar)\b', 75, {'command_flags': re.IGNORECASE}),
# champú ed el cariño se estaba quejando

# Hola, PaypalSímbolo pagadoPepSímbolo femeninoSímbolo TreibPythonSímbolo de PaypalSimba asada femeninaHembraPaypal Simbafeit SchimpfTribst simpleVeit SchimmelPep shimmer

# Snacks en SIMPaypal SIMHalf SIMPep simple||Hornear galletas


 # Logfile-Duden Logfile-Duden Logfile-Logfile Alcanzado hacia el norte Logfile-Logfile Logfile-Logfile Edita Alivio Vernissage Crédito El crédito establece Quién es Editar Quién es





]



