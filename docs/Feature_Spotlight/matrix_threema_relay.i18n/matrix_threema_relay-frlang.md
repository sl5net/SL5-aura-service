> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay.md).*

# Élément ↔ Relais GUI Threema Beta

Un petit démon qui reflète les messages entre **Element Desktop** (Matrix) et
**Threema Beta** (le client de bureau Threema) sur Linux/X11 en conduisant les deux
Windows comme un utilisateur le ferait : raccourcis clavier, presse-papiers et quelques clics de souris.

Pas d'API, pas de jetons, pas de bibliothèques Python supplémentaires. Seulement des outils en ligne de commande X11 standard.

## Ce que cela fait

| Direction | Que se passe-t-il |
|---|---|
| **Element → Threema** | Le dernier message *que vous* avez écrit dans Element est lu et, s'il est nouveau, collé dans Threema Beta et envoyé. |
| **Threema → Element** | Le dernier message *entrant* du chat Threema ouvert est copié via son menu contextuel et, s'il est nouveau, collé dans Element et envoyé. |

Utilisation typique: dicter ou taper dans une salle d'élément (par exemple avec Aura)
speech-to-text) et que le texte arrive dans un chat de trois, et voir le
Les réponses de troisma apparaissent dans la même pièce d'élément.

Les deux fenêtres doivent être ouvertes, connectées, et montrer le chat/salle que vous voulez relayer.

Protection contre les boucles

Un miroir bidirectionnel naïf rebondirait chaque message pour toujours. Le relais
empêche cela avec une histoire de courte durée (`relay_history.py`):

1. Chaque texte le relais est rappelé **avant** il est envoyé, pendant 180 secondes.
2. Si un texte apparaît de l'autre côté de cette histoire, c'est notre propre
   écho: il est marqué comme vu mais **non** transmis à nouveau.
3. Un texte qui est nouveau *et* inconnu est un message authentique et est transmis.

Les textes sont comparés avec l'espace blanc s'est effondré, de sorte que les différences de rupture de ligne de
copier/coller ne défait pas le gardien. Parce que les entrées meurent, vous pouvez envoyer le
Le même texte (par exemple "ok") à nouveau après le passage de la fenêtre.

Au démarrage, le dernier message courant de chaque côté est lu comme une **baseline** et est
*Non* transmis. Seuls les messages qui arrivent après le départ sont relayés.

Exigences

- Linux avec **X11** (`echo $XDG_SESSION_TYPE` doit imprimer `x11`). Wayland n'est pas soutenu.
- `xdotool`, `xclip`, `wmctrl` et `xset` (optionnel, utilisé pour désactiver l'économiseur d'écran)
- Elément Bureau (classe WM `element.Element`)
- Troisma Beta (classe WM `threema beta.Threema Beta`, p.ex. le Flatpak)
  `ch.threema.threema-desktop`)
- Python 3 avec virtualenv du projet
- `zsh` pour le script d'étalonnage unique

Configuration : calibrage unique

Troisma Beta dessine son propre menu contextuel qui ne peut pas être utilisé avec le clavier,
donc le relais clique sur "Copier le message" avec la souris aux positions par rapport à la
Fenêtre 3-ma. Mesurez-les une fois :

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

