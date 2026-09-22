> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../Flexibilität_Binärlogik_und_Komplexität.md).*

## The flexibility of the rules: From binary logic to complexity

The combined priority and processing logic (sequential sort, full match stop, cumulation, fuzzy fallback) offers remarkable flexibility:

### 1. Simple (binary) control through highest priority

By positioning a **highest priority rule with a full match stop**, a simple on/off mechanism (`Toggle`) can be configured.

*   **Example:** A rule at the top of `FUZZY_MAP_pre` can recognize a specific input string (e.g. a simple command word), process it immediately and thus block the entire subsequent cascade for this token. This allows the configuration of simple commands or states that only allow two words/commands.

### 2. Complex customizations and framework integration

At the same time, the structure allows the implementation of complex, cascading modifications that are necessary for specific framework requirements (such as CodeIgniter or similar):

*   **Cumulation:** Cumulation allows multiple rules to be applied sequentially to the text, for example to gradually convert the naming conventions or placeholders of a framework into a desired output.
*   **Plug-ins:** The hierarchical loading logic via `plugins/` ensures that project-specific or framework-specific rules (e.g. for CodeIgniter) can be added as separate modules. These plug-in rules have a defined but lower priority than the core language rules, which leaves the core logic untouched but allows the behavior to be specifically extended.

**Conclusion:** Whether it is the binary switching of control words or the detailed adaptation to the conventions of a complex framework - the hierarchy of priorities (module > row) and the control through the stop criterion of the Full Match provide the necessary control over the processing process.

