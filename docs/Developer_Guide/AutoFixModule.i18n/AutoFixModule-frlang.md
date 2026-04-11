# Module de réparation automatique (mode de saisie rapide des règles)

## Ce que ça fait

Lorsque vous tapez un mot simple (sans guillemets ni syntaxe Python) dans un fichier map
comme `FUZZY_MAP_pre.py`, le système le convertit automatiquement en une règle valide.

C'est le moyen le plus rapide de créer de nouvelles règles : vous n'avez pas besoin de vous souvenir du format.

## Exemple

Vous tapez ceci dans `FUZZY_MAP_pre.py` :

```
oma
```

Le module de correction automatique détecte une `NameError` (mot nu, Python non valide)
et transforme automatiquement le fichier en :

```python
# config/maps/.../de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', 'oma'),
]
```

Modifiez maintenant la règle selon ce dont vous avez réellement besoin :

```python
('Oma', 'oma'),              # capitalize
('Großmutter', 'oma'),       # synonym
('Thomas Müller', 'thomas'), # from a phone book
```

## Comment ça marche

Le module `scripts/py/func/auto_fix_module.py` se déclenche automatiquement
lorsqu'Aura détecte une `NameError` lors du chargement d'un fichier de carte.

Il alors :
1. Ajoute l'en-tête de chemin de fichier correct
2. Ajoute `import re` s'il est manquant
3. Ajoute la définition de liste `FUZZY_MAP_pre = [`
4. Convertit les mots nus en tuples `('word', 'word'),`
5. Ferme la liste avec `]`

## Règles et limites

- Fonctionne uniquement sur les fichiers inférieurs à **1 Ko** (limite de sécurité)
- S'applique uniquement à : `FUZZY_MAP.py`, `FUZZY_MAP_pre.py`, `PUNCTUATION_MAP.py`
- Le fichier doit être dans un dossier de langue valide (par exemple `de-DE/`)
- Fonctionne pour plusieurs mots à la fois (par exemple à partir d'une liste d'annuaire téléphonique)

## Problèmes connus (pas entièrement testés)

> ⚠️ Ce module est fonctionnel mais testé de manière non exhaustive. Les cas suivants peuvent ne pas fonctionner correctement :

- **Nombres** – `5` ou `6` ne sont pas des identifiants Python valides, la correction automatique peut ne pas les gérer
- **Caractères spéciaux** – les mots avec `-`, `.`, les trémas ne peuvent pas déclencher une `NameError`
- **Entrées multi-mots** – `thomas mueller` (avec espace) provoque `SyntaxError` et non `NameError`, donc la correction automatique peut ne pas se déclencher
- **Valeurs séparées par des virgules** – `drei, vier` peut être inséré tel quel sans devenir un tuple approprié

Si la correction automatique ne se déclenche pas, ajoutez la règle manuellement :
```python
('replacement', 'input word'),
```

## Le commentaire `# aussi<-from`

Ce commentaire est ajouté automatiquement pour rappeler le sens de la règle :

```
too <- from
```

Signification : **sortie** (aussi) ← **entrée** (depuis). Le remplacement vient en premier.

Pour `PUNCTUATION_MAP.py`, le sens est inversé : `# from->too`

## Entrée groupée à partir d'une liste

Vous pouvez coller plusieurs mots à la fois :

```
thomas
maria
berlin
```

Chaque simple mot devient sa propre règle :

```python
('thomas', 'thomas'),
('maria', 'maria'),
('berlin', 'berlin'),
```

Modifiez ensuite chaque remplacement selon vos besoins.

## Fichier : `scripts/py/func/auto_fix_module.py`