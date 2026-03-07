# Premiers pas avec SL5 Aura

## Qu'est-ce que SL5 Aura ?

SL5 Aura est un assistant vocal hors ligne qui convertit la parole en texte (STT) et applique des règles configurables pour nettoyer, corriger et transformer la sortie.

Cela fonctionne sans interface graphique – tout fonctionne via CLI ou console.

## Comment ça marche

```
Microphone → Vosk (STT) → Maps (Pre) → LanguageTool → Maps (Post) → Output
```

1. **Vosk** convertit votre discours en texte brut
2. **Pre-Maps** nettoie et corrige le texte avant la vérification orthographique
3. **LanguageTool** corrige la grammaire et l'orthographe
4. **Post-Maps** applique les transformations finales
5. **La sortie** est le texte final propre (et éventuellement TTS)

## Vos premiers pas

### 1. Démarrez Aura
```bash
python main.py
```

### 2. Test avec l'entrée de la console
Tapez `s` suivi de votre texte :
```
s hello world
```

### 3. Voir une règle en action
Ouvrez `config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py`

Décommentez la règle à l'intérieur et testez à nouveau. Ce qui se produit?

## Comprendre les règles

Les règles résident dans `config/maps/` dans les fichiers Python appelés `FUZZY_MAP_pre.py` ou `FUZZY_MAP.py`.

Une règle ressemble à ceci :
```python
('Hello World', r'\bhello world\b', 0, {'flags': re.IGNORECASE})
#   ^output        ^pattern          ^threshold  ^case-insensitive
```

La **sortie** vient en premier : vous voyez immédiatement ce que produit la règle.

Les règles sont traitées **de haut en bas**. Le premier fullmatch (`^...$`) arrête tout.

## Koans – Apprendre par la pratique

Les koans sont de petits exercices dans `config/maps/koans_deutsch/` et `config/maps/koans_english/`.

Chaque koan enseigne un concept :

| Koan | Sujet |
|---|---|
| 01_koan_erste_schritte | Première règle, correspondance complète, arrêt du pipeline |
| 02_koan_écouter | Listes, règles multiples |
| 03_koan_schwierige_namen | Noms difficiles, correspondance phonétique |

Commencez par Koan 01 et progressez.

## Conseils

- Les règles dans `FUZZY_MAP_pre.py` s'exécutent **avant** la vérification orthographique – idéales pour corriger les erreurs STT
- Les règles dans `FUZZY_MAP.py` s'exécutent **après** la vérification orthographique – bonnes pour le formatage
- Les fichiers de sauvegarde (`.peter_backup`) sont créés automatiquement avant toute modification
- Utilisez `peter.py` pour laisser une IA travailler automatiquement sur les koans