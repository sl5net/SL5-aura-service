# Mathématiciens célèbres – Guide de correction STT

## Le problème

Les systèmes de reconnaissance vocale (STT) comme Vosk entendent souvent mal ou mal épellent les noms de mathématiciens célèbres.
Ceci est particulièrement courant avec les noms allemands contenant des caractères spéciaux (ß, ü, ä, ö)
ou des noms empruntés à d'autres langues.

## Erreurs STT courantes

| Sortie parlée/STT | Orthographe correcte | Remarques |
|---|---|---|
| gauss, gauss | Gauss | Mathématicien allemand, ß souvent porté disparu |
| huileur, huileur | Euler | Suisse, le nom ressemble à « huileur » en allemand |
| leibnitz, lipnitz | Leibniz | z à la fin, faute d'orthographe courante |
| riman, riemann | Riemann | double-n souvent manqué |
| Hilbert | Hilbert | généralement correct, juste des majuscules |
| chantre | Chantre | généralement correct, juste des majuscules |
| poincaré, poincaré | Poincaré | accent manque souvent |
| noether, nôter | Noéther | tréma souvent manqué |

## Exemples de règles

```python
FUZZY_MAP_pre = [
    ('Gauß', r'\bgau[sß]{1,2}\b', 0, {'flags': re.IGNORECASE}),
    ('Euler', r'\b(oiler|oyler|euler)\b', 0, {'flags': re.IGNORECASE}),
    ('Leibniz', r'\bleib(nitz|niz|nits)\b', 0, {'flags': re.IGNORECASE}),
    ('Riemann', r'\bri{1,2}e?mann?\b', 0, {'flags': re.IGNORECASE}),
    ('Noether', r'\bn[oö]e?th?er\b', 0, {'flags': re.IGNORECASE}),
]
```

## Pourquoi Pre-LanguageTool ?

Ces corrections devraient avoir lieu dans `FUZZY_MAP_pre.py` (avant LanguageTool),
parce que LanguageTool pourrait "corriger" un nom mal orthographié en un autre mauvais mot.
Mieux vaut d'abord le corriger, puis laisser LanguageTool vérifier la grammaire.

## Tests

Après avoir ajouté une règle, testez avec la console Aura :
```
s euler hat die formel e hoch i pi plus eins gleich null bewiesen
```
Attendu : `Euler hat die Formel e hoch i pi plus eins gleich null bewiesen`