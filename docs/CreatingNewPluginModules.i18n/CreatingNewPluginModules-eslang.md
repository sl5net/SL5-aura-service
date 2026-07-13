## Creación de nuevos módulos complementarios (docs/CreatingNewPluginModules.md)

Nuestro marco utiliza un potente sistema de descubrimiento automático para cargar módulos de reglas. Esto hace que agregar nuevos conjuntos de comandos sea simple y limpio, sin necesidad de registrar manualmente cada componente nuevo. Esta guía explica cómo crear, estructurar y administrar sus propios módulos personalizados.

### El concepto central: módulos basados en carpetas

Un módulo es simplemente una carpeta dentro del directorio `config/maps/`. El sistema escanea automáticamente este directorio y trata cada subcarpeta como un módulo cargable.

### Guía paso a paso para crear un módulo

Siga estos pasos para crear un nuevo módulo, por ejemplo, para guardar macros para un juego específico.

**1. Navega al directorio de mapas**
Todos los módulos de reglas residen en la carpeta `config/maps/` del proyecto.

**2. Cree su carpeta de módulos**
Crea una nueva carpeta. El nombre debe ser descriptivo y utilizar guiones bajos en lugar de espacios (por ejemplo, `my_game_macros`, `custom_home_automation`).

**3. Agregar subcarpetas de idioma (paso crítico)**
Dentro de la carpeta de su nuevo módulo, debe crear subcarpetas para cada idioma que desee admitir.

* **Convención de nomenclatura:** Los nombres de estas subcarpetas **deben ser códigos de idioma y configuración regional válidos**. El sistema utiliza estos nombres para cargar las reglas correctas para el idioma activo.
* **Ejemplos correctos:** `de-DE`, `en-US`, `en-GB`, `pt-BR`
* **Advertencia:** Si utiliza un nombre no estándar como `alemán` o `inglés_rules`, el sistema ignorará la carpeta o la tratará como un módulo separado, no específico de un idioma.

**4. Agregue sus archivos de reglas**
Coloque sus archivos de reglas (por ejemplo, `FUZZY_MAP_pre.py`) dentro de la subcarpeta del idioma apropiado. La forma más sencilla de comenzar es copiar el contenido de una carpeta de módulo de idioma existente para utilizarlo como plantilla.

### Ejemplo de estructura de directorio

```
config/
└── maps/
    ├── standard_actions/      # An existing module
    │   ├── de-DE/
    │   └── en-US/
    │
    └── my_game_macros/        # <-- Your new custom module
        └── de-DE/             # <-- Language-specific rules
            └── FUZZY_MAP_pre.py

        ├── __init__.py        # <-- Important: This Empty File must be in every Folders!!
            
```

### Administrar módulos en la configuración

El sistema está diseñado para requerir una configuración mínima.

#### Habilitación de módulos (el valor predeterminado)

Los módulos están **habilitados de forma predeterminada**. Siempre que exista una carpeta de módulo en `config/maps/`, el sistema la encontrará y cargará sus reglas. **No es necesario agregar una entrada a su archivo de configuración para habilitar un nuevo módulo.**

#### Deshabilitar módulos

Para deshabilitar un módulo, debe agregar una entrada en el diccionario `PLUGINS_ENABLED` dentro de su archivo de configuración y establecer su valor en `False`.

(Opcional) Para Verdadero/Falso, también puedes usar 1/0. Sin embargo, esto es poco común y puede reducir la legibilidad.

**Ejemplo (`config/settings.py`):**
```python
# A dictionary to explicitly control the state of modules.
# The key is the path to the module relative to 'config/maps/'.
PLUGINS_ENABLED = {
    "empty_all": False,

    # This module is explicitly enabled.
    "git": True,

    # This module is also enabled. Second Parameter is per default True. Not False means True.
    # "wannweil": False,

    # This module is explicitly disabled.
    "game": False,

    # This module is disabled by other rule
    "game/game-dealers_choice": True,

    # This module is disabled by other rule
    "game/0ad": True,
}


```
### Notas de diseño importantes

* **Comportamiento predeterminado: Ninguna entrada equivale a "Verdadero"**
Si un módulo no aparece en el diccionario `PLUGINS_ENABLED`, se considera **activo** de forma predeterminada. Este diseño mantiene limpio el archivo de configuración, ya que solo necesita enumerar las excepciones.

* **Abreviatura de habilitación**
Su sistema de configuración también entiende que enumerar una clave de módulo sin un valor implica que está habilitado. Por ejemplo, agregar `"wannweil"` al diccionario es lo mismo que agregar `"wannweil": True`. Esto proporciona una abreviatura conveniente para habilitar módulos.
  
(Opcional) Para Verdadero/Falso, también puedes usar 1/0. Sin embargo, esto es poco común y puede reducir la legibilidad.

* **Deshabilitar módulos principales:** El comportamiento previsto es que al deshabilitar un módulo principal   
deshabilite automáticamente todos sus módulos secundarios y subcarpetas de idioma. Por ejemplo, configurar `"standard_actions": False` debería evitar que se carguen `de-DE` y `en-US`. (27.10.'25 lunes)
  
*   **meta**
El objetivo es mejorar aún más este sistema. Por ejemplo, proporcionar una forma de respetar la configuración del módulo secundario incluso si el principal está deshabilitado, o introducir reglas de herencia más complejas. (27.10.'25 lunes)


  
  
  
t1- Es ist in der Tat wesentlich benutzerfreundlicher und komfortabler, die Steuerung über die Sprachbefehle direkt in diesem Dokumentationsabschnitt hervorzuheben [1].

t2- Wir erweitern den Entwurf um eine klare Beschreibung der Tasten- bzw. Sprachsteuerungsbefehle (como „Aura, Lernmodus einschalten / ausschalten“) y erklären kurz, como `toggle_learning.py` das Aus- und Einkommentieren automatisiert [2].


### Habilitación del modo de aprendizaje (entrenamiento inigualable)

Para permitir que su módulo personalizado aprenda automáticamente frases no reconocidas cuando el "Lernmodus" (modo de aprendizaje) está activo, puede agregar una regla general en la parte inferior ** de su lista `FUZZY_MAP_pre`.

Esta regla invoca el complemento de entrenamiento inigualable cuando ninguna otra regla específica en su archivo coincide:

```python
    # --- Training-Plugin (dynamically toggled by the learning mode) ---
    (f'{str(__file__)}', r'^(.*)$', 10, {
        'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']
    }),
```

El complemento de entrenamiento usa `f'{str(__file__)}'` para ubicar su archivo y agregar automáticamente la frase no reconocida al primer grupo de reglas disponible (como su grupo de comandos principal).

#### Alternar el modo de aprendizaje mediante comandos de voz

En lugar de editar archivos manualmente, la forma más cómoda de administrar esta función es mediante comandos de voz integrados:

* **Para habilitar:** Diga *"Aura, modo de aprendizaje activado"* o *"Aura, Lernmodus starten"*.
* **Para desactivar:** Diga *"Aura, modo de aprendizaje desactivado"* o *"Aura, Lernmodus stoppen"*.

Estos comandos activan `toggle_learning.py` detrás de escena, que automáticamente comenta o descomenta las líneas generales en sus archivos de mapas activos.
  
  
  
  
*Consejo: Después de definir sus patrones de expresiones regulares, ejecute `python3 tools/map_tagger.py` para generar automáticamente ejemplos de búsqueda para las herramientas CLI. Consulte [Map Maintenance Tools](../../Developer_Guide/Map_Maintenance_Tools-eslang.md) para obtener más detalles.*