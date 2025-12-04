# clarifying the exact behavior of your system's workflow:
    
### Corrected Explanation of the Integrated Workflow

the first rule for **Input Transformation** and **Labeling** before the final search action is executed by the second rule.

#### 1. Input: "was ist ein haus"

#### 2. Rule 1: Labeling/Transformation

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
 {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool','fullMatchStop']})
```

*   **Action:** The user input `"was ist ein haus"` is successfully matched.
*   **Result (Internal):** The system generates the output/label `"was ist ein haus (Begriffsklärung)"`.
*   **Continuation:** Since `fullMatchStop` is in the `skip_list`, the rule matching **DOES NOT STOP**. The process continues to the next rule, carrying the *transformed* or *labeled* content.

#### 3. Rule 2: General Action/Execution

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
})
```

*   **Action:** The system now likely matches the **current result/label** from the previous step, which is `"was ist ein haus (Begriffsklärung)"` (or it matches the original input, but the executed script prioritizes the transformed label).
    *   **Prefix Match:** The prefix (`was ist`) still matches.
    *   **Capture Group:** The capture group `(?P<search>.*)` captures the rest of the string:
        *   If the system uses the **Rule 1 output as the new input**, it captures: **`haus (Begriffsklärung)`** (or the full transformed string, which is then parsed by the execution script).
*   **Execution:** The `wikipedia_local.py` script is executed.

#### 4. Final Action:

*   The `wikipedia_local.py` script receives the specifically modified search term/label.
*   The script performs a Wikipedia search for the intended term: **`haus (Begriffsklärung)`**.

**Conclusion:**

This setup is an elegant way to handle ambiguous or generic queries. By having the specific rule modify the input or generate a targeted label and then forcing the process to continue to the general search rule, you ensure the Wikipedia search is run not for the generic "haus," but for the specific, disambiguated entry: **`haus (Begriffsklärung)`**.

This confirms that the exclusion of `fullMatchStop` is **essential** for allowing the first rule to pre-process and enrich the query before it is acted upon by the general-purpose execution rule.

(sl5,4.12.'25 12:24 Thu)
