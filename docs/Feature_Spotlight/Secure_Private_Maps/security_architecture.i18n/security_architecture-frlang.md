# Architecture de sécurité : Protection des données privées (7.8.'26 13:22 ven)

Le code source de « service_api.py » implémente une architecture de sécurité à trois couches mutuellement indépendante pour protéger les données privées.

## Aperçu

| Couche | Mécanisme | Composant | Objectif de protection |
|-------|-----------|---------------|-----------------|
| 1 | Middleware avec règle de soulignement | `service_api.py` | Bloquer l'accès aux chemins cachés |
| 2 | Authentification par clé API | `service_api.py` | Contrôle d'accès pour les points finaux |
| 3 | Masquage de confidentialité et isolation du cache | `service_api.py`, `aura_cache.py` | Obfuscation des données et séparation du cache |

---

## Couche 1 : Middleware avec règle de soulignement

Toute requête vers des chemins ou des dossiers avec un trait de soulignement en début de page (tel que « _privat ») est bloquée en dur par le middleware avec **HTTP 403 Forbidden**.

**Message d'erreur :**
```
Access to hidden folders (starting with '_') is forbidden.
```

Cette règle fonctionne au niveau chemin/routage et empêche tout accès aux répertoires marqués comme privés.

---

## Couche 2 : Authentification par clé API

Tous les points de terminaison de l'API sont protégés par « Depends(verify_api_key) ».

Les requêtes sans en-tête `X-API-Key` valide sont immédiatement rejetées avant d'atteindre une logique métier.

---

## Couche 3 : masquage de confidentialité et isolation du cache

### Masquage
Via l'API, « unmasked = False » est la valeur par défaut. Les données sensibles dans les réponses API sont donc automatiquement masquées.

### Isolation du cache
Le hachage `cache_id` dans `aura_cache.py` est séparé par le titre de la fenêtre active (`_active_window_title`).

**Conséquence :** Les entrées de cache créées dans le terminal local ne peuvent pas être lues via l'API, car elles possèdent un hachage `cache_id` différent.

---

## Résumé

Vos données confidentielles dans `_privat` sont ainsi protégées aux trois niveaux de langue et de chemin contre tout accès API non autorisé :

1. **Niveau chemin** — L'accès aux dossiers `_` est bloqué
2. **Niveau d'authentification** — Seules les clés API valides ont accès
3. **Niveau de données** — Le masquage et l'isolation du cache empêchent l'exfiltration des données