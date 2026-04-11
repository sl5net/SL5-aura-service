# Mode Terminal (Exclusion de langue)

Le mode Terminal est un état de configuration dans lequel aucun module linguistique spécifique n'est installé ou configuré pour les unités de traitement vocal/texte.

## Comment activer
Lors de la configuration initiale ou du script de sélection de la langue, lorsque vous êtes invité à indiquer la **Langue principale**, saisissez :
- `n`
- 'aucun'
- '0'

## Effets
- **EXCLUDE_LANGUAGES** est défini sur « tout ».
- Aucun modèle spécifique à une langue (comme les modèles Whisper ou Vosk) ne sera téléchargé ou initialisé.
- Le système fonctionne en mode « Terminal uniquement », utile pour les environnements à faible capacité de disque ou lorsque seuls les outils CLI de base sont requis sans prise en charge vocale localisée.

## Variables d'environnement
Lorsqu'elles sont actives, les exportations suivantes sont générées :
__CODE_BLOCK_0__