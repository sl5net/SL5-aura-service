# Outils de maintenance de carte Regex

Pour prendre en charge la fonctionnalité de recherche rapide (commande `s` / `search_rules.sh`), nous utilisons un script d'assistance qui annote automatiquement les modèles d'expression régulière avec des exemples lisibles par l'homme.

## Pourquoi avons-nous besoin de ça ?
Nos fichiers `FUZZY_MAP.py` contiennent des expressions régulières complexes. Pour les rendre consultables via des chercheurs flous (fzf) sans avoir besoin de comprendre l'expression régulière brute, nous ajoutons des commentaires `# EXAMPLE :` au-dessus des modèles.

**Avant:**
```python
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

**Après (généré automatiquement) :**
```python
# EXAMPLE: 1234-5678-9012-3456
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

## Le script Tagger (`map_tagger.py`)

Nous fournissons un script Python qui analyse tous les fichiers `FUZZY_MAP.py` et `FUZZY_MAP_pre.py` et génère automatiquement ces exemples.

###Installation
Le script nécessite la bibliothèque « exrex » pour générer des correspondances aléatoires pour les expressions régulières complexes.

```bash
pip install exrex
```

### Utilisation
Exécutez le script depuis la racine du projet :

```bash
python3 tools/map_tagger.py
```

### Flux de travail
1. **Créez ou modifiez** un fichier de carte (par exemple, en ajoutant de nouvelles règles).
2. **Exécutez** le script Tagger.
3. **Mode interactif :**
- Le script vous montrera une suggestion générée.
- Appuyez sur `ENTER` pour l'accepter.
- Tapez « s » pour ignorer.
- Tapez « sa » (ignorer tout) si vous souhaitez ignorer tous les modèles restants dont la génération échoue.
4. **Validez** les modifications.

> **Remarque :** Le script ignore les balises `# EXAMPLE :` existantes, il peut donc être exécuté à plusieurs reprises en toute sécurité.