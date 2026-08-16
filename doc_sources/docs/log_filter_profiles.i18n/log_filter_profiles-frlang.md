# Profils de filtre de journal

Le filtre de journal actif est toujours `config/filters/settings_local_log_filter.py`.

## Profils

Les profils prédéfinis sont stockés dans `config/filters/.backlock/` :

| Profil | Descriptif |
|---|---|
| `premier_run` | Sortie minimale – erreurs et état uniquement. Appliqué automatiquement au premier démarrage. |
| `normale` | Filtre standard pour un usage quotidien. |

## Changer de profil manuellement

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

## Ajouter un profil personnalisé

1. Créez un nouveau dossier sous `config/filters/.backlock/my_profile/`
2. Copiez-y un `settings_local_log_filter.py` existant et modifiez-le selon vos besoins
3. Appliquez-le avec `cp` comme indiqué ci-dessus

## Changement automatique de profil

Au premier démarrage, Aura détecte que le répertoire `log/` n'existe pas encore et
copie automatiquement le profil `first_run` comme filtre actif.