# clarifier le comportement exact du workflow de votre système :
  
### Explication corrigée du workflow intégré

la première règle pour **Input Transformation** et **Labeling** avant que l'action de recherche finale soit exécutée par la deuxième règle.

#### 1. Saisie : "was ist ein haus"

#### 2. Règle 1 : Étiquetage/Transformation

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
 {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool','fullMatchStop']})
```

* **Action :** L'entrée utilisateur `"was ist ein haus"` correspond avec succès.
* **Résultat (interne) :** Le système génère la sortie/étiquette `"was ist ein haus (Begriffsklärung)"`.
* **Suite :** Puisque `fullMatchStop` est dans la `skip_list`, la règle correspondant **NE S'ARRÊTE PAS**. Le processus passe à la règle suivante, portant le contenu *transformé* ou *étiqueté*.

#### 3. Règle 2 : Action/Exécution générale

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
})
```

* **Action :** Le système correspond désormais probablement au **résultat/étiquette actuel** de l'étape précédente, qui est `"was ist ein haus (Begriffsklärung)"` (ou il correspond à l'entrée d'origine, mais le script exécuté donne la priorité à l'étiquette transformée).
* **Correspondance du préfixe :** Le préfixe (`was ist`) correspond toujours.
* **Groupe de capture :** Le groupe de capture `(?P<search>.*)` capture le reste de la chaîne :
* Si le système utilise la **sortie de la règle 1 comme nouvelle entrée**, il capture : **`haus (Begriffsklärung)`** (ou la chaîne transformée complète, qui est ensuite analysée par le script d'exécution).
* **Exécution :** Le script `wikipedia_local.py` est exécuté.

#### 4. Action finale :

* Le script `wikipedia_local.py` reçoit le terme/étiquette de recherche spécifiquement modifié.
* Le script effectue une recherche Wikipédia pour le terme prévu : **`haus (Begriffsklärung)`**.

**Conclusion:**

Cette configuration constitue une manière élégante de gérer les requêtes ambiguës ou génériques. En demandant à la règle spécifique de modifier l'entrée ou de générer une étiquette ciblée, puis en forçant le processus à continuer avec la règle de recherche générale, vous vous assurez que la recherche Wikipédia n'est pas exécutée pour le « haus » générique, mais pour l'entrée spécifique et sans ambiguïté : **`haus (Begriffsklärung)`**.

Cela confirme que l'exclusion de `fullMatchStop` est **essentielle** pour permettre à la première règle de pré-traiter et d'enrichir la requête avant qu'elle ne soit traitée par la règle d'exécution à usage général.

(sl5,4.12.'25 12:24 jeu.)