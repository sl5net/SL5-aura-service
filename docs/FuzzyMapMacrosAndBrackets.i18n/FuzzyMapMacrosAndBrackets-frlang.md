# Macros de carte floue et logique de support

Aura prend en charge le regroupement de plusieurs règles de prétraitement dans des fichiers « FUZZY_MAP_pre.py » pour les exécuter séquentiellement en tant que pipeline cohérent une fois qu'une « règle de démarrage » est déclenchée. Ce document décrit la philosophie de conception, la syntaxe et le flux d'exécution de cette fonctionnalité.

## Principes de conception de base

1. **Zéro redondance** : les règles à l'intérieur d'un groupe restent des tuples Python standard :
`('replacement_text', r'regex_pattern', seuil, flags_and_options)`
2. **Double utilisation** : les règles individuelles au sein d'un groupe sont des règles autonomes entièrement fonctionnelles. Si le groupe n'est pas déclenché, ils sont évalués normalement dans la boucle parent.
3. **Marqueur de fin passif** : La fin d'un groupe est définie par une entrée de règle passive qui ne correspond jamais seule. Il agit uniquement comme une limite pour l’analyseur.
4. **Repli hybride (Append-on-Non-Match)** : lorsqu'un groupe est actif, chaque règle interne doit contribuer à la sortie. Si l'expression régulière d'une règle interne correspond au texte, la substitution normale a lieu. S'il ne correspond pas, son texte de remplacement est ajouté au texte actuel avec un espace.

---

## Syntaxe et structure

Un groupe de macros est défini en encapsulant une série de règles standard entre une **Règle de début** et une **Règle de fin** dans `FUZZY_MAP_pre.py`.

### 1. La règle de départ
La règle de démarrage est une règle standard qui déclenche la macro lorsqu'elle correspond. Il inclut une clé ``group_start'` dans son dictionnaire d'options :
```python
('replacement', r'start_pattern', 100, {'group_start': 'unique_group_name'})
```

### 2. Règles intérieures
Les règles internes sont des règles standard placées séquentiellement après la règle de départ. Ils ne nécessitent aucune métadonnée particulière :
```python
('inner_replacement', r'inner_pattern', 100, {})
```

### 3. La règle de fin (marqueur passif)
La règle de fin a un remplacement « None », un modèle vide et une clé « group_end » dans son dictionnaire d'options :
```python
(None, r'', 100, {'group_end': 'unique_group_name'})
```

---

## Exemple concret

Voici un cas de test pratique défini dans un fichier `FUZZY_MAP_pre.py` :

```python
FUZZY_MAP_pre = [
    # Start Rule: Triggers the group 'sandbox_test' when "start sandbox" matches
    ('Sandbox:', r'start\w* sandbox', 100, {'group_start': 'sandbox_test'}),
    
    # Inner Rule 1: Replaces "apfel" with "birne" if present
    ('birne', r'apfel', 100, {}),
    
    # Inner Rule 2: Replaces "banane" if present, otherwise appends "banane"
    ('banane', r'banane', 100, {}),
    
    # End Rule: Passive boundary marker
    (None, r'', 100, {'group_end': 'sandbox_test'}),
]
```

### Scénarios de flux d'exécution :

* **Scénario A (Macro déclenchée)** :
* Entrée : `"démarrer le bac à sable avec apfel"`
* Débit attendu :
1. La règle de démarrage correspond à `"start sandbox"` et la remplace par `"Sandbox:"` -> texte actuel : `"Sandbox: mit apfel"`.
2. Le groupe ``sandbox_test'` est déclenché.
3. Nous exécutons les règles internes de manière récursive sur `"Sandbox: mit apfel"` :
- La règle interne 1 correspond à `"apfel"` et remplace par `"birne"` -> texte actuel : `"Sandbox: mit birne"`.
- La règle interne 2 ne correspond pas à `"banane"`. Puisque le groupe est actif, il revient à ajouter `"banane"` -> Texte actuel : `"Sandbox: mit birne banane"`.
4. Le texte final `"Sandbox: mit birne banane"` est renvoyé et corrigé par LanguageTool.
* Sortie : `"Bac à sable : avec Birne Banane"`

* **Scénario B (Macro non déclenchée - Double utilisation)** :
* Entrée : `"un apfel et un kirsche"`
* Débit attendu :
1. La règle de départ ne correspond pas. Le groupe ``sandbox_test'` reste inactif.
2. La boucle passe à la règle suivante.
3. **Règle intérieure 1** : correspond à `"apfel"` et le remplace par `"birne"` -> Texte actuel : `"ein birne und eine kirsche"`.
4. **Règle intérieure 2** : Ne correspond pas. Étant donné que le groupe n'a pas été déclenché, la règle se comporte comme une règle autonome normale et **rien n'est ajouté**.
5. La règle de fin est ignorée.
* Sortie : `"un birne et un kirsche"`

---

## Détails techniques (sous le capot)

* **Récursion isolée** : lorsqu'un groupe est déclenché, le moteur appelle de manière récursive `process_text_in_background` avec `custom_rules=[inner_rule]`. Cela permet à chaque règle interne de s’exécuter dans le cadre d’une passe de pipeline complète et synchrone.
* **Garanties de performance et de stabilité** :
* **Sequence Bypass** : les exécutions récursives internes contournent la file d'attente de séquence `chunk_id` pour éviter les blocages et les retards d'exécution.
* **Suppression des E/S et TTS** : les exécutions récursives suppriment l'écriture de fichiers intermédiaire et les sorties vocales TTS, garantissant que seul le texte final stabilisé est écrit et prononcé.
* **Garantie de stabilité** : les exécutions récursives s'interrompent strictement après une itération pour éviter des boucles de stabilité infinies lors des ajouts de repli.
* **Terminaison sécurisée** : le contrôle de stabilité repose strictement sur le nombre maximal d'itérations (`MAX_ITERATIONS_FOR_SAFETY`) pour empêcher les boucles infinies, en contournant la limitation basée sur le temps qui pourrait interrompre prématurément les exécutions de macros légitimes et plus lentes.
__CODE_BLOCK_4__