# Mise en cache avancée des résultats (sensible à l'état)

## Aperçu
Aura dispose d'un cache de résultats persistant et contextuel conçu pour éliminer les traitements redondants. Lorsqu'une commande vocale est reconnue et correspond à une règle, Aura vérifie si exactement le même résultat a été généré auparavant dans les mêmes circonstances. Si une correspondance est trouvée, Aura contourne les opérations coûteuses telles que les **vérifications grammaticales de LanguageTool** ou la **génération Ollama LLM**, fournissant le résultat avec une latence proche de zéro.

## Principales fonctionnalités
- **Context-Aware :** Le cache est spécifique au titre de la fenêtre active. Une commande dite dans « LibreOffice » peut avoir un résultat en cache différent de celui de la même commande dans « Terminal ».
- **Auto-réparation (auto-invalidation) :** Le cache expire automatiquement si vous modifiez le fichier de règles sous-jacent (carte `.py`).
- **La confidentialité d'abord :** Tous les résultats mis en cache sont stockés dans une base de données SQLite locale (`data/_aura_result_cache.db`).
- **Zéro maintenance :** Pour la plupart des utilisateurs, cela fonctionne entièrement en arrière-plan sans configuration.

## Comment ça marche
Le système génère un « cache_id » unique basé sur trois variables :
1. **La sortie de la règle :** Le texte généré par la carte.
2. **La langue :** Le code de langue actif actuel (par exemple, `de-DE`).
3. **La fenêtre active :** Le titre de la fenêtre actuellement active.

### Logique de validité
Le cache garantit que vous ne recevez jamais d'informations « périmées ». Il utilise deux types de contrôles de validité :

| Tapez | Nom | Logique | Cas d'utilisation |
| :--- | :--- | :--- | :--- |
| **Tapez 0** | **Synchronisation automatique des fichiers** | Utilise l'heure de modification (`mtime`) du fichier map. | **Standard.** Si vous modifiez votre bac à sable ou votre carte, toutes les entrées de cache associées sont instantanément invalidées. |
| **Type 1** | **Horodatage manuel** | Utilise un « horodatage » fixe fourni dans les attributs de la règle. | **Développeur.** Codez en dur une version/un horodatage pour forcer ou maintenir un état de résultat spécifique. |

## Exemples de configuration de règles

Vous pouvez contrôler le comportement de la mise en cache directement dans vos fichiers `FUZZY_MAP_pre.py` ou `FUZZY_MAP.py`.

### 1. Comportement par défaut (mise en cache automatique)
Par défaut, la mise en cache est activée et utilise l'heure de modification du fichier.
```python
# No extra attributes needed. 
# If this file is saved, the cache for this rule refreshes.
('Bold', r'^make it bold$', 100)
```

### 2. Désactivation du cache
Si une commande produit des données dynamiques (comme l'heure actuelle ou une blague aléatoire), vous devez désactiver le cache.
```python
('Current Time', r'^what time is it$', 100, {
    'cache': False 
})
```

### 3. Horodatage manuel (version fixe)
Si vous souhaitez que le cache persiste quelles que soient les modifications du fichier (sauf si vous modifiez la version), utilisez un horodatage manuel.
```python
('Stable Command', r'^run complex task$', 100, {
    'timestamp': '2026-05-09-v1'
})
```

## Impact sur les performances
- **Cache Miss :** Traitement standard (0,05 s - 5,0 s selon l'utilisation de LLM).
- **Cache Hit :** Traitement instantané.

Ce mécanisme permet aux commandes ou aux fautes de frappe corrigées d'être renvoyées instantanément sans solliciter le processeur.