## Objectif : Le modèle "Séance de dictée"

### Unser Ziel(allemand) : Die "Diktier-Sitzung"

Un seul déclencheur démarre une **"Diktier-Sitzung"**, la meilleure des trois phases :

1. **Phase de démarrage (Warten auf Sprache) :**
* Lorsque le déclencheur déclenche le système.
* Lorsque **keine** Spracheingabe erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT` (par exemple 12s).

2. **Phase active (Kontinuierliches Diktieren) :**
* Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in den aktiven Modus.
* Lorsque VOSK exécute une pause de lecture et un bloc de texte activé (par exemple, un bloc de texte), ce bloc **sofort** est utilisé pour l'utilisation (LanguageTool, etc.) et le texte est également généré.
* Die Aufnahme läuft währenddessen **nahtlos weiter**. Die Sitzung wartet auf den ächsten Satz.

3. **Phase finale (Ende der Sitzung) :**
* L'organisation de la situation se termine seulement lorsqu'un de ces éléments de lit est effectué :
* Le Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT` (par exemple 1-2s) complet encore.
* Der Nutzer stoppt die Sitzung manuell per Trigger.

**Zusammengefasst:** Eine Sitzung, viele sofortige Textausgaben. La position est bien active, jusqu'à ce que la noix ait une pause plus longue ou une pause manuelle.


### **Objectif : Le modèle « Séance de dictée »**

Un seul déclencheur lance une **"Session de dictée"**, qui se compose de trois phases :
1. **Phase de démarrage (en attente de parole) :**
* Après le déclenchement, le système commence à écouter.
* Si **aucune parole** n'est détectée, la session entière se termine après le `PRE_RECORDING_TIMEOUT` (par exemple, 12 s).
2. **Phase active (dictée continue) :**
* Dès que la première entrée vocale est détectée, la session passe en mode actif.
* Chaque fois que VOSK détecte une pause et délivre un morceau de texte (par exemple, une phrase), ce morceau est **immédiatement** transmis au pipeline de traitement (LanguageTool, etc.) et affiché sous forme de texte.
* L'enregistrement continue **de manière transparente** en arrière-plan, en attendant la prochaine parole.
3. **Phase de résiliation (fin de la session) :**
* La session entière se termine uniquement lorsque l'une des deux conditions suivantes est remplie :
* L'utilisateur reste complètement silencieux pendant la durée du `SPEECH_PAUSE_TIMEOUT` (par exemple, 1-2s).
* L'utilisateur arrête manuellement la session via le déclencheur.
**En bref :** Une session, plusieurs sorties de texte immédiates. La session reste active jusqu'à ce que l'utilisateur fasse une longue pause ou y mette fin manuellement.