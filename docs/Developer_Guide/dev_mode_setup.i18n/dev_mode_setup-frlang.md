# Guide de configuration DEV_MODE

## Le problème

puisque nous sommes compatibles avec Weyland, nous utilisons « threading.Lock » pour la journalisation.

Maintenant (21.3.'26 samedi), les règles de journalisation ont changé. À Manjaro, cela ne posait aucun problème.

Lorsque `DEV_MODE = 1` est actif, Aura produit des centaines d'entrées de journal par seconde
à partir de plusieurs fils de discussion. Cela peut provoquer un blocage de `SafeStreamToLogger`, ce qui rend
Aura se bloque après le premier déclenchement de la dictée.

## Le correctif : utilisez le filtre LOG_ONLY

Lors du développement avec `DEV_MODE = 1`, vous **devez** également configurer un filtre de journal dans :
`config/filters/settings_local_log_filter.py`

### Filtre de travail minimal pour DEV_MODE :
```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"Title",
    r"window",
    r":st:",
]
LOG_EXCLUDE = []
```

## One-liner pour settings_local.py
Ajoutez ce commentaire comme rappel à côté de votre paramètre DEV_MODE :
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

## Cause première
`SafeStreamToLogger` utilise un `threading.Lock` pour protéger les écritures sur la sortie standard.
Sous une charge de journal élevée (DEV_MODE), les conflits de verrouillage provoquent des blocages sur les systèmes
avec une planification de threads agressive (par exemple CachyOS avec des noyaux/glibc plus récents).