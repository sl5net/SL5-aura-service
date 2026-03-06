# 🧠 Mode hybride SL5 Aura : intégration LLM locale

**Statut :** Expérimental / Stable
**Technologie :** Ollama (Llama 3.2) + sous-processus Python
**Confidentialité :** 100 % hors ligne

## Le Concept : "Architecte & Stagiaire"

Traditionnellement, Aura s'appuie sur des règles déterministes (RegEx) – rapides, précises et prévisibles. Voici le **"Architecte"**. Cependant, parfois l'utilisateur souhaite demander quelque chose de « flou » ou créatif, comme *« Raconte-moi une blague »* ou *« Résumez ce texte »*.

C'est là qu'intervient le **Local LLM Plugin** (le **"Stagiaire"**) :
1. **Aura (RegEx)** vérifie d'abord toutes les commandes strictes ("Allumer les lumières", "Ouvrir l'application").
2. Si rien ne correspond à **ET**/ **OU**, un mot déclencheur spécifique (par exemple, "Aura...") est détecté, la règle de secours s'active.
3. Le texte est envoyé à un modèle d'IA local (Ollama).
4. La réponse est nettoyée et émise via TTS ou saisie de texte.

---

## 🛠 Prérequis

Le plugin nécessite une instance en cours d'exécution de [Ollama](https://ollama.com/) fonctionnant localement sur la machine.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

---

## 📂 Structure et ordre de chargement

Le plugin est intentionnellement placé dans le dossier `z_fallback_llm`.
Étant donné qu'Aura charge les plugins **par ordre alphabétique**, cette dénomination garantit que la règle LLM est chargée **en dernier**. Il sert de « filet de sécurité » pour les commandes non reconnues.

**Chemin :** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. La carte (`FUZZY_MAP_pre.py`)

Nous utilisons un **score élevé (100)** et un mot déclencheur pour forcer Aura à céder le contrôle au script.

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + any text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'flags': re.IGNORECASE,
        # 'skip_list': ['LanguageTool'], # Optional: Performance boost
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

### 2. Le gestionnaire (`ask_ollama.py`)

Ce script communique avec la CLI Ollama.
**Important :** Il contient une fonction `clean_text_for_typing`. Les sorties brutes LLM contiennent souvent des emojis (😂, 🚀) ou des caractères spéciaux qui peuvent faire planter des outils comme « xdotool » ou des systèmes TTS existants.

```python
# Snippet from ask_ollama.py
def execute(match_data):
    # ... (Regex group extraction) ...
    
    # System prompt for short answers
    system_instruction = "Answer in German. Max 2 sentences. No emojis."
    
    # Subprocess call (blocks briefly, note the timeout!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # IMPORTANT: Sanitize output for system stability
    return clean_text_for_typing(result.stdout)
```

---

## ⚙️ Options de personnalisation

### Changer le déclencheur
Modifiez le RegEx dans `FUZZY_MAP_pre.py` si vous ne souhaitez pas utiliser "Aura" comme mot d'activation.
* Exemple pour un vrai Catch-All (tout ce qu'Aura ne sait pas) : `r'^(.*)$'` (Attention : Ajustez le score !)

### Échanger le modèle
Vous pouvez facilement échanger le modèle dans `ask_ollama.py` (par exemple, vers `mistral` pour une logique plus complexe, bien que cela nécessite plus de RAM).
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

### Invite système (Persona)
Vous pouvez donner à Aura une personnalité en ajustant le `system_instruction` :
> "Vous êtes un assistant sarcastique d'un film de science-fiction."

---

## ⚠️ Limites connues

1. **Latence :** La toute première requête après le démarrage peut prendre 1 à 3 secondes pendant le chargement du modèle dans la RAM. Les demandes ultérieures sont plus rapides.
2. **Conflits :** Si le RegEx est trop large (`.*`) sans une structure de dossiers appropriée, il peut avaler des commandes standard. L'ordre alphabétique (`z_...`) est essentiel.
3. **Matériel :** Nécessite env. 2 Go de RAM gratuite pour Llama 3.2.