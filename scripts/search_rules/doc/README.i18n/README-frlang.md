# Logique souhaitée

# Alt+F et Alt+G

## **Logique**

D'après la description et l'analogie avec **Alt+F**, la logique pour **Alt+G** devrait ressembler à ceci :

### **1. Passer du texte intégral → Idem (`Alt+G`)**

- **Action**:
- La requête de recherche actuelle (`CURRENT_QUERY`) est enregistrée dans `SAVED_QUERY`.
- Le champ de recherche est **vidé**.
- `DITTO_STATE` est défini sur `"1"`.
- Rechargement de l'interface graphique

### **2. En mode Idem**

- **Sur n'importe quelle entrée (frappe)** :
- Le mode DITTO est **automatiquement quitté** (`DITTO_STATE="0"`).
- Rechargement de l'interface graphique
- Le champ de recherche reste **vide** (pas de restauration de `SAVED_QUERY`).

### **3. Passer de DITTO → Texte intégral (`Alt+G` à nouveau)**

- **Action**:
- `DITTO_STATE` est défini sur `"0"`.
- Rechargement de l'interface graphique
- `SAVED_QUERY` est **restauré**. (cette étape ne fonctionne pas pour le moment 11.8.'26 22:18 mar)


---

## **Alt+F fonctionne et Alt+G ne fonctionne pas à 11.8.'26 22:18 mar**

Puisque **Alt+F** fonctionne correctement, nous pouvons adopter la **même logique** pour **Alt+G**.

### **Alt+F Logique (Fonctionne)**

- **Passer du mode Texte intégral → 1/Fichier** :