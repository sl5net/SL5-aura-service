# 🧠 Mode hybride SL5 Aura : intégration locale du LLM et du presse-papiers

**Statut :** Stable
**Technologie :** Ollama (Llama 3.2) + Architecture de pont de fichiers
**Confidentialité :** 100 % hors ligne

## Le Concept : "Architecte & Stagiaire"

Traditionnellement, Aura s'appuie sur des règles déterministes (RegEx) – rapides et précises. Voici le **"Architecte"**.
Le **Local LLM Plugin** fait office de **"Stagiaire"** : il gère les demandes floues, résume les textes et répond aux questions générales.

## 🛠 Architecture : Le Pont du Presse-papiers

En raison des restrictions de sécurité sous Linux (Wayland/X11), les processus en arrière-plan (comme Aura) ne peuvent souvent pas accéder directement au presse-papiers. Nous avons résolu ce problème avec une **architecture de pont** :

1. **Le fournisseur (session utilisateur) :** Un petit script shell (`clipboard_bridge.sh`) s'exécute dans la session de l'utilisateur. Il surveille le presse-papiers et reflète son contenu dans un fichier temporaire (`/tmp/aura_clipboard.txt`).
2. **Le consommateur (Aura) :** Le plugin Python lit ce fichier. L’accès aux fichiers étant universel, les problèmes d’autorisation sont contournés.

---

## 🚀 Guide de configuration

### 1. Installez Ollama
```bash
sudo pacman -S ollama xclip wl-clipboard
sudo systemctl enable --now ollama
ollama run llama3.2
```

### 2. Configurer le script Bridge
Créez `~/clipboard_bridge.sh` et rendez-le exécutable :

```bash
#!/bin/bash
# Mirrors clipboard to a file in RAM
FILE="/tmp/aura_clipboard.txt"
while true; do
    if command -v wl-paste &> /dev/null; then
        wl-paste --no-newline > "$FILE" 2>/dev/null
    else
        xclip -selection clipboard -o > "$FILE" 2>/dev/null
    fi
    sleep 1.5
done
```

**Important :** Ajoutez ce script au démarrage automatique de votre système !

### 3. Logique du plugin (`ask_ollama.py`)

Le script se trouve dans `config/maps/plugins/z_fallback_llm/de-DE/`.
* **Déclencheur :** Détecte des mots tels que « Ordinateur », « Aura », « Presse-papiers », « Résumé ».
* **Mémoire :** Conserve un `conversation_history.json` pour se souvenir du contexte (par exemple, "Qu'est-ce que je viens de demander ?").
* **Ingénierie rapide :** donne la priorité aux données actuelles du presse-papiers par rapport au contexte de conversation historique pour éviter les hallucinations.

---

## 📝 Exemples d'utilisation

1. **Résumer le texte :**
* *Action :* Copiez un long e-mail ou le texte d'un site Web (Ctrl+C).
* *Commande vocale :* "Ordinateur, résumez le texte dans le presse-papiers."

2. **Traduction/Analyse :**
* *Action :* Copiez un extrait de code.
* *Commande vocale :* « Ordinateur, que fait le code dans le presse-papiers ? »

3. **Discussion générale :**
* *Commande vocale :* "Ordinateur, raconte-moi une blague sur les programmeurs."

4. **Réinitialiser la mémoire :**
* *Commande vocale :* "Ordinateur, oublie tout." (Efface l'historique JSON).
  