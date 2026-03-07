# Logique prioritaire (avec Fuzzy et Fallback)
Les solutions Fuzzy complètes sont disponibles en tant que solution de repli.


---

## La nouvelle logique de priorité (avec Fuzzy et Fallback)

Avec cette définition (`if not current_rule_matched:`), dans la combinaison avec le mode `default_mode_is_all = True` (commulierung), vous obtiendrez un **zweistufiger Prioritäts-Workflow** :

### Phase 1 : La priorité élevée (déterministe) Durchlauf

Le moteur a défini la liste standard `fuzzy_map_pre` (Modul-Reihenfolge > Zeilennummer).

#### A. Stopp-Kriterium (Höchste Priorität)

Lorsqu'un règlement **Full Match** (`^...$`) est terminé, l'organisation de l'organisation de ce jeton est arrêtée.

* **Prioritäts-Konsequenz :** Die Regel, die am höchsten in der List steht et un Full Match erzielt, gewinnt definitiv et bedet den Prozess.

#### B. Kumulations-Kriterium (Hohe Priorität)

Lors d'un match **un match complet**, d'un **match partiel** ou d'un sonstige Ersetzung (sans Stopp-Kriterium) erzielt :

* Die Ersetzung wird angewendet.
* **WICHTIG :** La variable `current_rule_matched` sera utilisée avec `True`.
* Die Verarbeitung geht zur nächsten Regel über (Kumulation).

**Prioritäts-Konsequenz :** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**. Frühere Regeln modifie le texte pour les différentes règles.

---

### Phase 2 : Le repli de faible priorité (flou)

Le Fuzzy-Check n'est pas authentifié, lorsque le processus déterministe (Phase 1) supprime les pertes et **une même règle** s'applique (`current_rule_matched` est jusqu'à `False`).

Lorsque le Fuzzy-Check est affiché, doré :

1. La fonction Fuzzy telle qu'elle est dans le texte prévu à l'heure actuelle, le **Zielwert** (« remplacement ») est également (basierend auf der Schwelle).
2. Lorsqu'un Fuzzy-Match est généré, la configuration est effectuée.
3. **WICHTIG :** La **fonction Fuzzy-Funktion a arrêté la mise en œuvre douce, après le premier Fuzzy-Match généré par **.

#### La priorité du règlement flou a-t-elle été définie :

```python
# Pseudo-Code:
for rule in fuzzy_map_pre:
    # 1. Deterministic/Regex checks here...

# Wenn Phase 1 beendet ist und KEIN Match gefunden wurde:
if not current_rule_matched:
    # 2. Fuzzy Fallback
    for rule in fuzzy_map_pre: # WIRD HIER DIE LISTE NOCHMAL DURCHLAUFEN?
        # Führe den Fuzzy-Check auf Basis der replacement/threshold der Regel durch.
```

**La Fuzzy-Funktion, wird nur am Ende aufgerufen.

---

## Finales Priorités-Fazit

Unabhängig davon, comme le Fuzzy-Suche im Detail implémenté par Solange, la **Phase déterministe (Phase 1)** avant et dans la Reihenfolge der Liste durchläuft, doré :

**La haute priorité se trouve dans le règlement, elle apparaîtra dans `fuzzy_map_pre`, et elle sera également basée sur la logique du déterminisme (match complet ou cumul).**

1. **Regeln mit Stopp-Kriterium (^...$):** Müssen zuerst stehen, um ihre hohe Priorität auszuspielen.
2. **Regeln zur Kumulation (partieller Match) :** Müssen in der logischen Reihenfolge der Transformationen stehen (vom Rohtext zur finalen Form). Vous pouvez définir `current_rule_matched` sur `True` et **bloquer** en utilisant les Fuzzy-Fallbacks pour ce jeton.
3. **Fuzzy-Fallback :** La **priorité minimale**. Nous sommes en activité lorsque la réglementation déterministe est appliquée.

**Ce qui :** Jede Regel (auch un kumulierende, nicht-stoppende Regel), meurt dans la phase 1, **désactivé le Fuzzy-Fallback** pour ce jeton. Dies muss beim Design der generischen Regeln berücksichtigt werden.