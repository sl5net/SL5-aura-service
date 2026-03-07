La Sortierung ergibt sich aus der Kombination der **alphabetischen Sortierung** auf jeder Ebene et la **Hierarchie** der Ordner.

Prinzip "First Match Wins", bestimmt durch die Lade-Reihenfolge die Priorität.

Vous pouvez démarrer un programme d'assistance en ligne complet au niveau « DE DE », « en-US » et « plugins ».

---

## Allgemeine Sortier- und Prioritätsreihenfolge

Les chargeurs (et la priorité) sont placés dans le règlement par la sortie alphabétique de l'ordre et du module sur Ebène.

### 1. Globale Ordner-Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst alphabetisch durchlaufen:

| Ordre | Priorité | Annonce |
| :--- | :--- | :--- |
| `de-DE` | **1. Priorité** | Wird zuerst geladen. |
| `en-US` | **2. Priorité** | Wird nach `de-DE` geladen. |
| `plugins` | **3. Priorité** | Wird zuletzt geladen. |

### 2. Ladung der Kern-Regeln (de-DE et en-US)

Les règles au sujet des noyaux de noyaux sont disponibles dans la liste `fuzzy_map_pre` créée.

### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

Les plug-ins ont été créés à l'origine par l'ordre alphabétique des « plugins » en « DE-DE » et « en-US » disponibles.

Les commandes intérieures des « plugins » contiennent les commandes les plus diverses par ordre alphabétique :

| Plug-in | Feuilles alphabétiques |
| :--- | :--- |
| `CCC_tue` | 1. Plug-in |
| `chiffres_à_numéros` | 2. Plug-in |

### 4. Dernière liste de priorités pour `FUZZY_MAP_pre`

Der Ladevorgang sammelt *alle* gefundenen Regeln in die finale Liste. Priorité aux priorités :

| Place dans `fuzzy_map_pre` | Pfad zur Regel | Priorité |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (Basis-Sprachregeln) |
| **2.** | `en-US/FUZZY_MAP_pre.py` | Haut (Basis-Sprachregeln) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Moyen (Les plugins sont sortis par alphabet, `CCC` kommt vor `digits`) |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig (Les plugins sont disponibles en alphabet alphabétique) |

---

## Wichtig : Fokus auf die Sprache (Contextabhängigkeit)

C'est à ce moment-là que l'activité active Sprache est filtrée.

Si vous n'êtes pas sûr du réglage pour **Deutsch (`de-DE`)** chargé, vous aurez droit à une priorité logique, le réglage de noyau est également adapté aux réglages de plug-in :

1. **Kern-Regeln :** `de-DE/FUZZY_MAP_pre.py`
2. **Plugin-Regeln (CCC) :** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **Plugin-Regeln (Chiffres) :** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**Fazit zur Priorisierung :**

* **Kern-Regeln** permet de créer tous les plugins à partir de la sortie alphabétique de l'ordre pour qu'ils soient disponibles.
* **Les plugins pris en charge** sont indiqués par ordre alphabétique selon le nom des commandes de plugins (`C` ou `D`). Ceci signifie que `CCC_tue` a une priorité ici comme `digits_to_numbers`.