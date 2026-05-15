# Perfiles de filtro de registro

El filtro de registro activo siempre es `config/filters/settings_local_log_filter.py`.

## Perfiles

Los perfiles predefinidos se almacenan en `config/filters/.backlock/`:

| Perfil | Descripción |
|---|---|
| `primera_ejecución` | Salida mínima: errores y estado únicamente. Se aplica automáticamente en el primer inicio. |
| `normal` | Filtro estándar para uso diario. |

## Cambiar perfil manualmente

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

## Agregar un perfil personalizado

1. Cree una nueva carpeta en `config/filters/.backlock/my_profile/`
2. Copie un `settings_local_log_filter.py` existente en él y edítelo según sus necesidades.
3. Aplíquelo con `cp` como se muestra arriba.

## Cambio automático de perfil

En el primer inicio, Aura detecta que el directorio `log/` aún no existe y
copia automáticamente el perfil `first_run` como filtro activo.