Le script demande trois positions de souris, chacune avec un compte à rebours (ne touchez pas la
Clavier, ne pas déplacer ou redimensionner la fenêtre :

1. **Click droit** le dernier message * entrant* (une bulle sur le côté gauche) et partir
   Le menu s'ouvre.
2. Déplacez la souris, sans cliquer, sur **"Copier le message"**.
3. Déplacez la souris sur le champ d'entrée **message**.

Le résultat est stocké dans `~/.config/threema-relay.conf`:

Sens de la clé
|---|---|
`FX`
Cliquez sur la position, les pixels au-dessus du bord inférieur de la fenêtre.
`DX`, `DY`
`INPUT_FX`, `INPUT_BOTTOM`
`DELAY_MENU`, `DELAY_COPY`.

Vérifiez l'étalonnage avec un nouveau message entrant comme le dernier dans le chat:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

Il imprime le texte copié sans le transmettre. L'étalonnage repose sur la fenêtre
géométrie: si vous changez beaucoup la taille de la fenêtre Threema, étalonnez à nouveau.

Utilisation

À partir de la racine du dépôt :

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

Options:

Option Effet
|---|---|
Intervalle de scrutin (par défaut `2.0`)
`--no-threema-to-element`
`--no-element-enter`=Passer les messages Threema dans le champ d'entrée de l'élément, mais ne **pas** les envoyer (mode de test sûr)=

Arrête avec `Ctrl+C`.

Première sortie recommandée : utilisez `--no-element-enter`, envoyez-vous un message dans Threema
et vérifiez qu'il apparaît dans le champ d'entrée d'Element. Alors lancez-vous sans option.

Exemple de journal :

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

Comment ça marche

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- *Up* dans le compositeur d'Element modifie votre dernier message; *Ctrl+A / Ctrl+C* copies
  it et *Escape* quitte le mode d'édition. C'est pourquoi seulement **votre dernier élément**
  Le message est relayé à Threema.
- Pour Threema a **sentinel string** est mis en premier dans le presse-papiers. Si c'est encore
  par la suite, rien n'a été copié (par exemple parce que votre propre message est le
  Le dernier et le clic frappent aucune bulle) et la tentative est ignorée.

Fichiers

Dossier Objet
|---|---|
`matrix_threema_relay.py`: Boucle principale, CLI, logique de décision (`classify_candidate`)
Lire le dernier message de l'élément
`send_to_threema_window.py`
`read_last_threema_message.py`=Lis le dernier message entrant de Threema, charge l'étalonnage
`send_to_element_window.py`
`relay_history.py`
`threema-relay.zsh`: Outil d'étalonnage et d'essai manuel (`calibrate`, `test`)
`test_threema_relay.py`= Tests unitaires (pas de X11 requis)=

Exécutez les essais avec:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

Limites

- **Le relais utilise votre souris et votre clavier. **** Au cours de chaque sondage, les
  Élément Windows sont concentrés et la souris saute brièvement (il est restauré). Ne pas
  Tapez pendant un sondage, ou utilisez un `--poll` plus long.
- Supprime le presse-papiers de chaque sondage.
- **Le message de la dernière fois dans Threema:** quand votre propre message est le dernier dans le Threema
  Chat, une réponse qui est arrivée juste avant qu'il ne soit pas vu.
- **Le dernier message** est lu par sondage. Si plusieurs messages arrivent dans un seul
  Seul le plus récent est relayé.
- **Texte seulement.** Les images, fichiers, réactions et modifications ne sont pas relayés.
- **Une paire de chat.** Quel que soit le chat/salle ouvert dans chaque fenêtre est utilisé.
- **Une ébauche dans le champ d'entrée de l'élément** sera combinée avec le prochain collé
  Message.
- **X11 seulement.** Wayland bloque les changements d'entrée synthétique et de foyer de fenêtre.
- Le relais désactive l'économiseur d'écran X11 et le DPMS au démarrage (`xset s off -dpms`);
  Ils restent à l'écart jusqu'à ce que vous les réactivez ou que vous vous connectiez à nouveau.

Dépannage

Symptôme Cause probable / Correction
|---|---|
Cochez `xdotool search --class "Threema Beta"` et `xprop WM_CLASS` (cliquez sur la fenêtre).
`Nothing copied` / no Threema → Element. Augmenter `DELAY_MENU`/`DELAY_COPY` dans la configuration d'une machine lente.
Le texte arrive dans Threema mais n'est pas envoyé.
Le texte de trois minutes apparaît dans l'élément mais n'est pas envoyé. Le relais a été lancé avec `--no-element-enter`.
Les nombres décimaux comme `0,9353` dans la configuration Écrit par une ancienne version de script sous un local allemand. Le code Python les accepte ; Calibrer à nouveau avec le script actuel écrit des points. Autres
