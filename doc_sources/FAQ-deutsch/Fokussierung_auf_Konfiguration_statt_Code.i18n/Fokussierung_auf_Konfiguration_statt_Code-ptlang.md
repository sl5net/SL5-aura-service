## Die Mächtigkeit der Konfiguration: Nenhuma programação notwendig

As estrelas dos sistemas são darin, dass es hochkomplexes Verhalten ohne the Notwendigkeit von tradicionaleller Programmierung ermöglicht.

### 1. Fokussierung auf Konfiguration Statt Code

A lógica geral dos sistemas será ausschließlich durch die **Konfiguration** der Regel-Tupel (`(Zielwert, Regex-Muster, Fuzzy-Wert, Optionen)`) gesteuert und durch die **physische Position** dieser Regeln in den jeweiligen Dateien (Modul-Reihenfolge und Zeilennummer) priorizado.

* **Keine Programmierkenntnisse notig:** Neue Transformationen ou spezifische Verhaltensweisen erfordern kein Eingreifen in the Kerncode ou the Anwendung komplexer Funktionen, sondern lediglich das Hinzufügen ou Neuanordnen von Konfigurationseinträgen in the Mapping-Dateien.

### 2. Die Rolle von Regulären Ausdrücken (Regex)

Quando a configuração básica de Regex é mais necessária (por exemplo, uma combinação de strings com correspondência completa exata), a integração de **Expressões regulares (PregReg)** resulta em uma enorme dificuldade de funcionalidade.

* **Vorteil für einfache Fälle:** Para o maior desafio, como as definições de Stopp-Kriterien (`^Wort$`) ou einfachen Inklusionsmustern, são apenas os elementos Regex-Kenntnisse forforderlich.
* **Möglichkeit für Experten:** Wer komplexe Muster (Lookaheads wie `(?!Haus)`) nutzen möchte, kann die tun, um hochspezifische Kontrollmechanismen zu implementieren, ohne die Einfachheit für Gelegenheitsnutzer zu opfern.
* **Möglichkeit für Experten:** Geräte/Spiele zu steuern ... veja Plugin **config/maps/plugins/game/0ad/**

**Fazit:** O sistema é darauf ausgelegt, ein maximales Mass an Kontrolle über die Textverarbeitung zu bieten, wobei die **Regel-Daten** die Geschäftslogik definieren und die Kern-Engine lediglich der zuverlässige Interpret und Ausführer dieser Prioritäten und Kaskaden isto.