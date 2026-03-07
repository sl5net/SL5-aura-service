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