# Premiers pas avec SL5 Aura

> **Prérequis :** Vous avez terminé le script de configuration et configuré votre raccourci clavier.
> Sinon, consultez le [Installation section in README.md](../../README.i18n/README-frlang.md#installation).

---

## Étape 0 : Configurez votre raccourci clavier

Choisissez votre plateforme :

**Linux/macOS** — Installez [CopyQ](https://github.com/hluk/CopyQ) et créez une commande avec un raccourci global :
```bash
touch /tmp/sl5_record.trigger
```

**Windows** — Utilisez [AutoHotkey v2](https://www.autohotkey.com/) ou CopyQ. Le script d'installation installe les deux automatiquement.
Le fichier de déclenchement est : `c:\tmp\sl5_record.trigger`

> Tous les détails : [README.md#configure-your-hotkey](../../README.i18n/README-frlang.md#configure-your-hotkey)

## Étape 1 : Votre première dictée

1. Démarrez Aura (s'il n'est pas déjà en cours d'exécution) :
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
Attendez le son de démarrage – cela signifie qu’Aura est prêt.

2. Cliquez dans n'importe quel champ de texte (éditeur, navigateur, terminal).
3. Appuyez sur votre touche de raccourci, dites **"Hello World"**, appuyez à nouveau sur la touche de raccourci.
4. Regardez le texte apparaître.

> **Rien ne s'est passé ?** Vérifiez `log/aura_engine.log` pour les erreurs.
> Correctif commun pour CachyOS/Arch : `sudo pacman -S mimalloc`

---

## Étape 2 : Écrivez votre première règle

Le moyen le plus rapide d’ajouter une règle personnelle :

1. Ouvrez `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Ajoutez une règle dans `FUZZY_MAP_pre = [...]` :
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **Enregistrer** — Aura se recharge automatiquement. Aucun redémarrage nécessaire.
4. Dictez « Hello World » et regardez-le devenir « Hello World ».

> Voir `docs/FuzzyMapRuleGuide.md` pour la référence complète des règles.

### L'Oma-Modus (raccourci pour débutant)

Vous ne connaissez pas encore les regex ? Aucun problème.

1. Ouvrez n'importe quel `FUZZY_MAP_pre.py` vide dans le bac à sable
2. Écrivez juste un mot simple sur sa propre ligne (pas de guillemets, pas de tuple) :
   ```
   raspberry
   ```
3. Enregistrer — le système Auto-Fix détecte le simple mot et automatiquement
le convertit en une entrée de règle valide.
4. Vous pouvez ensuite modifier manuellement le texte de remplacement.

C'est ce qu'on appelle **Oma-Modus** — conçu pour les utilisateurs qui souhaitent des résultats sans
apprendre d'abord les regex.

---

## Étape 3 : Apprendre avec les Koans

Les Koans sont de petits exercices qui enseignent chacun un concept.
Ils vivent dans `configmaps/koans deutsch/` et `configmaps/koans english/`.

Commencez ici :

| Dossier | Ce que vous apprenez |
|---|---|
| `00_koan_oma-modus` | Auto-Fix, première règle sans regex |
| `01_koan_erste_schritte` | Votre première règle, les bases du pipeline |
| `02_koan_écouter` | Travailler avec des listes |
| `03_koan_schwierige_namen` | Correspondance floue pour les noms difficiles à reconnaître |
| `04_koan_kleine_helfer` | Raccourcis utiles |

Chaque dossier koan contient un `FUZZY_MAP_pre.py` avec des exemples commentés.
Décommentez une règle, enregistrez, dictez la phrase déclencheur – c'est fait.

---

## Étape 4 : Aller plus loin

| Quoi | Où |
|---|---|
| Référence complète des règles | `docs/FuzzyMapRuleGuide.md` |
| Créez votre propre plugin | `docs/CreatingNewPluginModules.md` |
| Exécuter des scripts Python à partir de règles | `docs/advanced-scripting.md` |
| DEV_MODE + configuration du filtre de journal | `docs/Developer_Guide/dev_mode_setup.md` |
| Règles contextuelles (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |