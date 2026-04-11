# Guide des règles FUZZY_MAP

## Format de règle

```python
('replacement', r'regex_pattern', threshold, {'flags': re.IGNORECASE})
```

| Poste | Nom | Descriptif |
|---|---|---|
| 1 | remplacement | Le texte de sortie après la correspondance de la règle |
| 2 | modèle | Regex ou chaîne floue à comparer |
| 3 | seuil | Ignoré pour les règles regex. Utilisé pour la correspondance floue (0–100) |
| 4 | drapeaux | `{'flags' : re.IGNORECASE}` pour insensible à la casse, `0` pour sensible à la casse |

## Logique du pipeline

- Les règles sont traitées **de haut en bas**
- **Toutes** les règles de correspondance sont appliquées (cumulatives)
- Un **fullmatch** (`^...$`) arrête immédiatement le pipeline
- Les règles antérieures ont la priorité sur les règles ultérieures

## Modèles courants

### Faire correspondre un seul mot (limite du mot)
```python
('Python', r'\bpython\b', 0, {'flags': re.IGNORECASE})
```

### Faire correspondre plusieurs variantes
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'flags': re.IGNORECASE})
```

### Fullmatch – arrête le pipeline
```python
('hello koan', r'^.*$', 0, {'flags': re.IGNORECASE})
```
⚠️ Cela correspond à **tout**. Le pipeline s'arrête ici. Les règles antérieures restent prioritaires.

### Faire correspondre le début de l'entrée
```python
('Note: ', r'^notiz\b', 0, {'flags': re.IGNORECASE})
```

### Correspond à l'expression exacte
```python
('New York', r'\bnew york\b', 0, {'flags': re.IGNORECASE})
```

## Emplacements des fichiers

| Fichier | Phases | Descriptif |
|---|---|---|
| `FUZZY_MAP_pre.py` | Outil pré-langage | Appliqué avant la vérification orthographique |
| `FUZZY_MAP.py` | Outil post-langage | Appliqué après vérification orthographique |
| `PUNCTUATION_MAP.py` | Outil pré-langage | Règles de ponctuation |

## Conseils

- Mettez les règles **spécifiques** avant les règles **générales**
- Utilisez `^...$` fullmatch uniquement lorsque vous souhaitez arrêter tout traitement ultérieur
- `FUZZY_MAP_pre.py` est idéal pour les corrections avant la vérification orthographique
- Testez les règles avec : "votre entrée de test" dans la console Aura
- Les sauvegardes sont créées automatiquement sous `.peter_backup`

## Exemples

```python
FUZZY_MAP_pre = [
    # Correct a common STT mistake
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'flags': re.IGNORECASE}),
]
```

## Votre première règle – étape par étape

1. Ouvrez `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Ajoutez votre règle dans `FUZZY_MAP_pre = [...]`
3. Enregistrer — Aura se recharge automatiquement, aucun redémarrage n'est nécessaire
4. Dictez votre phrase déclencheur et regardez-la se déclencher


## Structure de fichier recommandée

Mettez vos règles **avant** les longs blocs de commentaires :
```python
# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('My Rule', r'my rule', 0, {'flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**Pourquoi ?** La correction automatique d'Aura analyse uniquement le premier ~ 1 Ko d'un fichier.
Si vos règles apparaissent après un long en-tête, Auto-Fix ne peut pas les trouver ou les réparer.
Le commentaire du chemin sur la ligne 1 est également recommandé : il aide les humains à identifier rapidement le fichier.