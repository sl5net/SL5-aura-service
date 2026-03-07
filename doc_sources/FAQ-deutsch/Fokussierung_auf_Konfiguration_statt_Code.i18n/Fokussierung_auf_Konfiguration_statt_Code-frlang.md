## Die Mächtigkeit der Configuration: Keine Programmierung notwendig

Les caractéristiques des systèmes sont telles que les complexes sont complexes et ne nécessitent pas l'observation de la programmation traditionnelle.

### 1. Fonctionnement de la configuration à partir du code

La logique générale des systèmes est également due à la **configuration** de la règle de réglage (`(Zielwert, Regex-Muster, Fuzzy-Wert, Optionen)`) et à la **position physique** de la règle dans les nouvelles dates (Modul-Reihenfolge et Zeilennummer) prioritaires.

* **Keine Programmierkenntnisse nötig:** Neue Transformationen or spezifische Verhaltensweisen erfordern kein Eingreifen in den Kerncode oder die Anwendung komplexer Funktionen, sondern lediglich das Hinzufügen ou de Neuanordnen von Configurationseinträgen in den Mapping-Dateien.

### 2. Les rouleaux de contrôle régulier (Regex)

Lorsque la configuration classique des expressions régulières est facile (par exemple, une utilisation simple des chaînes jusqu'à la correspondance complète exacte), l'intégration des ** expressions régulières (PregReg) ** est une énorme extension des fonctionnalités.

* **Vorteil pour une erreur simple :** Pour les meilleures erreurs, comme les définitions des critères d'arrêt (`^Wort$`) ou un modèle d'inclusion d'encre simple, vous n'avez aucun élément Regex-Kenntnisse fourni.
* **Möglichkeit für Experten:** Wer komplexe Muster (Lookaheads wie `(?!Haus)`) nutzen möchte, kann die tun, um hochspezifische Kontrolmechanismen zu Implementieren, Ohne die Einfachheit für Gelegenheitsnutzer zu Opfern.
* **Möglichkeit für Experten:** Geräte/Spiele zu steuern ... voir Plugin **config/maps/plugins/game/0ad/**

**Fazit :** Le système est censé être ausgelegt, une masse maximale et un contrôle sur l'interprétation du texte à deux, qui ont défini les **dates réglementaires** et défini le logiciel de gestion et le moteur Kern de manière à ce que l'interprétation et les priorités soient claires et précises. est.