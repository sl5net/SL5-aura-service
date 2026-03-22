import re  # noqa: F401

# ============================================================
# Koan 03: Difficult Names – Fuzzy Matching in Practice
# ============================================================
#
# LEARNING GOAL:
#   Vosk often mishears difficult names. With regex you can
#   still match reliably – even with recognition errors.
#
# TASK:
#   Try to say this title:
#   "Your Most Noble Excellency Arch Administrative Councillor"
#
#   Then check what Vosk actually heard:
#   grep "📢📢📢" log/aura_engine.log | tail -5
#
#   Activate the rule that fits best (remove '#').
#
# QUESTION TO THINK ABOUT:
#   Which rule is more robust – the exact or the .* one?
#   What are the trade-offs of r'^Your Most Noble.*$'?
#
# NEXT STEP: Koan 04
# ============================================================

FUZZY_MAP_pre = [
    # Exact match (precise but fragile):
    # ('Great job!', r'^Your Most Noble Excellency.*$', 90, {'flags': re.IGNORECASE}),

    # Flexible match:
    # ('Success!', r'^.*Xenochronistic Chronology.*$', 90, {'flags': re.IGNORECASE}),

    # Fuzzy match for the name:
    ('Phonetics mastered!', r'^.*(Countess|Mondes|kund des|Kaum des).*$', 90, {'flags': re.IGNORECASE}),
]

difficultNames = """
This is an excellent progression! To create a name that is phonetically maximum difficult to pronounce, we must overuse English consonant clusters, archaic titles, and unusual syllable combinations.

Here is the result:

Title:
Your Most Noble Excellency, Arch-Administrative-Councillor-of-Przewalskyst-Silesia-Westphalia, Royal-Electoral Deputy-Substitute and Authentic Trustee of Xenochronistic Chronology.

Name:
Phryxts-Gzwryl-Wzesch-Chrysth, Countess of and to Squelch-Quartzh-Pfrts-Blackened-Crest.

Can you pronounce the title?
Can you pronounce the name?

What interesting things can you find in
log/aura_engine.log?

If you have multiple friends who are also Countesses? How do you distinguish them in speech output?


"""



