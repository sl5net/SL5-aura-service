# Mécanismes de régulation et de priorité des priorités

Tous les détails notwendigen, un jeu complet de priorités, de modes et de solutions de repli pour les options.

---

# Mécanismes de régulation et de priorité des priorités

Notre système de réglage est basé sur une vérification séquentielle, à la position d'un réglage dans la liste `fuzzy_map_pre` dont la priorité est la meilleure (Modul-Lade-Reihenfolge > Zeilennummer).

Ce principe est suivi du **réglage des paramètres cachés** (`default_mode_is_all = True`), qui permet aux règles passées de s'adapter à un certain Stopp-Kriterium.

## 1. La haute priorité : la définition déterministe

Die Verarbeitung commence mit dem Durchlauf der Regeln in der geladenen Reihenfolge. Il y a deux types d'interventions qui ont la priorité :

### A. Stopp-Kriterium absolu (Höchste Priorität)
Le règlement avec la haute priorité, un **vollständigen Match** (de `^` à `$`) sur le Token sera modifié et le processus d'organisation pour ce Token est si fort (**First Match Wins**). Dies stellt sicher, dass die spezifischste und déterministischste Regel Vorrang hat.

### B. Cumulation (Transformationsreihenfolge)
Lorsqu'un règlement s'applique, il n'y a qu'un seul match (`^...$`) qui se déroule, ce qui signifie que la configuration est possible. Die Verarbeitung geht jedoch zur nächsten Regel über. Da jede Regel auf dem **bereits modifizierten** Text arbeitet, ist die Listenreihenfolge entscheidend for die **Kaskadierung** der Transformationen.

## 2. La priorité inférieure : le repli flou

L'Einsatz der Fuzzy-Logik (Ähnlichkeitsscore 0–100) est aussi efficace que Fallback, un tippfehler im Rohtext zu korrigieren.

Aus Performance- und Stabilitätsgründen wird die Fuzzy-Logik **nur dann** aktiviert, wenn der gesamte déterministische Durchlauf (Punkt 1) **keine einzige Regel** angewendet hat. Il s'agit d'une réglementation déterministe qui définit le nouveau drapeau et ** bloque ** le Fuzzy-Fallback pour le jeton actif.

## 3. La validation externe (LanguageTool)

Nach Abschluss all Regel-basierten Ersetzungen wird a zusätzliche Prüfung durch LanguageTool (LT) durchgeführt, um stilistische or grammaticalische Fehler zu beheben.

Cet outil est déjà utilisé, lorsque l'analyse des règles de réglage difficiles s'applique aux textes ursprünglichen d'une valeur de référence supérieure (`LT_SKIP_RATIO_THRESHOLD`). Dies stellt sicher, dass LT nicht auf Texte angewendet wird, die durch notre Kaskade bereits si brutalement transformé wurden, ass the Korrektur durch LT fehleranfällig wäre.