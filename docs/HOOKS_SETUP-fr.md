# Configuration des hooks Git pré-Push et des outils Python sous Linux

Ce projet utilise un hook Git pré-push pour mettre à jour automatiquement « requirements.txt » à partir de vos scripts Python.
Pour utiliser ce workflow, vous devez avoir l'outil « pipreqs » installé et disponible sur Git.

## Recommandé : installez pipreqs avec pipx

1. **Installez pipx (s'il n'est pas déjà installé) :**
```bash
sudo pacman -S python-pipx
```

2. **Installez pipreqs à l'aide de pipx :**
```bash
pipx installer pipreqs
```

3. **Vérifiez que pipreqs fonctionne :**
```bash
pipreqs --version
```

## Alternative : utiliser un environnement virtuel Python

Si vous préférez ou utilisez un virtualenv pour votre projet :

1. **Créez et activez un virtualenv :**
```bash
python -m venv .venv
source .venv/bin/activer
```

2. **Installez pipreqs dans virtualenv :**
```bash
pip installer pipreqs
```

3. **Modifiez le git hook** pour appeler pipreqs en utilisant le chemin complet :
```bash
.venv/bin/pipreqs "$TMPDIR" --force
```

## Pourquoi ne pas utiliser l'installation simple de pip ?

Les distributions Linux modernes restreignent les installations pip à l'échelle du système pour éviter de casser les packages du système d'exploitation.
**N'utilisez PAS** d'utiliser `sudo pip install pipreqs` ou `pip install pipreqs` globalement.

## Dépannage

- Si vous voyez `pipreqs : command not found`, assurez-vous que vous l'avez installé avec pipx et que `~/.local/bin` est dans votre `$PATH`.
- Vous pouvez vérifier votre chemin avec :
```bash
écho $ CHEMIN
```

## Besoin d'aide ?

Ouvrez un problème ou posez-le dans la discussion du projet !
