## Developer Guide: Advanced Fuzzy Map Regular Expressions

The Fuzzy Mapping system utilizes standard Python regular expressions, allowing for powerful matching and exclusion patterns, particularly through **Negative Lookaheads (`(?!...)`)**.

### Using Negative Lookaheads for Whitelisting

This pattern allows you to define a rule that applies to **everything EXCEPT** a specific list of words or phrases. This is especially useful in combination with the `empty_all` pattern to build cumulative, restricted rule sets.

| Goal | Example Rule (`FUZZY_MAP`) | Explanation |
| :--- | :--- | :--- |
| **Apply to All Except One Word** | `('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE})` | This rule will apply a replacement (or skip logic, here `''`) to **any text** that is *not* exactly "Haus". `(?!Haus)` is the Negative Lookahead, ensuring the text does not start with "Haus". |
| **Apply to All Except Multiple Words** | `('', r'^(?!Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE})` | This rule applies to **everything** that does not start with "Schach", "Matt", "bad", or "Haus". Use the OR pipe (`|`) within the lookahead group `(?!...)` to whitelist multiple terms. |

***

### Using Positive Lookaheads for Restricted Rules

The standard approach uses Positive Lookaheads or simple capturing groups to restrict a rule to *only* a specific list of words.

| Goal | Example Rule (`FUZZY_MAP`) | Explanation |
| :--- | :--- | :--- |
| **Apply Only to a Specific List** | `('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE})` | This rule only applies if the text starts with one of the listed words (Schach, Matt, bad, or Haus). The matched text is then replaced by the target (`Schachmatt`) based on the threshold. |

