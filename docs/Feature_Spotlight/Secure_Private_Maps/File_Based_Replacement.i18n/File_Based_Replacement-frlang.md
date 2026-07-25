# PLEINS FEUX SUR LES FONCTIONS : Remplacements de règles basées sur des fichiers

Ce document décrit comment conserver les valeurs sensibles (mots de passe, clés API, tokens)
à partir du code source de `FUZZY_MAP_pre` / `FUZZY_MAP` et de l'historique Git en chargeant le
Texte de « remplacement » à partir d'un fichier séparé au moment de l'exécution au lieu de le coder en dur.

Ceci est particulièrement utile lors des diffusions en direct ou des partages d'écran, où la carte
le code source lui-même peut être visible, mais le fichier référencé ne l'est pas.

---

## 1. Le concept

Normalement, le champ « remplacement » d'une règle est le texte de sortie littéral :

```python
('my-secret-value', r'^(trigger)$', 85, {'command_flags': re.IGNORECASE})
```

Avec le remplacement basé sur les fichiers activé, une valeur de « remplacement » commençant par un
le préfixe configuré (par défaut `-` ou `.`) est plutôt traité comme un **nom de fichier**.
Aura résout ce nom de fichier par rapport au propre répertoire du plugin, lit son
contenu et utilise ce contenu comme texte de remplacement.

```python
('-api_key.txt', r'^(show api key)$', 85, {'command_flags': re.IGNORECASE})
```

Si `api_key.txt` existe à côté de `FUZZY_MAP_pre.py` du plugin, son (supprimé)
le contenu est utilisé en remplacement. Si le fichier n'existe pas, le littéral
la chaîne `-api_key.txt` est renvoyée à la place (sécurité intégrée : aucune fuite accidentelle de
"fichier introuvable" comme texte utilisable, et pas de crash).

---

## 2. Paramètres

Configuré dans `config/settings.py` (ou `config/settings_local.py` pour les
remplacements) :

| Paramètre | Tapez | Par défaut | Descriptif |
|---|---|---|---|
| `FILE4REPLACEMENT_USE` | `bool` | `Vrai` | Interrupteur principal pour l'ensemble de la fonctionnalité. Si « False », « remplacement » est toujours utilisé littéralement. |
| `FILE4REPLACEMENT_ALLOWED_PREFIXES` | `tuple[str]` | `('-', '.')` | Les valeurs de « remplacement » doivent commencer par l'un de ces préfixes pour déclencher une recherche de fichier. Vide/`Aucun` = toute valeur ne commençant pas par une lettre est traitée comme un nom de fichier potentiel. |
| `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` | `bool` | 'Faux' | Si `True`, permet de résoudre les fichiers en dehors du propre répertoire du plugin (par exemple les chemins absolus ou les séquences `../`). Voir la section Sécurité ci-dessous. |
| `FILE4REPLACEMENT_DENY_PREFIXES` | `tuple[str]` | par ex. `('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Program Files')` | Les chemins absolus résolus commençant par l'un de ces éléments sont **toujours** rejetés, quel que soit `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL`. Limite de sécurité stricte contre les répertoires système. |

---

## 3. Résolution du chemin

Le dossier est résolu comme suit :

1. Le `source_path` du plugin (enregistré automatiquement par le chargeur de carte) est
joint à `PROJECT_ROOT` (lu depuis `SL5NET_AURA_PROJECT_ROOT`
variable d'environnement) pour obtenir le répertoire du plugin.
2. La valeur de « remplacement » est jointe à ce répertoire.
3. Sauf si `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` est `True`, le chemin résolu
doit rester dans le répertoire du plugin, sinon la recherche est rejetée.
4. Indépendamment de ce qui précède, tout chemin résolu commençant par une entrée dans
`FILE4REPLACEMENT_DENY_PREFIXES` est toujours rejeté.
5. Si le fichier existe, son contenu supprimé est renvoyé. Sinon, le
La chaîne de « remplacement » originale est renvoyée inchangée.

---

## 4. Notes de sécurité

- N'activez `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` que si vous comprenez le
implications : cela permet à tout utilisateur pouvant éditer un fichier `FUZZY_MAP_pre` (par ex.
via un éditeur de cartes en ligne) pour lire des fichiers arbitraires que le processus Aura peut
accéder et faire apparaître leur contenu sous forme de texte de sortie en direct.
- `FILE4REPLACEMENT_DENY_PREFIXES` fournit une protection de base contre
répertoires système communs même lorsque la traversée de chemin est autorisée, mais elle est
cela ne remplace pas la restriction des personnes autorisées à modifier les fichiers cartographiques en premier lieu.
- Les fichiers référencés sont du texte brut sur le disque. Combinez avec le fichier de votre système d'exploitation
autorisations si le contenu est sensible.

---

## 5. Exemple

Voir `config/maps/plugins/TEST_FILE4REPLACEMENT/` pour un exemple de plugin fonctionnel,
et `tools/tests/TEST_FILE4REPLACEMENT.sh` pour un script de test qui exerce
à la fois une recherche dans le répertoire et une recherche en dehors du répertoire du plugin.

```python
# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
FUZZY_MAP_pre = [
    ('.Zebra.txt', r'^(Zebra)$', 85, {'command_flags': re.IGNORECASE}),
]
```

Créez `.Zebra.txt` à côté de ce fichier avec le texte de remplacement souhaité, puis
dites (ou tapez via la console) « s Zebra » pour le déclencher.