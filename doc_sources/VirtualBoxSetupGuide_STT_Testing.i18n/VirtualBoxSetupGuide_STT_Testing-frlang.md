# Guide de configuration de VirtualBox pour les tests de projets STT

Ce guide fournit les étapes recommandées pour configurer une machine virtuelle Ubuntu 24.04 stable et performante dans VirtualBox. Suivre ces instructions créera un environnement cohérent pour tester l'application STT et évitera les problèmes courants tels que la lenteur de l'installation, le blocage du système et l'absence de fonctionnalités du presse-papiers.

## Prérequis

- VirtualBox installé sur la machine hôte.
- Un fichier ISO Ubuntu 24.04 Desktop téléchargé.

## Matériel hôte de référence

Cette configuration a été testée et validée sur le système hôte suivant. Les performances peuvent varier sur d'autres matériels, mais les paramètres de stabilité doivent s'appliquer universellement.

- **Système d'exploitation :** Manjaro Linux
- **Noyau :** 6.6.94
- **Processeur :** 16 × AMD Ryzen 7 3700X
- **Mémoire :** 31,3 Go de RAM
- **Processeur graphique :** NVIDIA GeForce GTX 1050 Ti

---

## Partie 1 : Création et configuration de VM

Ces paramètres sont essentiels pour les performances et la stabilité.

### Étape 1.1 : Créer la nouvelle machine virtuelle

1. Dans VirtualBox, cliquez sur **Nouveau**.
2. **Nom :** `Testeur Ubuntu STT` (ou similaire).
3. **Image ISO :** Laissez ce champ vide.
4. Cochez la case : **"Ignorer l'installation sans assistance"**.
5. Cliquez sur **Suivant**.
6. **Matériel :**
- **Mémoire de base :** « 4 096 Mo » ou plus.
- **Processeurs :** « 4 » ou plus.
7. Cliquez sur **Suivant**.

### Étape 1.2 : Créer le disque dur virtuel (CRITIQUE)

Il s’agit de l’étape la plus importante pour une installation et des performances rapides.

1. Sélectionnez **"Créer un disque dur virtuel maintenant"**.
2. Définissez la taille du disque sur **40 Go** ou plus.
3. Sur l'écran suivant, modifiez le type de stockage en **"Taille fixe"**.
> **Pourquoi ?** Un disque de taille fixe est pré-alloué et évite les énormes goulots d'étranglement d'E/S qui se produisent lorsqu'un disque « alloué dynamiquement » est constamment redimensionné pendant l'installation.
4. Cliquez sur **Créer** et attendez la fin du processus.

### Étape 1.3 : Paramètres finaux de la VM

Sélectionnez la VM nouvellement créée et cliquez sur **Paramètres**. Configurez les éléments suivants :

- **Système -> Carte mère :**
- **Jeu de puces :** `ICH9`
- Cochez **"Activer EFI (OS spéciaux uniquement)"**.

- **Affichage -> Écran :**
- **Contrôleur graphique :** `VMSVGA`
- **Décochez "Activer l'accélération 3D"**.
> **Pourquoi ?** L'accélération 3D est une cause fréquente de blocage et de blocage du système chez les invités Linux. Le désactiver améliore considérablement la stabilité.

-   **Stockage:**
- Sélectionnez le **Contrôleur SATA**. Cochez la case **"Utiliser le cache d'E/S de l'hôte"**.
- Sélectionnez le fichier du disque virtuel (`.vdi`). Cochez la case **"Disque SSD"**.
- Sélectionnez le lecteur optique **Vide**. Cliquez sur l'icône du CD à droite et **"Choisissez un fichier disque..."** pour joindre votre ISO Ubuntu 24.04.

Cliquez sur **OK** pour enregistrer tous les paramètres.

---

## Partie 2 : Installation du système d'exploitation Ubuntu

1. Démarrez la machine virtuelle.
2. Procédez à la configuration de la langue et du clavier.
3. Lorsque vous atteignez « Mises à jour et autres logiciels », sélectionnez :
- **Installation minimale**.
- **Décochez** "Télécharger les mises à jour lors de l'installation d'Ubuntu".
4. Poursuivez l'installation jusqu'à ce qu'elle soit terminée.
5. Une fois terminé, redémarrez la VM. À l'invite, supprimez le support d'installation (appuyez sur Entrée).

---

## Partie 3 : Post-installation (ajouts d'invités)

Cette étape permet le partage du presse-papiers, le glisser-déposer et le redimensionnement automatique de l'écran.

### Étape 3.1 : Installer l'ISO des ajouts d'invité sur l'hôte (si nécessaire)

Sur votre **machine hôte**, assurez-vous que le package ISO Guest Additions est installé.

- **Sur Arch/Manjaro :**
    ```bash
    sudo pacman -S virtualbox-guest-iso
    ```
- **Sur Debian / Ubuntu :**
    ```bash
    sudo apt install virtualbox-guest-additions-iso
    ```

### Étape 3.2 : Installer les ajouts d'invités dans la machine virtuelle Ubuntu

Effectuez ces étapes **dans votre machine virtuelle Ubuntu en cours d'exécution**.

1. **Préparez Ubuntu :** Ouvrez un terminal et exécutez les commandes suivantes pour installer les dépendances de build.
    ```bash
    sudo apt update
    sudo apt install build-essential dkms linux-headers-$(uname -r)
    ```
2. **Insérez le CD :** Dans le menu supérieur de VirtualBox, accédez à **Périphériques -> Insérer l'image du CD des ajouts d'invité...**.
3. **Exécutez le programme d'installation :**
- Une boîte de dialogue peut apparaître vous demandant d'exécuter le logiciel. Cliquez sur **Exécuter**.
- Si aucune boîte de dialogue n'apparaît, ouvrez le gestionnaire de fichiers, cliquez avec le bouton droit sur le CD `VBox_GAs...`, choisissez **"Ouvrir dans le terminal"** et exécutez la commande :
      ```bash
      sudo ./VBoxLinuxAdditions.run
      ```
4. **Redémarrer :** Une fois l'installation terminée, redémarrez la VM.
    ```bash
    reboot
    ```
5. **Activer les fonctionnalités :** Après le redémarrage, accédez au menu **Périphériques** et activez **Presse-papiers partagé -> Bidirectionnel** et **Glisser-déposer -> Bidirectionnel**.

Votre environnement de test stable et performant est maintenant prêt.