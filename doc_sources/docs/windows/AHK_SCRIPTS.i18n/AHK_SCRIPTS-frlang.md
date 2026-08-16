### Documentation Markdown (`docs/AHK_SCRIPTS.md`)

# Infrastructure AutoHotkey pour le service SL5-Aura

Étant donné que Windows gère les verrous de fichiers et les raccourcis clavier système différemment de Linux, ce projet utilise un ensemble de scripts AutoHotkey (v2) pour combler le fossé entre le moteur Python STT et l'interface utilisateur Windows.

## Présentation des scripts

### 1. `trigger-hotkeys.ahk`
* **Objectif :** L'interface utilisateur principale pour contrôler le service.
* **Principales caractéristiques :**
* Intercepte **F10** et **F11** pour démarrer/arrêter la dictée.
* Utilise un « Keyboard Hook » pour remplacer le comportement par défaut du système Windows (par exemple, F10 activant la barre de menu).
* **Déploiement :** Conçu pour être enregistré via le planificateur de tâches Windows avec les « privilèges les plus élevés » afin de pouvoir capturer des raccourcis clavier même lorsque l'utilisateur travaille dans une application de niveau administrateur.

### 2. `type_watcher.ahk`
* **Objectif :** Agit en tant que « Consommateur » dans le pipeline STT.
* **Principales caractéristiques :**
* Surveille un répertoire temporaire pour les fichiers `.txt` entrants générés par le moteur Python.
* **State Machine (Zombie Map) :** Implémente une carte basée sur la mémoire pour garantir que chaque fichier est tapé exactement une fois. Cela évite la « double saisie » provoquée par des événements redondants du système de fichiers Windows (ajouté/modifié).
* **Saisie sécurisée :** Utilise `SendText` pour garantir que les caractères spéciaux sont gérés correctement dans n'importe quel éditeur actif.
* **Nettoyage fiable :** Gère la suppression de fichiers avec une logique de nouvelle tentative pour gérer les verrous d'accès aux fichiers Windows.

### 3. `scripts/ahk/sync_editor.ahk`
* **Objectif :** Assure une synchronisation transparente entre le disque et l'éditeur de texte (par exemple, Notepad++).
* **Principales caractéristiques :**
* **Sauvegarde à la demande :** Peut être déclenché par Python pour forcer un `Ctrl+S` dans l'éditeur avant que le moteur ne lise le fichier.
* **Dialog Automator :** Détecte et confirme automatiquement les boîtes de dialogue de rechargement « Fichier modifié par un autre programme », créant ainsi une expérience de mise à jour fluide en temps réel.
* **Commentaire visuel :** Fournit des boîtes de notification de courte durée pour informer l'utilisateur que des corrections sont appliquées.

### 4. `scripts/notification_watcher.ahk`
* **Objectif :** Fournit des commentaires sur l'interface utilisateur pour les processus en arrière-plan.
* **Principales caractéristiques :**
* Surveille les fichiers d'état ou les événements spécifiques pour afficher des notifications à l'utilisateur.
* Découple la logique de « calcul » d'un message (Python) de son « affichage » (AHK), garantissant que le moteur STT principal n'est pas bloqué par les interactions de l'interface utilisateur.


---

### Solution de secours non-administrateur
Si l'application est exécutée sans privilèges d'administrateur :
- **Fonctionnalité :** Le service reste entièrement fonctionnel.
- **Limites des raccourcis clavier :** Les touches réservées au système telles que **F10** peuvent toujours déclencher le menu Windows. Dans ce cas, il est recommandé de remplacer les raccourcis clavier par des touches non système (par exemple, « F9 » ou « Insérer »).
- **Planificateur de tâches :** Si la tâche "AuraDictation_Hotkeys" a été créée lors d'une installation administrateur, le script s'exécutera avec des privilèges élevés, même pour un utilisateur standard. Sinon, `start_dictation.bat` lancera silencieusement une instance locale au niveau de l'utilisateur.

---

### 3. La « fusion nerveuse » s'effectue et l'homme est dans l'arrêt du code AHK
Pour être sûr, le script n'a rien à voir avec les popups, et ces "Silent-Flags" apparaissent dans votre date `.ahk` dans un :

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force   ; Ersetzt alte Instanzen ohne zu fragen
#NoTrayIcon            ; (Optional) Wenn du kein Icon im Tray willst
ListLines(False)       ; Erhöht Performance und verbirgt Debug-Logs
```

### 4. Stratégie pour les raccourcis clavier (alternative F10)
Depuis F10 sans droit d'administrateur sous Windows, vous pouvez rapidement le supprimer, vous pouvez essayer d'utiliser `trigger-hotkeys.ahk` une fois:

```autohotkey
if !A_IsAdmin {
    ; Wenn kein Admin, warne den Entwickler im Log
    ; Log("Running without Admin - F10 might be unreliable")
}

; Nutze Wildcards, um die Chance zu erhöhen, dass es auch ohne Admin klappt
*$f10::
{
    ; ... Logik
}
```

### Prise en charge des procédures :
1. **Batch-Datei :** Nutzt `start "" /b`, um the schwarze Fenster zu vermeiden, et prüft voher, ob der Admin-Task schon läuft.
2. **Transparenz :** Die Doku erklärt nun offen: "Kein Admin? Kein Problem, nimm einfach eine andere Taste als F10".
3. **AHK-Skript :** Nutzt `#SingleInstance Force`, pour la boîte de dialogue "Une ancienne instance est en cours d'exécution".

Damit wirkt die Software viel professionaleller ("Smooth"), sie im Hintergrund startet, ohne dass der Nutzer mit technischen Details oder Bestätigungsfenstern wird wird.
  
  
---

### Pourquoi cette documentation est importante :
En documentant la **"Zombie Map"** et l'exigence **"Task Scheduler/Admin"**, vous expliquez aux autres développeurs (et à vous-même) pourquoi le code est plus complexe qu'un simple script Linux. Il transforme des « solutions de contournement étranges » en « solutions conçues pour les limitations de Windows ».

(s, 29.1.'26 11:02 jeu.)