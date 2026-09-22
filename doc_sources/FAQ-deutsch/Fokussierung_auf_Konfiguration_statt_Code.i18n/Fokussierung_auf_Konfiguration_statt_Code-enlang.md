> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../Fokussierung_auf_Konfiguration_statt_Code.md).*

## The power of the configuration: No programming necessary

The strength of the system is that it enables highly complex behavior without the need for traditional programming.

### 1. Focus on configuration instead of code

The entire logic of the system is controlled exclusively by the **configuration** of the rule tuples (`(Zielwert, Regex-Muster, Fuzzy-Wert, Optionen)`) and prioritized by the **physical position** of these rules in the respective files (module order and line number).

*   **No programming knowledge required:** New transformations or specific behaviors do not require any intervention in the core code or the application of complex functions, just the addition or rearrangement of configuration entries in the mapping files.

### 2. The role of regular expressions (regex)

While the most basic configuration is possible without regex (e.g. simple string replacement with exact full match), the integration of **Regular Expressions (PregReg)** allows for a huge expansion of functionality.

*   **Advantage for simple cases:** For most use cases, such as defining stop criteria (`^Wort$`) or simple inclusion patterns, only basic regex knowledge is required.
*   **Expert Opportunity:** Those who want to use complex patterns (lookaheads like `(?!Haus)`) can do so to implement highly specific controls without sacrificing simplicity for casual users.
*   **Ability for experts:** to control devices/games...see plugin **config/maps/plugins/game/0ad/**

**Conclusion:** The system is designed to provide a maximum level of control over text processing, where the **rule data** defines the business logic and the core engine is simply the reliable interpreter and executor of these priorities and cascades.
