# Recherche et exécution de règles interactives

Ce projecteur met en lumière le système interactif de recherche et d'exécution de règles, reliant les commandes vocales, la navigation en direct et l'exécution instantanée.

## Fonctionnalités principales
[1] **Recherche en direct à double volet (`fzf`) :** Le volet de gauche filtre les fichiers de règles ; le volet droit affiche l'aperçu du contexte de ligne via `preview_rule.py`.
[2] **Exécutions instantanées (`Entrée` / `Ctrl+R`) :** Exécute instantanément la commande cible extraite via `run_palette_command.py` en arrière-plan.
[3] **Édition directe (`Ctrl+E`) :** Lance l'éditeur (CudaText avec `@line`, Kate/VS Code avec `--line`) directement sur la ligne ciblée.
[4] **Touche de raccourci de fenêtre flottante :** Lié à « Super+S » pour un flux de travail d'espace de travail rapide et intégré au bureau.
[5] **Propulsé par commande vocale :** De nombreuses commandes vocales préconfigurent les modèles de recherche dans `search_rules.sh` pour des recherches rapides et ciblées.

## Prise en charge multiplateforme
- **Linux Bash (`run_rule.sh` / `search_rules.sh`) :** Implémentation complète avec suivi de l'historique et opérations du presse-papiers (`Ctrl+X` / `Ctrl+A`).
- **Windows PowerShell (`search_rules.ps1`) :** Outil compagnon offrant des fonctionnalités de recherche de terminal légères.

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260727_155546.png)

![Interactive Rule Search Console](.././assets/interactive_rule_search_wie_wetter_heute20260727.png)

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260814.png)