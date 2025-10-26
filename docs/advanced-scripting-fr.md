# Actions de règles avancées : exécution de scripts Python

Ce document décrit comment étendre les fonctionnalités des règles simples de remplacement de texte en exécutant des scripts Python personnalisés. Cette fonctionnalité puissante vous permet de créer des réponses dynamiques, d'interagir avec des fichiers, d'appeler des API externes et de mettre en œuvre une logique complexe directement dans votre flux de travail de reconnaissance vocale.

## Le concept de base : `on_match_exec`

Au lieu de simplement remplacer du texte, vous pouvez désormais demander à une règle d'exécuter un ou plusieurs scripts Python lorsque son modèle correspond. Cela se fait en ajoutant une clé `on_match_exec` au dictionnaire d'options de la règle.

La tâche principale du script consiste à recevoir des informations sur la correspondance, à effectuer une action et à renvoyer une chaîne finale qui sera utilisée comme nouveau texte.

### Structure des règles

Une règle avec une action de script ressemble à ceci :

```python
# In your map file (e.g., config/maps/.../de-DE/my_rules.py)
from pathlib import Path

# It's best practice to define the directory path once at the top
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    (
        None,  # The replacement string is often None, as the script generates the final text.
        r'what time is it', # The regex pattern to match.
        95, # The confidence threshold.
        {
            'flags': re.IGNORECASE,
            # The new key: a list of script files to execute.
            'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
        }
    ),
]
```
**Points clés :**
- La valeur `on_match_exec` doit être une **list**.
- Les scripts se trouvent dans le même répertoire que le fichier map, c'est pourquoi `CONFIG_DIR / 'script_name.py'` est la manière recommandée pour définir le chemin.

---

## Création d'un script exécutable

Pour que le système utilise votre script, il doit suivre deux règles simples :
1. Il doit s'agir d'un fichier Python valide (par exemple, `my_script.py`).
2. Il doit contenir une fonction nommée `execute(match_data)`.

### La fonction `execute(match_data)`

Il s'agit du point d'entrée standard pour tous les scripts exécutables. Le système appellera automatiquement cette fonction lorsque la règle correspond.

- **`match_data` (dict) :** Un dictionnaire contenant tout le contexte de la correspondance.
- **Valeur de retour (str) :** La fonction **doit** renvoyer une chaîne. Cette chaîne deviendra le nouveau texte traité.

### Le dictionnaire `match_data`

Ce dictionnaire constitue le pont entre l'application principale et votre script. Il contient les clés suivantes :

* ``original_text'` (str) : La chaîne de texte intégral *avant* que tout remplacement de la règle actuelle soit appliqué.
* ``text_after_replacement'` (str) : Le texte *après* la chaîne de remplacement de base de la règle a été appliqué, mais *avant* que votre script soit appelé. (Si le remplacement est « Aucun », ce sera la même chose que « original_text »).
* ``regex_match_obj'` (re.Match) : L'objet officiel de correspondance d'expression régulière Python. Ceci est extrêmement puissant pour accéder aux **groupes de capture**. Vous pouvez utiliser `match_obj.group(1)`, `match_obj.group(2)`, etc.
* `'rule_options'` (dict) : Le dictionnaire complet d'options pour la règle qui a déclenché le script.

---

## Exemples

### Exemple 1 : Obtenir l'heure actuelle (réponse dynamique)

Ce script renvoie un message d'accueil personnalisé en fonction de l'heure de la journée.

**1. La règle (dans votre fichier carte) :**
```python
(None, r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

**2. Le script (`get_current_time.py`) :**
```python
from datetime import datetime
import random

def execute(match_data):
    """Returns a friendly, time-aware response."""
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime('%H:%M')

    if hour < 12:
        greeting = "Good morning!"
    elif hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    responses = [
        f"{greeting} It's currently {time_str}.",
        f"Right now, the time is {time_str}. Hope you're having a great day!",
    ]
    return random.choice(responses)
```
**Usage:**
> **Entrée :** "quelle heure est-il"
> **Sortie :** "Bon après-midi ! Il est actuellement 14h30."

### Exemple 2 : Calculatrice simple (utilisant des groupes de capture)

Ce script utilise des groupes de capture de l'expression régulière pour effectuer un calcul.

**1. La règle (dans votre fichier carte) :**
```python
(None, r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```

**2. Le script (`calculator.py`) :**
```python
def execute(match_data):
    """Performs a simple calculation based on regex capture groups."""
    try:
        match_obj = match_data['regex_match_obj']
        
        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        else:
            return "I didn't understand that operator."
            
        return f"The result is {result}."
    except (ValueError, IndexError):
        return "I couldn't understand the numbers in your request."
```
**Usage:**
> **Saisie :** "calculer 55 plus 10"
> **Sortie :** "Le résultat est 65."

### Exemple 3 : Liste d'achats persistante (E/S de fichier)

Cet exemple montre comment un script peut gérer plusieurs commandes (ajout, affichage) en inspectant le texte original de l'utilisateur, et comment il peut conserver les données en écrivant dans un fichier.

**1. Les règles (dans votre fichier carte) :**
```python
# Rule for adding items
(None, r'add (.*) to the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),

# Rule for showing the list
(None, r'show the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),
```

**2. Le script (`shopping_list.py`) :**
```python
from pathlib import Path

LIST_FILE = Path(__file__).parent / "shopping_list.txt"

def execute(match_data):
    """Manages a shopping list stored in a text file."""
    original_text = match_data['original_text'].lower()
    
    # --- Add Item Command ---
    if "add" in original_text:
        item = match_data['regex_match_obj'].group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")
        return f"Okay, I've added '{item}' to the shopping list."
    
    # --- Show List Command ---
    elif "show" in original_text:
        if not LIST_FILE.exists() or LIST_FILE.stat().st_size == 0:
            return "The shopping list is empty."
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.read().strip().splitlines()
        
        item_str = ", ".join(items)
        return f"On the list you have: {item_str}."
        
    return "I'm not sure what to do with the shopping list."
```
**Usage:**
> **Entrée 1 :** "ajouter du lait à la liste de courses"
> **Sortie 1 :** "D'accord, j'ai ajouté le "lait" à la liste de courses."
>
> **Entrée 2 :** "afficher la liste de courses"
> **Sortie 2 :** "Sur la liste vous avez : du lait."

---

## meilleures pratiques

- **Un travail par script :** Gardez les scripts concentrés sur une seule tâche (par exemple, `calculator.py` calcule uniquement).
- **Gestion des erreurs :** Enveloppez toujours la logique de votre script dans un bloc `try...sauf` pour l'empêcher de planter l'ensemble de l'application. Renvoie un message d'erreur convivial à partir du bloc `sauf`.
- **Bibliothèques externes :** Vous pouvez utiliser des bibliothèques externes (comme `requests` ou `wikipedia-api`), mais vous devez vous assurer qu'elles sont installées dans votre environnement Python (`pip install <library-name>`).
- **Sécurité :** Sachez que cette fonctionnalité peut exécuter n'importe quel code Python. Utilisez uniquement des scripts provenant de sources fiables.