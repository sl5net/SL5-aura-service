# Attribut de règle : `execute_only` (Expérimental, 7.7.'26 Mar)

L'attribut `execute_only` est une option de configuration expérimentale conçue pour les règles qui déclenchent uniquement des scripts externes sans modifier ni remplacer le texte saisi.

## Aperçu
- **Type :** `bool` (par exemple, `True` ou `False`)
- **Cas d'utilisation principal :** Généralement utilisé en combinaison avec `on_match_exec` pour exécuter des scripts externes.

## Comment ça marche et comportement actuel
- **Optimisation de la vitesse :** (quelques millisecondes uniquement) Contourne les routines de post-traitement et de remplacement de texte, accélérant ainsi l'exécution immédiate de l'action déclenchée.
- **Aucun effet secondaire d'exclusion/d'inversion :** La définition de `execute_only` sur `True` n'empêche **pas** d'autres règles de correspondance d'évaluer le même texte d'entrée.
- **Halting Flow :** Si vous devez empêcher les règles suivantes de traiter le même texte d'entrée, vous devez actuellement mettre fin au flux d'exécution manuellement (par exemple, en lançant une exception à la fin de votre script déclenché ou de votre gestionnaire d'ensemble de règles).

## Exemple de configuration

```python
# EXAMPLE: gather metal
('gather metal',
 r'^(gather\s*)?(met\w+|mat\w+|metall|mit|zitat|metal|matcha|günther)$',
 85,
 {
     'flags': re.IGNORECASE,
     'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
     'on_match_exec': [CONFIG_DIR / '..' / '0ad_actions.py'],
     'execute_only': True, # Experimental: Fast execution, does not halt the rule-chain.
 }),
```