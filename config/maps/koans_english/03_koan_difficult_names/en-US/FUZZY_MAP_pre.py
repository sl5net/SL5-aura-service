# config/maps/koans_english/03_difficult_names/en-US/FUZZY_MAP_pre.py
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
# 2. If no regex matches, a simple fuzzy match is performed.

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

solution is below

"""


















































FUZZY_MAP_pre = [
    # TODO: Help match these tongue-twisters.

    # Maybe like this for the title?
    # ('Great job!', r'^Your Most Noble Excellency.*$', 90, {'flags': re.IGNORECASE}),

    # Or a partial match?
    # ('Success!', r'^.*Xenochronistic Chronology.*$', 90, {'flags': re.IGNORECASE}),

    # And for the name?
    ('Phonetics mastered!', r'^.*(Countess|Mondes|kund des|Kaum des|kund des).*$', 90, {'flags': re.IGNORECASE}),
]

#Kaum deskund des
