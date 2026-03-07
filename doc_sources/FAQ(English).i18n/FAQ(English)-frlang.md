### FAQ (anglais) 3.8.'2025 Sun

**1. Q : Qu'est-ce que SL5 Aura ?**
R : Il s'agit d'un programme de synthèse vocale hors ligne à l'échelle du système. Il vous permet de dicter dans n'importe quelle application de votre ordinateur (Windows, macOS, Linux) sans avoir besoin d'une connexion Internet.

**2. Q : Pourquoi devrais-je l’utiliser ? Qu'est-ce qui le rend spécial ?**
R : **Confidentialité.** Vos données vocales sont traitées à 100 % sur votre ordinateur local et ne sont jamais envoyées vers le cloud. Cela le rend entièrement privé et conforme au RGPD.

**3. Q : Est-ce gratuit ?**
R : Oui, l'édition communautaire est entièrement gratuite et open source. Vous pouvez trouver le code et l'installateur sur notre GitHub : [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. Q : De quoi ai-je besoin pour l'utiliser ?**
R : Un ordinateur et un microphone. Pour une meilleure précision, nous recommandons fortement un microphone casque dédié plutôt qu’un micro intégré pour ordinateur portable.

**5. Q : La précision n’est pas parfaite. Comment puis-je l'améliorer ?**
R : Essayez de parler clairement, à un volume et à un rythme constants. La plus grande différence est de réduire le bruit de fond et d’utiliser un meilleur microphone.
Personnalisation du logiciel (puissance avancée) : pour une précision de niveau supérieur, SL5 Aura utilise une fonctionnalité puissante appelée FuzzyMaps. Considérez-les comme votre dictionnaire personnel et intelligent. Vous pouvez créer des fichiers texte simples avec des règles pour corriger les erreurs de reconnaissance courantes et récurrentes.

Exemple : Si le logiciel entend souvent « get hap » au lieu de « GitHub », vous pouvez ajouter une règle qui corrige automatiquement cela à chaque fois.

Avantage : Cela vous permet d'"enseigner" au logiciel votre jargon technique spécifique, vos noms de produits, vos abréviations, ou même de créer des ensembles de règles pour des vocabulaires uniques. En personnalisant ces cartes, vous pouvez améliorer considérablement la précision de votre cas d'utilisation spécifique.

***

#### **Partie 1 : Questions générales**

**Q : Qu'est-ce que le SL5 Auro ?**
R : SL5 Auro est un programme de synthèse vocale hors ligne à l'échelle du système. Il vous permet de dicter du texte dans n'importe quelle application de votre ordinateur (par exemple, votre client de messagerie, un traitement de texte, un éditeur de code) sans avoir besoin d'une connexion Internet.

**Q : Que signifie « hors ligne » et pourquoi est-ce important ?**
R : « Hors ligne » signifie que tout le traitement vocal s'effectue directement sur votre ordinateur. Vos données vocales ne sont **jamais** envoyées à un serveur cloud (comme Google, Amazon ou OpenAI). Cela offre une confidentialité et une sécurité maximales, ce qui le rend idéal pour les informations confidentielles (par exemple pour les avocats, les médecins, les journalistes) et est entièrement conforme aux réglementations en matière de protection des données telles que le RGPD.

**Q : Est-ce vraiment gratuit ? Quel est le problème ?**
R : La « Community Edition » est 100 % gratuite et open source. Il n’y a pas de piège. Nous croyons au pouvoir des outils open source. Si vous trouvez le logiciel utile et souhaitez soutenir son développement continu, vous pouvez le faire via notre [Ko-fi page](https://ko-fi.com/sl5).

**Q : À qui s'adresse ce logiciel ?**
R : Il s'adresse à tous ceux qui écrivent beaucoup et souhaitent accroître leur efficacité : écrivains, étudiants, programmeurs, professionnels du droit et de la médecine, personnes ayant des limitations physiques ou toute personne préférant simplement parler plutôt que dactylographier.

#### **Partie 2 : Installation et configuration**

**Q : Quels systèmes d'exploitation sont pris en charge ?**
R : Le logiciel est testé et confirmé pour fonctionner sur Windows 11, Manjaro Linux, Ubuntu et macOS.

**Q : Comment puis-je l'installer sous Windows ?**
R : Nous fournissons un programme d’installation simple en un clic. Il s'agit d'un script .Bat qui nécessite des droits d'administrateur pour configurer l'environnement et télécharger les modèles nécessaires. Une fois exécuté, il gérera tout pour vous.

**Q : Le téléchargement des modèles est très volumineux. Pourquoi?**
R : Les modèles de reconnaissance vocale permettent au logiciel de fonctionner hors ligne. Ils contiennent toutes les données nécessaires pour que l’IA comprenne votre langage. Des modèles plus grands et plus précis peuvent atteindre plusieurs gigaoctets. Notre nouveau téléchargeur les divise en morceaux plus petits et vérifiables pour garantir un téléchargement fiable.

**Q : Je suis sous Linux. Quel est le processus ?**
R : Sous Linux, vous clonerez généralement le référentiel depuis GitHub et exécuterez un script d'installation. Ce script crée un environnement virtuel Python, installe les dépendances et démarre le service de dictée.

**Q : Lorsque je double-clique sur un fichier « .py » sous Windows, il s'ouvre dans un éditeur de texte. Comment puis-je l'exécuter ?**
R : Il s'agit d'un problème Windows courant où les fichiers « .py » ne sont pas associés à l'interpréteur Python. Vous ne devez pas exécuter directement les scripts Python individuels. Utilisez toujours le script de démarrage principal fourni (par exemple, un fichier « .bat »), car cela garantit que l'environnement correct est activé en premier.

#### **Partie 3 : Utilisation et fonctionnalités**

**Q : Comment puis-je l'utiliser pour dicter ?**
R : Tout d'abord, vous démarrez le « service de dictée » en exécutant le script approprié. Il fonctionnera en arrière-plan. Ensuite, vous utilisez un déclencheur (comme un raccourci clavier ou un script dédié) pour démarrer et arrêter l'enregistrement. Le texte reconnu sera alors automatiquement saisi dans la fenêtre actuellement active.

**Q : Comment puis-je améliorer la précision ?**
R : 1. **Utilisez un bon microphone :** Un microphone pour casque est bien meilleur que le micro intégré d'un ordinateur portable. 2. **Minimisez le bruit de fond :** Un environnement calme est essentiel. 3. **Parlez clairement :** Parlez à un rythme et à un volume constants. Ne marmonnez pas et ne vous précipitez pas.
Personnalisation du logiciel (puissance avancée) : Pour une précision de niveau supérieur, SL5 Auro utilise une fonctionnalité puissante appelée FuzzyMaps. Considérez-les comme votre dictionnaire personnel et intelligent. Vous pouvez créer des fichiers texte simples avec des règles pour corriger les erreurs de reconnaissance courantes et récurrentes.

Exemple : Si le logiciel entend souvent « get hap » au lieu de « GitHub », vous pouvez ajouter une règle qui corrige automatiquement cela à chaque fois.

Avantage : Cela vous permet d'"enseigner" au logiciel votre jargon technique spécifique, vos noms de produits, vos abréviations, ou même de créer des ensembles de règles pour des vocabulaires uniques. En personnalisant ces cartes, vous pouvez améliorer considérablement la précision de votre cas d'utilisation spécifique.

**Q : Puis-je changer de langue ?**
R : Oui. Le système prend en charge le « rechargement à chaud » en direct des fichiers de configuration. Vous pouvez modifier le modèle de langue dans la configuration et le service y basculera instantanément sans avoir besoin de redémarrer.

**Q : Qu'est-ce que "LanguageTool" ?**
R : LanguageTool est un vérificateur de grammaire et de style open source que nous avons intégré. Une fois votre discours transformé en texte, LanguageTool corrige automatiquement les erreurs de transcription courantes (par exemple, « droit » ou « écrire ») et corrige la ponctuation, améliorant ainsi considérablement le résultat final.

#### **Partie 4 : Dépannage et assistance**

**Q : J'ai démarré le service, mais rien ne se passe lorsque j'essaie de dicter.**
R : Vérifiez les points suivants :
1. Le service fonctionne-t-il toujours sur votre terminal/console ? Recherchez les messages d'erreur.
2. Votre microphone est-il correctement sélectionné comme périphérique d'entrée par défaut dans votre système d'exploitation ?
3. Le microphone est-il coupé ou le volume est-il trop faible ?

**Q : J'ai trouvé un bug ou j'ai une idée pour une nouvelle fonctionnalité. Que dois-je faire?**
R : C'est super ! Le meilleur endroit pour signaler des bugs ou suggérer des fonctionnalités est d'ouvrir un « problème » sur notre [GitHub repository](https://github.com/sl5net/Vosk-System-Listener).



**5. Q : La précision n’est pas parfaite. Comment puis-je l'améliorer ?**
R : La précision dépend à la fois de votre configuration et de la personnalisation du logiciel.

* **Votre configuration (les bases) :** Essayez de parler clairement à un volume et à un rythme constants. Réduire le bruit de fond et utiliser un bon microphone casque au lieu du micro intégré d'un ordinateur portable fait une énorme différence.

* **Personnalisation du logiciel (puissance avancée) :** Pour une précision de niveau supérieur, le SL5 Auro utilise une fonctionnalité puissante appelée **FuzzyMaps**. Considérez-les comme votre dictionnaire personnel et intelligent. Vous pouvez créer des fichiers texte simples avec des règles pour corriger les erreurs de reconnaissance courantes et récurrentes.

* **Exemple :** Si le logiciel entend souvent « get hap » au lieu de « GitHub », vous pouvez ajouter une règle qui corrige automatiquement cela à chaque fois.
* **Avantage :** Cela vous permet d'"enseigner" au logiciel votre jargon technique spécifique, vos noms de produits, vos abréviations, ou même de créer des ensembles de règles pour des vocabulaires uniques. En personnalisant ces cartes, vous pouvez améliorer considérablement la précision de votre cas d'utilisation spécifique.




### Plongée architecturale approfondie : réaliser un enregistrement continu de style « talkie-walkie »

Notre service de dictée met en œuvre une architecture robuste pilotée par l'état pour offrir une expérience d'enregistrement transparente et continue, semblable à l'utilisation d'un talkie-walkie. Le système est toujours prêt à capturer l'audio, mais ne le traite que lorsqu'il est explicitement déclenché, garantissant ainsi une réactivité élevée et une faible utilisation des ressources.

Ceci est réalisé en découplant la boucle d'écoute audio du thread de traitement et en gérant l'état du système avec deux composants clés : un indicateur d'événement `active_session` et notre `audio_manager` pour le contrôle du microphone au niveau du système d'exploitation.

**La logique de la machine à états :**

Le système fonctionne en boucle perpétuelle, gérée par un seul raccourci clavier qui bascule entre deux états principaux :

1. **État d'écoute (par défaut/prêt) :**
* **Condition :** L'indicateur `active_session` est `False`.
* **Statut du micro :** Le microphone est **muet** pour « réactiver le microphone() ». L'écouteur Vosk est actif et attend une entrée audio.
* **Action :** Lorsque l'utilisateur appuie sur la touche de raccourci, l'état change. Le drapeau `active_session` est défini sur `True`, signalant le début d'une "vraie" dictée.

2. **État de traitement (l'utilisateur a fini de parler) :**
* **Condition :** L'utilisateur appuie sur la touche de raccourci alors que l'indicateur `active_session` est `True`.
* **Statut du micro :** La **première action** consiste à **couper** immédiatement le microphone via `mute_microphone()`. Cela arrête instantanément le flux audio vers le moteur Vosk.
*   **Action:**
* L'indicateur `active_session` est défini sur `False`.
* Le morceau audio final reconnu est récupéré de Vosk.
* Le fil de traitement est lancé avec ce texte final.
* Surtout, dans un bloc «finally», le thread de traitement exécute «unmute_microphone()» une fois terminé.

**La « magie » du signal de réactivation :**

La clé de la boucle sans fin est l'appel final `unmute_microphone()`. Dès que le traitement de la dictée « A » est terminé et que le microphone est réactivé, le système revient automatiquement et instantanément à l'état **ÉCOUTE**. L'auditeur Vosk, qui attendait patiemment, recommence immédiatement à recevoir de l'audio, prêt à capturer la dictée « B ».

Cela crée un cycle très réactif :
`Appuyez sur -> Parler -> Appuyez sur -> (Muet et traitement) -> (Réactivation et écoute)`

Cette architecture garantit que le microphone n'est coupé que pendant la brève durée du traitement du texte, ce qui donne au système une sensation instantanée pour l'utilisateur tout en conservant un contrôle robuste et en empêchant les enregistrements incontrôlables.