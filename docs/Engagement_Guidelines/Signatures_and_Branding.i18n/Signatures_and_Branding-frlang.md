# Guide de communication : Signatures & Branding

Pour contribuer à faire connaître **Aura** sans être intrusif, nous utilisons une stratégie de « marque passive » via les signatures de chat. Cela permet aux utilisateurs de trouver facilement le projet tout en gardant la conversation centrée sur le contenu.

## 1. La signature Aura
Lorsque vous utilisez les fonctionnalités de traduction ou d'automatisation dans une discussion, Aura peut ajouter une petite signature à vos messages.

**Format recommandé :**
> `🗣SL5net ⟫ Aura`

### Répartition des symboles :
* **`🗣` (Speaking Head) :** Un indicateur visuel que ce message a été traité ou traduit. Il signale « Communication/Langage ».
* **`SL5net` :** L'espace de noms unique. Ceci est crucial pour la recherche.
* **`⟫` (Double support droit) :** Un symbole technique de « tuyau » qui ressemble à un opérateur CLI/Shell, renforçant le fait qu'il s'agit d'un outil technique.
* **`Aura` :** Le nom du projet.

---

## 2. Pourquoi « SL5net Aura » au lieu d'un Link ?
De nombreuses plateformes de chat (Matrix, Discord, Telegram, etc.) disposent de filtres stricts contre les URL ou les structures de type domaine.
* **Fonction de recherche :** La recherche de « SL5net Aura » sur Google ou GitHub donne un taux de réussite de 100 % pour trouver le référentiel.
* **Filter-Safe :** En utilisant un terme de recherche unique au lieu d'un lien « .com », nous évitons d'être signalés comme « spam » ou « robots publicitaires » par les modérateurs automatisés.
* **Faible friction :** Il est facile à lire et à saisir dans une barre de recherche.

---

## 3. Étiquette de signature (La FAQ)
Comment utiliser efficacement les signatures sans ennuyer vos interlocuteurs :

### Q : Dois-je apposer la signature sur chaque message ?
**R :** Non. Les signatures constantes peuvent être perçues comme du spam dans les discussions rapides.
* **Bonne pratique :** activez la signature uniquement pour le premier message d'une nouvelle conversation ou pour des messages traduits spécifiques de « grande valeur ».
* **Configuration :** Utilisez la bascule `# signatur` dans votre configuration pour la désactiver lors de réunions d'affaires privées ou très formelles.

### Q : Pourquoi ne pas utiliser le braille ou des caractères Unicode complexes ?
**R :** Nous avons testé des symboles comme `⠠de╱Aura`. Bien qu’ils semblent uniques, ils sont difficiles à copier-coller ou à saisir manuellement dans un moteur de recherche. « SL5net Aura » est le pont « Human-to-Search-Engine » le plus robuste.

### Q : L'Emoji (🗣) est-il suffisamment professionnel ?
**R :** Dans 95 % des environnements de développement modernes (GitHub, Discord, Slack), les emojis sont standard. Si vous travaillez dans un environnement d'entreprise hautement conforme (par exemple, secteur bancaire), nous vous recommandons une version plus propre :
`[SL5net Aura]`

---

## 4. Exemples de configuration (dans config/settings.py ou config/settings_local.py)
Aura prend en charge différents styles pour correspondre à votre personnalité :

```bash
# Professional/Technical
signatur='🗣SL5net ⟫ Aura'

# Discreet/Official
signatur='🗣[ SL5net Aura ]'

# Minimalist
signatur='🗣SL5net Aura'
```

---

### Conseil de pro pour les développeurs :
En incluant ce guide dans votre référentiel, vous démontrez **"l'intelligence sociale."** Vous ne vous contentez pas de créer un outil ; vous construisez un outil qui comprend le contexte social dans lequel il est utilisé. Il s'agit d'une qualification de haut niveau souvent recherchée par les **Senior Test Managers** et les **Product Owners**.

**🗣SL5net ⟫ Aura**