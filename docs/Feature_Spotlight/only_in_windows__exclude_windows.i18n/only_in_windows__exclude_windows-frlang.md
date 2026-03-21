# Attributs de règle : `only_in_windows` et `exclude_windows`

Ces deux attributs contrôlent **dans quelles fenêtres actives une règle est autorisée à se déclencher**.
Ils sont définis dans le dictionnaire « options » d'une règle et acceptent une **liste de modèles d'expressions régulières**
qui correspondent au titre de la fenêtre active actuelle (`_active_window_title`).

---

## `only_in_windows`

La règle se déclenche **uniquement si** le titre de la fenêtre active correspond à **au moins un** des modèles donnés.
Toutes les autres fenêtres sont ignorées.

**Cas d'utilisation :** Restreindre une règle à une application spécifique.


> La règle se déclenchera **uniquement** lorsque Firefox ou Chromium est la fenêtre active.

---

## `exclude_windows`

La règle se déclenche **sauf** si le titre de la fenêtre active correspond à **au moins un** des modèles donnés.
Les fenêtres correspondantes sont ignorées.

**Cas d'utilisation :** Désactivez une règle pour des applications spécifiques.

Exemples

```py
Targets
    Occurrences of 'exclude_windows' in Project with mask '*pre.py'
Found occurrences in Project with mask '*pre.py'  (3 usages found)
    Usage in string constants  (3 usages found)
        STT  (3 usages found)
            config/maps/plugins/z_fallback_llm/de-DE  (3 usages found)
                FUZZY_MAP_pre.py  (3 usages found)
                    90 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    105 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    119 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd'],

```



La correspondance est **insensible à la casse** et utilise des **expressions régulières** Python.

---

## Résumé

| Attribut | Se déclenche quand... |
|-----------------------|--------------------------------------------|
| `only_in_windows` | le titre de la fenêtre **correspond** à l'un des modèles |
| `exclude_windows` | le titre de la fenêtre **ne correspond** à aucun modèle |

---

## Voir aussi

- `scripts/py/func/process_text_in_background.py` — lignes ~1866 et ~1908
- `scripts/py/func/get_active_window_title.py` — comment le titre de la fenêtre est récupéré