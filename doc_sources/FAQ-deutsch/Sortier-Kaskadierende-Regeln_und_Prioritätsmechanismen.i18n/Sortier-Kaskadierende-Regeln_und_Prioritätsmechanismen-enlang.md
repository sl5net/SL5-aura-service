> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../Sortier-Kaskadierende-Regeln_und_Prioritätsmechanismen.md).*

# Cascading rule execution and priority mechanisms

All the necessary details to explain the complex interaction of priority, mode and fallback.

---

# Cascading rule execution and priority mechanisms

Our control system is based on strict, sequential processing, in which the position of a rule in the list `fuzzy_map_pre` determines its priority (module load order > row number).

This follows the principle of **cascading rule execution** (`default_mode_is_all = True`), where all matching rules are applied one after the other until a specific stop criterion is met.

## 1. The High Priority: The Deterministic Run

Processing begins with the passage through the rules in the loaded order. There are two types of applications that determine the priority:

### A. Absolute Stop Criterion (Highest Priority)
The rule with the highest priority that achieves a **complete match** (from `^` to `$`) on the token is applied and immediately ends all processing for this token (**First Match Wins**). This ensures that the most specific and deterministic rule takes precedence.

### B. Cumulation (transformation order)
If a rule matches but does not achieve a full match (`^...$`), the replacement is applied. However, processing moves on to the next rule. Since each rule works on the **already modified** text, the list order is crucial for **cascading** the transformations.

## 2. The Low Priority: The Fuzzy Fallback

The use of fuzzy logic (similarity score 0-100) serves exclusively as a fallback to correct typos in the raw text.

For performance and stability reasons, fuzzy logic is activated **only** if the entire deterministic run (point 1) has **not a single rule** applied. Each successful deterministic rule application sets the necessary flag, thereby **blocking** the fuzzy fallback for the current token.

## 3. External validation (LanguageTool)

After all rule-based replacements are completed, an additional check is performed by LanguageTool (LT) to correct any stylistic or grammatical errors.

However, this tool is skipped if the number of rule replacements performed relative to the original text length exceeds a threshold (`LT_SKIP_RATIO_THRESHOLD`). This ensures that LT is not applied to texts that have already been transformed by our cascade to such an extent that correction by LT would be error-prone.
