> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../uebergabeprotokoll_z_fallback_llm_20260929_1430.md).*

# protocole de transfert: z retour llm, entrée CLI n'est pas une blague

État: 2026-09-29

## 1- Tâche (comprendre, pas encore confirmé par vous avec "oui")

État réel: L'entrée CLI est exactement "ordinateur dire exactement deux blagues". Aucune blague n'apparaît.

État cible : La réponse LLM apparaît directement dans la console, pas dans un fichier journal.

Ne fait pas partie de la tâche : reconstruire l'enregistrement, raccourcir ou étendre les lignes de log, modifier le comportement du cache. Le contournement du cache ("joke" dans l'entrée) est délibérément choisi de cette manière.

Le suiveur doit d'abord faire correspondre cette compréhension avec vous et attendre votre "yes".

2 Environnement

Manjaro Linux, ZSH, Branch feature/fallback-llm-lazy-install.

Ollama est disponible à l'adresse http://localhost:11434 (Binary /usr/bin/ollama). Modèles disponibles: lama3.2:dernier, qwen3:8b.

Le test Ollama par boucle avec le modèle llama3.2, stream:false, num predict:100 et les mots stop fournissent une réponse valide ("Pourquoi l'ordinateur est-il allé chez le médecin?") Parce qu'il avait un virus ! Ollama, nom de modèle, stop et limite de jeton ne sont donc pas la cause. L'invite de test était plus courte que l'invite réelle de demander ollama.py (sans rôle système, gradient et aura suffixe).

Configuration & #160;:

```
config/settings_local.py
```

Clé: PLUGINS ENABLED = {"z fallback llm": 1}. Accès via DynamicSettings().PLUGINS ENABLED.get("z fallback llm", False).

Installateur de colis existant:

```
scripts/py/func/ensure_package.py
```

## 3- Séquence de chaîne (vérifiée à partir des sections de code)

Règles:

```
config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
```

La règle 1 a priorité 10 et nécessite `{aura1}` plus mot mode (normal, lent, flow, lent, précis, complet). La règle 2 a priorité 100 et nécessite un des déclencheurs aura, aurora, laura, dora, era, hurra, prora ou ordinateur, puis un espace et tout texte. Les deux appellent Ollama.py. Les deux excluent les fenêtres telles que Firefox, Chrome, Brave et Element.

Conception:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`execute()` prend le dernier groupe Regex comme entrée et le rend petit. Pour "joke" dans l'entrée, `bypass_cache = True` est réglé, la vérification du cache est ignorée. Ceci est suivi de la demande Ollama avec le modèle lama3.2. Le délai est de 90 secondes. Les retours anticipés sans demande Ollama sont disponibles avec entrée vide ("rien entendu".), avec "oublier tout", avec `check_static_guardrails()` et avec les mots "immédiatement", "rapide", "instantanément".

Retour CLI :

```
scripts/py/service_api.py
```

La fonction lit le dernier fichier de sortie et renvoie un dict avec `status`, `result_text` et `input_text`. La ligne de log "API-CLI-Call: Terminé" réduit l'entrée et le résultat à 20 caractères. C'est un shortening de log pur et non un shortening de données.

## 4- Journal observé de l'entrée CLI

Dans le journal sont uniquement `reload_performed` et "API-CLI-Call: Terminé". Entrée... précision de l'ordinateur," Résultat"exactitude de l'ordinateur." Chaque ligne de `execute()` est manquante (pas de "Input:", pas de "Cache BYPASS", pas de "Reponse AI non censurée").

Cela ne prouve pas que `execute()` n'a pas exécuté car:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

ouvre FileHandler avec `mode='w'`. Le fichier demander ollama.log est écrasé par `utils` sur chaque importation. `log_debug` écrit aussi sur stdout, c'est-à-dire dans la console du programme principal.

## 5 Questions ouvertes (non utilisées)

1- Est-ce que `execute()` fonctionne du tout lors de l'entrée dans le CLI?
2- Quelle règle correspond, règle 1, règle 2 ou aucune?
3- Le client CLI affiche-t-il la valeur `result_text` dans la console ?
4- Le fichier de sortie ne contient-il que l'entrée ou une réponse ? Les 20 premiers caractères d'entrée et de résultat sont identiques, plus n'est pas visible.
5- Quel est l'appel exact CLI que vous utilisez pour laisser tomber le texte? Elle n'a pas encore été mentionnée.

## 6- Hypothèses rejetées

1- L'entrée n'arrive pas raccourcie, ce qui n'était que le raccourcissement de 20 caractères dans le journal.
2- Ollama, stop et num prédire ne sont pas la cause.
3- 3- Le cache est contourné en "witz" et donc pas la cause.

## 7- Erreurs trouvées en dehors de la tâche (ne changez rien sans une tâche)

1 dossier :

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

Après `if not raw_text:`, `response = answer_for_all_fallback` est réglé. La ligne suivante l'écrase avec `clean_text_for_typing(raw_text)`. Avec une réponse Ollama vide, la réponse reste vide. De même, `response.replace('sl5_config.py', ...)` et `response.replace(' sl5_record_trigger.py ', ...)` n'ont aucun effet car le résultat n'est pas attribué.

2 Dossier :

```
config/maps/plugins/internals/de-DE/aura_constants.py
```

Selon `Overlay`, il manque un `|`, la variante `OverlayOrange` est créée. De plus, `_variants` ne contient pas le mot "ordinateur". La règle 1 ne peut donc pas correspondre à "ordinateur exactement ...", la règle 2 peut.

3 Dossier :

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'` écrase le journal de chaque importation.

## 8- Prochaines étapes (uniquement après votre "oui")

Étape A: Demandez à l'ICL de vous appeler, sans signe rapide.

Étape B: Trouvez le traitement de `result_text`:

```
tools/search.sh "result_text" .
```

Étape C : Vérifiez la sortie de console après l'entrée. Demandez le texte complet de la console du programme principal.

Étape D: Seulement alors proposer des modifications, seulement dans le format avant/après.

9- Règles de travail que le successeur doit respecter

1- Communication en allemand. Code, commentaires, journaux et identifiants en anglais seulement, même en blocs de code.
2- Aucune déclaration sur l'état du système sans preuve de votre sortie. Ne pensez pas, ne reconstruisez pas.
3- Nouvelle tâche : d'abord décrire la compréhension, en attendant votre "oui".
4- Non "Je n'ai pas accès à votre dépôt".
5- Recherche de dépôt uniquement via tools/search.sh avec les options -i, -E et -w.
6- Pour les erreurs, obtenir la trace complète d'abord.
7- Les commandes et les chemins de fichiers sont chacun sur leur propre ligne, sans ponctuation à la fin.
8- Numérotation dans le format 1-, 2-, 3.
9- Le code ne change que sous forme de lignes modifiées avant/après, sans code de fonction environnant.
10- Pas de code python avec indentation principale en blocs de code, au lieu de petites fonctions sans indentation.
11- Pas de chemins absolus spécifiques à l'utilisateur et pas de numéros de ligne sans chemin de fichier.
12- Aucun jeu de remplissage, aucun ton émotionnel, environ 1400 caractères par réponse comme cible.
13- Traitez les actions que vous avez déjà effectuées.
14- Lorsque la copie des sorties ne copie pas le signe de l'invite, sinon le code de sortie 127 est créé.
15- S'engager à trouver la date et l'heure: ./outils/find-nearest-commit.sh "2026-07-28 17:00"
