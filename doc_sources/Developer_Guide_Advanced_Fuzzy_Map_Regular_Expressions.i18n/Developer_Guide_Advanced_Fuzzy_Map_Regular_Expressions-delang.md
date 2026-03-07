## Entwicklerhandbuch: Erweiterte reguläre Fuzzy-Map-Ausdrücke

Das Fuzzy-Mapping-System verwendet standardmäßige reguläre Python-Ausdrücke und ermöglicht leistungsstarke Matching- und Ausschlussmuster, insbesondere durch **Negative Lookaheads („(?!...)`)**.

### Verwendung negativer Lookaheads für das Whitelisting

Mit diesem Muster können Sie eine Regel definieren, die für **alles AUSSER** einer bestimmten Liste von Wörtern oder Phrasen gilt. Dies ist besonders nützlich in Kombination mit dem Muster „empty_all“, um kumulative, eingeschränkte Regelsätze zu erstellen.

| Ziel | Beispielregel (`FUZZY_MAP`) | Erklärung |
| :--- | :--- | :--- |
| **Auf alle außer einem Wort anwenden** | `('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE})` | Diese Regel wendet eine Ersetzung (oder Sprunglogik, hier „''`) auf **jeden Text** an, der *nicht* genau „Haus“ ist. „(?!Haus)“ ist der negative Lookahead, der sicherstellt, dass der Text nicht mit „Haus“ beginnt. |
| **Auf alle außer mehreren Wörtern anwenden** | `('', r'^(?!Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE})` | Diese Regel gilt für **alles**, was nicht mit „Schach“, „Matt“, „bad“ oder „Haus“ beginnt. Verwenden Sie die ODER-Verknüpfung („|“) innerhalb der Lookahead-Gruppe „(?!...)“, um mehrere Begriffe auf die Whitelist zu setzen. |

***

### Positive Lookaheads für eingeschränkte Regeln verwenden

Der Standardansatz verwendet positive Lookaheads oder einfache Erfassungsgruppen, um eine Regel *nur* auf eine bestimmte Liste von Wörtern zu beschränken.

| Ziel | Beispielregel (`FUZZY_MAP`) | Erklärung |
| :--- | :--- | :--- |
| **Nur auf eine bestimmte Liste anwenden** | `('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE})` | Diese Regel gilt nur, wenn der Text mit einem der aufgeführten Wörter beginnt (Schach, Matt, bad oder Haus). Der übereinstimmende Text wird dann basierend auf dem Schwellenwert durch das Ziel („Schachmatt“) ersetzt. |