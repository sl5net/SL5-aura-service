Además de las muchas opciones de búsqueda, probablemente exista una búsqueda de texto completo en su entorno de desarrollo. También puede utilizar:

scripts/search_rules/search_rules.sh

Esto le permite buscar en los mapas existentes o en el código fuente o la documentación. y luego puedes abrir la paz que encontraste en tu editor favorito o abrirla en github o... configura el script como lo necesites.

MAPS_DIR es configurable mediante argumento posicional o variable de entorno

El script mantiene su valor predeterminado codificado pero permite anulaciones:

- Prioridad: 1) primer parámetro posicional ($1), 2) var env MAPS_DIR existente,
3) valor predeterminado codificado "$SL5NET_AURA_PROJECT_ROOT/config/maps".
- Mejora la flexibilidad para CI, anulaciones locales y pruebas sin editar el script.
- Agrega comillas y una verificación de existencia del directorio para fallar temprano si la ruta no es válida.

Uso de ejemplo:
- ./search_rules.sh usa el valor predeterminado
- ./search_rules.sh ./docs utiliza la ruta proporcionada
- MAPS_DIR=/env/maps ./search_rules.sh

Esto preserva la compatibilidad con versiones anteriores y al mismo tiempo hace que la configuración sea explícita.

También hay una versión para PC con Windows (en esta carpeta) que puede hacer un poco menos: search_rules.ps1


(s, 28.3.'26 23:07 sábado)