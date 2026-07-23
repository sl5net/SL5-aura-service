# Guide des règles FUZZY_MAP

## Format de règle

```python
('replacement', r'regex_pattern', threshold, {'command_flags': re.IGNORECASE})
```

| Poste | Nom | Descriptif |
|---|---|---|
| 1 | remplacement | Le texte de sortie après la correspondance de la règle |
| 2 | modèle | Regex ou chaîne floue à comparer |
| 3 | seuil | Pour les règles regex : ignorées. Pour les règles floues : score de correspondance minimum (0–100) |
| 4 | options | Dictionnaire facultatif (voir « Référence des options » ci-dessous). Utilisez « 0 » ou omettez les valeurs par défaut |
### Remplacements bruts
Par défaut (`False`), les chaînes de remplacement sont traitées par `re.sub()` de Python, qui prend en charge l'utilisation de références arrière d'expression régulière comme `\1` ou `\2` pour insérer des groupes capturés (par exemple : `(r'\1', r'(\d)\s+(?=\d)', 95)`).
Si votre remplacement est une chaîne multiligne ou contient des barres obliques inverses non échappées (telles que des modèles de code ou des chemins) et doit être conservé exactement tel quel, activez « raw_replacement : True » dans le dictionnaire d'options :
```python
(System_Instructions, r'^(system instructions)$', 10, {'command_flags': re.IGNORECASE, 'raw_replacement': True})
```

### Options configurables par l'utilisateur disponibles :

* **`command_flags`** (entier) : indicateurs Regex utilisés lors de la compilation du modèle.
*Exemple :* `{'command_flags' : re.IGNORECASE}`
* **`raw_replacement`** (booléen) : Lorsque `True`, le texte de remplacement est traité comme une chaîne littérale pure et contourné par l'analyse de la barre oblique inverse `re.sub` de Python. Crucial pour les invites multilignes ou les chaînes avec des barres obliques inverses non échappées (`\`).
*Exemple :* `{'raw_replacement' : True}`
* **`cache`** (booléen) : bascule le cache des résultats AURA. Définissez sur « False » pour les règles qui génèrent une sortie dynamique (par exemple, l'heure actuelle, des blagues aléatoires) afin de garantir qu'elles sont évaluées à nouveau à chaque match.
*Exemple :* `{'cache' : Faux}`
* **`skip_list`** (liste de chaînes) : Spécifie les modules de pipeline de post-traitement à ignorer lorsque cette règle correspond.
*Exemple :* `{'skip_list' : ['LanguageTool']}` (ignore la vérification grammaticale)
* **`only_in_windows`** (liste de chaînes regex) : restreint la règle au déclenchement uniquement si le titre de la fenêtre active correspond à l'un des modèles spécifiés.
*Exemple :* `{'only_in_windows' : [r'^Mozilla Firefox$', r'Chrome']}`
* **`exclude_windows`** (liste de chaînes regex) : empêche la règle de se déclencher si le titre de la fenêtre active correspond à l'un des modèles spécifiés.
*Exemple :* `{'exclude_windows' : [r'Terminal', r'Claude']}`
* **`window_ignore_case`** (booléen) : contrôle si la correspondance de fenêtre (`only_in_windows` / `exclude_windows`) est évaluée sans tenir compte de la casse (`True`) ou en tenant compte de la casse (`False`). En cas d'omission, revient au paramètre global `LOWERCASE_WINDOW_TITLES` dans `config/settings.py`.
*Exemple :* `{'window_ignore_case' : False}`
* **`on_match_exec`** (liste des objets Path/string) : chemins vers les scripts/plugins qui doivent être exécutés lorsque cette règle correspond (fortement utilisé par les règles fourre-tout et de secours).
*Exemple :* `{'on_match_exec' : [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## Logique du pipeline
- Les règles sont traitées **de haut en bas**


## Logique du pipeline

- Les règles sont traitées **de haut en bas**
- **Toutes** les règles de correspondance sont appliquées (cumulatives)
- Un **fullmatch** (`^...$`) arrête immédiatement le pipeline
- Les règles antérieures ont la priorité sur les règles ultérieures

## Modèles courants

### Faire correspondre un seul mot (limite du mot)
```python
('Python', r'\bpython\b', 0, {'command_flags': re.IGNORECASE})
```

### Faire correspondre plusieurs variantes
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'command_flags': re.IGNORECASE})
```

### Fullmatch – arrête le pipeline
```python
('hello koan', r'^.*$', 0, {'command_flags': re.IGNORECASE})
```
⚠️ Cela correspond à **tout**. Le pipeline s'arrête ici. Les règles antérieures restent prioritaires.

### Faire correspondre le début de l'entrée
```python
('Note: ', r'^notiz\b', 0, {'command_flags': re.IGNORECASE})
```

### Correspond à l'expression exacte
```python
('New York', r'\bnew york\b', 0, {'command_flags': re.IGNORECASE})
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
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'command_flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'command_flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'command_flags': re.IGNORECASE}),
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
    ('My Rule', r'my rule', 0, {'command_flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**Pourquoi ?** La correction automatique d'Aura analyse uniquement le premier ~ 1 Ko d'un fichier.
Si vos règles apparaissent après un long en-tête, Auto-Fix ne peut pas les trouver ou les réparer.
Le commentaire du chemin sur la ligne 1 est également recommandé : il aide les humains à identifier rapidement le fichier.