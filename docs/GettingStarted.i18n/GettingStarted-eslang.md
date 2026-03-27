# Primeros pasos con SL5 Aura

> **Requisitos previos:** Ha completado el script de configuración y configurado su tecla de acceso rápido.
> Si no, consulte el [Installation section in README.md](../../README.i18n/README-eslang.md#installation).

---

## Paso 1: Tu primer dictado

1. Inicie Aura (si aún no se está ejecutando):
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
Espere el sonido de inicio; eso significa que Aura está lista.

2. Haga clic en cualquier campo de texto (editor, navegador, terminal).
3. Presione su tecla de acceso rápido, diga **"Hola mundo"**, presione la tecla de acceso rápido nuevamente.
4. Observe cómo aparece el texto.

> **¿No pasó nada?** Verifique `log/aura_engine.log` para ver si hay errores.
> Solución común para CachyOS/Arch: `sudo pacman -S mimalloc`

---

## Paso 2: escribe tu primera regla

La forma más rápida de agregar una regla personal:

1. Abra `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Agregue una regla dentro de `FUZZY_MAP_pre = [...]`:
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **Guardar**: Aura se recarga automáticamente. No es necesario reiniciar.
4. Dicte "hola mundo" y observe cómo se convierte en "Hola mundo".

> Consulte `docs/FuzzyMapRuleGuide.md` para obtener la referencia completa de la regla.

### El Oma-Modus (atajo para principiantes)

¿Aún no conoces las expresiones regulares? Ningún problema.

1. Abra cualquier `FUZZY_MAP_pre.py` vacío en el sandbox.
2. Escriba solo una palabra simple en su propia línea (sin comillas, sin tupla):
   ```
   raspberry
   ```
3. Guardar: el sistema Auto-Fix detecta la palabra desnuda y automáticamente
lo convierte en una entrada de regla válida.
4. Luego podrás editar el texto de reemplazo manualmente.

Esto se llama **Oma-Modus** y está diseñado para usuarios que desean resultados sin
aprender expresiones regulares primero.

---

## Paso 3: Aprende con Koans

Los koans son pequeños ejercicios en los que cada uno enseña un concepto.
Viven en `configmaps/koans deutsch/` y `configmaps/koans english/`.

Comience aquí:

| Carpeta | Lo que aprendes |
|---|---|
| `00_koan_oma-modus` | Auto-Fix, primera regla sin expresiones regulares |
| `01_koan_erste_schritte` | Su primera regla, conceptos básicos del oleoducto |
| `02_koan_listen` | Trabajar con listas |
| `03_koan_schwierige_namen` | Coincidencia difusa para nombres difíciles de reconocer |
| `04_koan_kleine_helfer` | Atajos útiles |

Cada carpeta koan contiene un `FUZZY_MAP_pre.py` con ejemplos comentados.
Descomente una regla, guárdela, dicte la frase desencadenante y listo.

---

## Paso 4: Ir más allá

| Qué | Dónde |
|---|---|
| Referencia completa de la regla | `docs/FuzzyMapRuleGuide.md` |
| Crea tu propio complemento | `docs/CreatingNewPluginModules.md` |
| Ejecute scripts de Python desde reglas | `docs/advanced-scripting.md` |
| DEV_MODE + configuración del filtro de registro | `docs/Developer_Guide/dev_mode_setup.md` |
| Reglas sensibles al contexto (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |