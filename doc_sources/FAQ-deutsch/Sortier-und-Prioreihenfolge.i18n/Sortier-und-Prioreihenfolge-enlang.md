> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../Sortier-und-Prioreihenfolge.md).*

The sorting results from the combination of **alphabetical sorting** at each level and the **hierarchy** of the folders.

Principle 'First Match Wins', determined by the loading order, decides the priority.

You start from a common root directory that contains `de-DE`, `en-US`, and `plugins`.

---

## General Sorting and Priority Order

The loading order (and thus the priority) is usually determined by the alphabetical sorting of the folders and modules at each level.

### 1. Global Folder Level (Highest Priority)

The folders at the top level are processed alphabetically first:

| Folder | Priority | Remark |
| :--- | :--- | :--- |
| `de-DE` | **1. priority** | Loads first. |
| `en-US` | **2. priority** | Loaded to `de-DE`. |
| `plugins` | **3. priority** | Last loaded. |


### 2. Loading of the Core Rules (de-DE and en-US)

The rules from these core language folders are first inserted into list `fuzzy_map_pre`.

### 3. Loading of the plug-in rules (Lower priority)

The plug-ins come only in third place because the folder `plugins` comes alphabetically after `de-DE` and `en-US`.

Within the `plugins` folder, the subfolders are traversed alphabetically again:

| Plug-in | Alphabetical Order |
| :--- | :--- |
| `CCC_tue` | 1. Plug-in |
| `digits_to_numbers` | 2. Plug-in |


### 4. Final priority chain for `FUZZY_MAP_pre`

The loading process collects *all* found rules into the final list. Priority order:

| Place in `fuzzy_map_pre` | Path to the rule | Priority |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Highest** (Basic language rules) |
| **2.** | `en-US/FUZZY_MAP_pre.py` | High (basic language rules) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Middle High (Plugins are sorted alphabetically, `CCC` comes before `digits`) |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Low (plugins are sorted alphabetically) |

---

## Important: Focus on language (context dependency)

It is filtered according to the currently active language.

Loading only the rules for **German (`de-DE`)** results in a more logical priority that values core rules higher than plugin rules:

1.  **Core Rules:** `de-DE/FUZZY_MAP_pre.py`
2.  **Plugin Rules (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3.  **Plugin Rules (Digits):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**Conclusion on prioritization:**

*   **Core rules** prevail against all plugins because they are loaded first by sorting the folders alphabetically.
*   **Plugins among themselves** are sorted strictly alphabetically according to the name of the plugin folder (`C` before `D`). This means that `CCC_tue` has a higher priority than `digits_to_numbers`.

