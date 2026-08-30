# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama_slow.py

# Ask_ollama_slow.py


try:
    # 1. ESSAYEZ : importation relative (pour l'appel python -m ...)

    from . import cache_core, normalizer, utils

except ImportError:
    # 2. FALLBACK : importation facile (pour les chargeurs de plugins)

    # IMPORTANT : Cela ne fonctionne que si les fichiers

    # normalizer.py, cache_core.py, utils.py

    # sont tous dans le même dossier que Ask_ollama.py.


    import cache_core
    import normalizer
    import utils

import hashlib
import json
import logging
import re

# inspection des importations
import sqlite3

# importer le système d'exploitation
import sys

# importer du yake
import time
import urllib.request

# importer la date et l'heure
# importer au hasard
from pathlib import Path
from urllib.error import HTTPError, URLError

# https://ollama.com/download



# --- CONFIGURATION ---

OLLAMA_API_URL = "http://localhost:11434/api/generate"

# GLOBAL_NORMALIZED_KEY = ""



SESSION_COUNT = 0

LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION AUDIO ---

create_bent_sine_wave_sound = True
try:
    project_root = Path(__file__).resolve().parents[5]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
except ImportError:
    pass


# def utils.log_debug2(message : str) :

# caller_info = "INCONNU :0"

# pile = inspecter.stack()

# si len(pile) > 1 :

# try:

# nom de fichier = os.path.basename(stack[1].filename)

# numéro_ligne = pile[1].lineno

# caller_info = f"{filename}:{line_number}"

# sauf exception :

# passeport

#
# t = f"⏱️{secDurationSinceExecFunctionStart()}s"

#
# print(f"{t}:[DEBUG_LLM] {caller_info} : {message}", file=sys.stderr)

# logging.info(f"{t} :{caller_info} : {message}")



# def normalize_for_hashing(texte) :

# retourner extreme_standardize_prompt_text(texte)

# # texte = texte.inférieur()

# # texte = re.sub(r'\s+', ' ', text).strip()

# # renvoyer le texte



# Liste très agressive de mots vides allemands (de la bibliothèque nltk)

# Ici, vous pouvez définir votre propre liste, encore plus longue





# --- CORRESPONDANCE INSTANTANÉE ---

def get_instant_match(user_text):
    """
    Sucht in der DB nach Keywords, die dem User-Text am ähnlichsten sind.
    Nutzt Python Set-Intersection (Schnittmenge) statt LLM.
    """
    utils.init_db()

    # 1. Divisez le texte utilisateur en mots (normalisation simple)

    # EXAMPLE: xs

    user_words = set(re.sub(r'[^\w\s]', '', user_text.lower()).split())
    # Supprimez les mots parasites pour une meilleure correspondance (facultatif mais utile)

    stop_words = {"computer", "aura", "bitte", "danke", "und", "oder", "wie", "was", "ist", "der", "die", "das",
                  "sofort", "schnell", "instant"}
    user_relevant = user_words - stop_words

    if not user_relevant:
        return None

    # utils.log_debug(f"🚀 MODE INSTANTANÉ : recherche d'une correspondance pour {user_relevant}…")


    try:
        conn = sqlite3.connect(utils.DB_FILE)
        c = conn.cursor()

        # Charger toutes les invites contenant des mots-clés

        c.execute("SELECT hash, keywords FROM prompts WHERE keywords IS NOT NULL")
        rows = c.fetchall()

        best_hash = None
        best_score = 0

        for row in rows:
            db_hash = row[0]
            db_keywords_str = row[1]
            if not db_keywords_str: continue

            db_keywords = set(db_keywords_str.split())

            # Compter les correspondances (Intersection)

            matches = user_relevant.intersection(db_keywords)
            score = len(matches)

            if score > best_score:
                best_score = score
                best_hash = db_hash

        # Décision : Nous avons besoin d'au moins 1 mot significatif comme hit

        if best_score >= 1:
            utils.log_debug(f"🚀 Instant Match gefunden! Score: {best_score} (Hash: {best_hash[:8]})")

            # Téléchargez une réponse à ce hachage (préférez celles bien notées)

            c.execute(
                "SELECT response_text FROM responses WHERE prompt_hash=? ORDER BY rating DESC, created_at DESC LIMIT 1",
                (best_hash,))
            resp_row = c.fetchone()
            conn.close()

            if resp_row:
                utils.play_cache_hit_sound()
                # return f"[MODE IMMÉDIATE] : {resp_row[0]}"

                return f"{resp_row[0]}"
        else:
            utils.log_debug("🚀 Kein ausreichender Match im Instant Modus.")
            conn.close()

        return None

    except Exception as e:
        utils.log_debug(f"Instant Mode Error: {e}")
        return None



# --- AIDE ---

def clean_text_for_typing(text):
    # EXAMPLE: X. - VAR äöüÄÖÜß

    allowed_chars = r'[^\w\s\.,!\?\-\(\)\[\]\{\}<>äöüÄÖÜß:;\'"\/\\@\+\=\~\#\%]'
    text = re.sub(allowed_chars, '', text)
    # EXAMPLE: Aucun

    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_readme_content():
    try:
        current_path = Path(__file__).resolve()
        for _ in range(6):
            current_path = current_path.parent
            readme_path = current_path / "README_AI-delang.md"
            if readme_path.exists():
                utils.log_debug(f"README gefunden: {readme_path}")
                content = readme_path.read_text(encoding='utf-8').strip()
                return content[:6000]
        return None
    except Exception as e:
        utils.log_debug(f"{e}")
        return None


def get_clipboard_content():
    if not utils.BRIDGE_FILE.exists(): return None
    try:
        content = utils.BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content: return content
        return None
    except Exception as e:
        utils.log_debug(f"{e}")
        return None


def load_history():
    if not utils.MEMORY_FILE.exists(): return []
    try:
        with open(utils.MEMORY_FILE, 'r', codage='utf-8') as f:
            return json.load(f)
    except Exception as e:
        utils.log_debug(f"{e}")
        return []


def save_to_history(user_text, ai_text):
    history = load_history()
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ai_text})
    if len(history) > utils.MAX_HISTORY_ENTRIES * 2:
        history = history[-(utils.MAX_HISTORY_ENTRIES * 2):]
    try:
        with open(utils.MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        utils.log_debug(f"{e}")


def secDauerSeitExecFunctionStart(reset=False):
    # Si reset=True OU la fonction s'exécute pour la toute première fois : régler l'heure

    if reset or not hasattr(secDauerSeitExecFunctionStart, "start_time"):
        secDauerSeitExecFunctionStart.start_time = time.time()
        return 0.00

    # Calculer la différence

    duration = time.time() - secDauerSeitExecFunctionStart.start_time
    return round(duration, 2)


def check_static_guardrails(text_raw):
    """
    Fängt Fragen ab, die auf falschen Annahmen basieren,
    bevor sie teure AI-Zeit verschwenden.
    """
    text = text_raw.lower()

    user_keywords_stict = ["benutzer", "user", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    # Si "Utilisateur" ET une "Action" se produit -> Bloquer.

    if any(k in text for k in user_keywords_stict):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts, Passwörter, Logins . "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    forbidden_terms = ["account erstellen", "passwort ändern", "login", "neuer benutzer"]
    if any(term in text.lower() for term in forbidden_terms):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts, Passwörter und Logins . "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    # 1. Gestion des utilisateurs (n'existe pas)

    user_keywords = ["benutzer", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    user_actions = ["entfernen", "löschen", "erstellen", "hinzufügen", "ändern", "wechseln", "neu"]

    # Si "Utilisateur" ET une "Action" se produit -> Bloquer.

    if any(k in text for k in user_keywords) and any(a in text for a in user_actions):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts oder Passwörter, Logins. "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    # 2. Déclencher des malentendus sur les fichiers

    # Lorsqu'on lui demande la configuration DANS le fichier de déclenchement

    # if "trigger" dans texte et ("konfigurier" dans texte ou "schreib" in text or "inhalt" in text or "make update" in text):
    #     return (
    #         "Die Datei '.sl5_record.trigger' est un pur Fichier de contrôle (Basculer). "
    #         "Erstellen = Aufnahme Start/Stop. "
    #         "Konfigurationen gehören ausschließlich nach 'config/'."
    #     )

    return None


def execute(match_data):
    # play_cache_hit_sound()


    secDauerSeitExecFunctionStart(reset=True)  # <--- Startschuss!

    utils.SESSION_COUNT += 1

    global GLOBAL_NORMALIZED_KEY

    # 1. CALCULER LA CLÉ CANONIQUE UNE FOIS


    try:
        match_obj = match_data['regex_match_obj']

        # --- CORRIGER LE DÉMARRAGE ---

        # Au lieu de vérifier match_obj.lastindex (qui manque dans le mock),

        # vérifions simplement la longueur du tuple groups().

        # Cela fonctionne en Python concernant ET dans les objets fictifs.

        groups = match_obj.groups()

        user_input_raw = (match_obj.group(2) if len(groups) >= 2 else
                          match_obj.group(1) if len(groups) >= 1 else
                          match_obj.group(0)).strip()
        user_input_raw = user_input_raw.lower()

        # utils.log_debug(f"⏱️{secDurationSinceExecFunctionStart()}s")

        # utils.log_debug(f"Entrée : {user_input_raw}:'{user_input_raw}'")


        if not user_input_raw: return "Nichts gehört."

        GLOBAL_NORMALIZED_KEY = normalizer.create_ultimate_cache_key(user_input_raw)
        hash_of_normalized_key = cache_core.prompt_key_to_hash(GLOBAL_NORMALIZED_KEY)

        # utils.log_debug(f"GLOBAL_NORMALIZED_KEY : {GLOBAL_NORMALIZED_KEY}")

        # utils.log_debug(f"hash_of_normalized_key : {hash_of_normalized_key}")


        keywords_str = GLOBAL_NORMALIZED_KEY

        # Détecte immédiatement les bêtises (0,00 s)

        static_reply = check_static_guardrails(user_input_raw)
        if static_reply:
            utils.log_debug(f"🛡️ Guardrail ausgelöst: '{user_input_raw}'")
            return static_reply

        if "vergiss alles" in user_input_raw.lower():
            if utils.MEMORY_FILE.exists():
                try:
                    utils.MEMORY_FILE.unlink()
                except Exception as e:
                    utils.log_debug(f"{e}")
            return "Gedächtnis gelöscht."

        # --- VÉRIFICATION INSTANTANÉE DU MODE ---

        # Si l'utilisateur dit "immédiatement", "rapidement" ou "instantanément",

        # nous recherchons UNIQUEMENT dans la base de données la meilleure correspondance de mot-clé.

        instant_triggers = ["sofort", "schnell", "instant"]
        if any(w in user_input_raw.lower() for w in instant_triggers):
            utils.log_debug("Mode: INSTANT REQUEST")
            instant_response = get_instant_match(user_input_raw)
            if instant_response:
                return instant_response
            else:
                return "Dazu habe ich noch keine schnelle Antwort gespeichert."

        AURA_NORMAL_PROFILE = (
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte normal ausführlich und hilfreich. "
            "Deine Antworten dürfen freundlicher sein und mehr Kontext liefern, aber bleibe präzise. "
            "Du bist NICHT an die EXTREM-Kürze des Tech-Modus gebunden.\n\n"

            "REGELN:\n"
            "1. Sei hilfreich und informativ. Liefere eine komplette Antwort.\n"
            "2. Wenn der Benutzer eine Konfiguration oder Regel erstellen will, antworte wie im Tech-Profil (Dateiname und Code-Block), aber füge eine kurze Erklärung hinzu.\n"
            "3. Bei allgemeinen Fragen antworte in ganzen Sätzen und einem angenehmen Ton.\n\n"

            "SYSTEM-WISSEN:\n"
            "- Du hast Zugriff auf Config und Code-Logik. Siehe Tech-Profil für Details.\n"

            "MUSTER-ANTWORTEN:\n"
            "User: Was ist ein Haus?\n"
            "Aura: Ein Haus ist ein dauerhaftes, überdachtes Bauwerk, das als Unterkunft oder Schutz dient.\n\n"

            "User: Erstelle eine PUNCTUATION-Regel für Stern.\n"
            "Aura: Gerne, hier ist die Regel für Stern:\n"
            "```python\n"
            "# PUNCTUATION-Tupel: (Suchwort, neues Wort)\n"
            "'stern': '*'\n"
            "```\n"
        )

        AURA_TECH_PROFILE = (
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte EXTREM kurz.\n\n"

            "WICHTIGSTE REGELN:\n"
            "1. KEIN 'Meta-Talk' (Keine Einleitungen, kein 'Hier ist der Code').\n"
            "2. Wenn du etwas nicht weißt oder es nicht zu Aura gehört: Sage 'Dazu habe ich keine Infos.' (Nicht leer bleiben!).\n"
            "3. Bei BEFEHLEN (Erstelle Regel): Antworte NUR mit dem Dateinamen und dem Regel-Tupel.\n\n"

            "SYSTEM-WISSEN:\n"
            "- Config: 'config/maps/' (Python-Dateien).\n"
            "- Logik: Regex Listen als Tupel.\n"
            "- Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "- Vosk (Audio) > Maps (PUNCTUATION_MAP.py)  > Maps (...pre.py) > LanguageTool (Opt.) > Maps (...post.py) > Output (Text & TTS).\n"
            "- Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"

            "- Umgebung: Headless (Keine GUI). Offline.\n\n"

            "SYSTEM-WISSEN:\n"
            
            # --- Traitement RegEx (logique descendante et d'arrêt) ---

            "- RegEx-Tupel: (`Name`, `RegEx`, **`Value_Ignored`**, `Flags`)\n" # <--- Klares Label für den IGNORIERTEN WERT
            "- RegEx-Regeln werden strikt **Top-Down** im Code verarbeitet (keine Prioritäts-Sortierung).\n"
            "- WICHTIG: Ein RegEx-Match, der den gesamten Text ersetzt (Full-Match), **stoppt** die weitere Verarbeitung.\n"
            
            # --- Logique floue (seuil) ---

            "- Fuzzy-Tupel: (`Ersetzung`, `Match-Phrase`, **`Threshold`**, ...)\n" # <--- Klares Label für den AKTIVEN WERT
            "- Die **Fuzzy-Suche** (verwendet 'fuzzywuzzy' und 'token_set_ratio') wird nur als **letzter Fallback** ausgeführt, wenn KEINE RegEx gefunden wurde.\n"
            "- Der **`Threshold`** (0-100) im Fuzzy-Tupel ist der Mindest-Score, den das Fuzzy-Matching erreichen muss. Er hat **KEINE** Funktion im RegEx-Tupel.\n"
            
            "MUSTER-ANTWORTEN (Kopiere diesen Stil):\n\n"

            "User: Wo sind die Configs?\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: Erstelle eine PUNCTUATION-Regel für Stern.\n"
            "```python\n"
            "# PUNCTUATION-Tupel: (Suchwort, neues Wort)\n"
            "'stern': '*'\n"
            "```\n\n"

            "User: Erstelle eine Regex-Regel für Kanzlerin.\n"
            "Aura: kanzlerin_map.py\n"
            "```python\n"
            "# Regel-Tupel: (Ersetzung, Regex, Priorität, Flags)\n"
            # EXAMPLE: Chancelier

            "('Angela Merkel', r'^(Chancelier|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "```\n\n"

            "User: Erstelle eine Catch-All Regel.\n"
            "Aura: catch_all.py\n"
            "```python\n"
            # EXAMPLE: Aucun

            "('Ersetzung', r'^.*$', 10, {})\n"
            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: Wiki

            "('Ersetzung', r'^Wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"

        )























        ollama_normal_params = {
            "temperature": 0.3,
            "mirostat": 2,
            "num_predict": 512,  # Wert für gründliche Antworten
        }







        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "zusammenfassung"]
        trigger_readme = ["hilfe", "dokumentation", "readme", "read me", "wie funktioniert", "was kannst du"]
        no_cache_keywords = ["witz", "spruch", "zufall", "random"]

        # --- Initialisation du mode (régler FIXED sur NORMAL) ---

        mode_prefix = "NORMAL"
        system_role = AURA_NORMAL_PROFILE  # Immer den Normal-Prompt verwenden
        ollama_params = ollama_normal_params  # Immer die Normal-Params verwenden
        use_history = True  # History beibehalten, da es Kontext ist


        context_data = ""
        input_lower = user_input_raw.lower()
        bypass_cache = True
        context_prefix = ""


        # --- DÉTECTION DE MODE ET CHARGEMENT DE CONTEXTE ---

        # Ici, nous déterminons uniquement : quel mode est actif ? Quel contexte est chargé ?


        # utils.log_debug(f"Entrée : {user_input_raw}:'{user_input_raw}'")

        # utils.log_debug(f"Entrée : {input_lower}:'{input_lower}'")


        if any(w in input_lower for w in no_cache_keywords):
            bypass_cache = True
            utils.log_debug("Cache BYPASS: Zufallswort erkannt.")

        # 1. VÉRIFICATION DU PRESSE-papierS

        elif any(w in input_lower for w in trigger_clipboard):
            utils.log_debug("Mode: CLIPBOARD")
            content = get_clipboard_content()
            if content:
                # content_preview = content[:50] + str(len(content))
                # Le hachage du contenu devient une partie du préfixe -> modifications du contenu = modifications du cache

                # clip_hash = hashlib.md5(content_preview.encode()).hexdigest()
                # mode_prefix = f"CLIP_{clip_hash}"

                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                system_role = "Du bist ein Assistent. Analysiere die Daten."
                use_history = False
            else:
                return "Zwischenablage ist leer."

        # 2. VÉRIFICATION DU LISEZMOI

        elif any(w in input_lower for w in trigger_readme):
            utils.log_debug("Mode: README")
            readme_content = get_readme_content()
            if readme_content:
                # Le hachage du fichier Lisez-moi devient une partie du préfixe -> modifications de la documentation = modifications du cache

                readme_hash = hashlib.md5(readme_content.encode()).hexdigest()
                mode_prefix = f"README_{readme_hash}"

                context_data = f"\nPROJEKT DOKUMENTATION:\n'''{readme_content}'''\n"
                system_role = (f"Support-Bot für 'SL5 Aura'. Fakten:\n{AURA_TECH_PROFILE}\nErfinde nichts.")
                use_history = False
            else:
                return "Readme nicht gefunden."

        # 3. PAR DÉFAUT (le repli est "STD" comme initialisé ci-dessus)


        # --- CALCUL DE HACHAGE ---


        # 1. Générez TOUJOURS des mots-clés immédiatement (pour la clé de cache ET le stockage de base de données)

        # Cela rend le cache "flou" -> "Créer une règle" et "Créer une règle" se retrouvent dans le même cache !


        # utils.log_debug(f"Mots-clés<execute 🔎 {keywords_str} 🔍")


        # Solution de secours : si aucun mot-clé n'a été trouvé (par exemple uniquement des mots de remplissage), utilisez le texte brut

        if not keywords_str:
            base_for_hash = user_input_raw
        else:
            base_for_hash = keywords_str

        # 2. Construisez la chaîne de hachage

        if "CLIP" in mode_prefix or "README" in mode_prefix:
            # Avec Clipboard/Readme, le contenu (préfixe) doit faire partie du hachage

            hash_input_string = f"{mode_prefix}|{base_for_hash}"
        else:
            # En mode standard, seul le jeu de mots-clés compte

            # Question : "Aura, combien de temps" -> Clé : "STD|tard"

            # Question : « Quelle heure est-il » -> Clé : « HEURES|tard » -> HIT !

            hash_input_string = f"STD|{base_for_hash}"

        context_prefix = context_prefix if 'context_prefix' in locals() else ""
        hash_input_string = f"{mode_prefix}|{context_prefix}|{base_for_hash}"

        # utils.log_debug(f"🔑 base_for_hash : '{base_for_hash}'")

        # utils.log_debug(f"🔑 hash_input_string : '{hash_input_string}'")


        # Invite complète pour l'IA (reste telle qu'elle était, pour le contexte)

        full_prompt_for_generation = f"{system_role}\n{context_data}\nUser: {user_input_raw}\nAura:"
        if use_history:
            hist = load_history()
            full_prompt_for_generation = f"{system_role}\nVerlauf: {json.dumps(hist)}\n{context_data}\nUser: {user_input_raw}\nAura:"

        # --- VÉRIFICATION DU CACHE ---


            # --- GÉNÉRATION D'IA (API OLLAMA) ---

        # utils.log_debug("Cache MISS. Envoi d'une requête API à Ollama...")


            # --- GÉNÉRATION D'IA (API OLLAMA) ---

            utils.log_debug("Cache BYPASS (Slow Mode). Sende API-Request an Ollama…")

        payload = {
            "model": "llama3.2:latest",
            "prompt": full_prompt_for_generation,
            "stream": False,
            "options": ollama_params
        }


        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(OLLAMA_API_URL, data=data, headers={'Content-Type': 'application/json'})

            # Délai d'attente augmenté à 120 s pour des raisons de sécurité

            with urllib.request.urlopen(req, timeout=120) as response:
                api_response = json.loads(response.read().decode('utf-8'))

            utils.SUM_PER_CACHE = (utils.SESSION_CACHE_HITS / utils.SESSION_COUNT) if utils.SESSION_COUNT > 0 else 0
            sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
            utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()

            session_sec_average = utils.SESSION_SEC_SUM / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0

            utils.log_debug(
                f"Nr. {utils.SESSION_COUNT} | CACHE_HITS:{utils.SESSION_CACHE_HITS} 📊 CacheHITs/Nr.: {sum_per_cache_str} | "
                f"⌚ Gespart: ~{session_sec_average * utils.SESSION_CACHE_HITS:.1f}s")

            raw_text = api_response.get("response", "")

            answer_for_all_fallback = (
                "Aura Status: Offline-System, Single-User (Keine Logins/Accounts).\n"
                "Pfade: Configs in 'config/', Regeln in 'config/maps/'.\n\n"

                "FORMAT 1: Einfache Ersetzung (z.B. PUNCTUATION_MAP)\n"
                "Synatx: 'Wort': 'Ersatz'\n"
                "Beispiel: 'stern': '*'\n\n"

                "FORMAT 2: Logik-Regeln (z.B. FUZZY_MAP)\n"
                "Syntax: (Name, Regex, Prio, Flags)\n"
                # EXAMPLE: Chancelier

                "Beispiel: ('Merkel', r'^(Chancelier|Angie)$', 100, {'flags': re.IGNORECASE})\n"
                # EXAMPLE: Wiki

                "Beispiel: ('Wiki', r'^Wiki (.*)$', 50, {'on_match_exec': 'wiki_search'})\n\n"

                "Doku: https://SL5.de/Aura"
            )

            if not raw_text:
                response = answer_for_all_fallback

            response = clean_text_for_typing(raw_text)

            response.replace('sl5_config.py', ' settings_local.py ')
            response.replace(' sl5_record_trigger.py ', ' /tmp/sl5_record.trigger ')

            response = response.replace('JSON', 'Python')
            response = response.replace('YAML', 'Python')
            response = response.replace('json', 'Python')
            response = response.replace('Aurah ', 'Aura ')
            response = response.replace('config/maps/Ordner', 'config/maps Ordner')

            # je n'ai aucune information à ce sujet

            if 'Dazu habe ich keine Info' in response or 'sl5_record_trigger.py' in response:
                response = answer_for_all_fallback

            if (False  # noqa: E129
                or "r'/tmp" in response # noqa: E127
                or 'user_map.py' in response # noqa: E127
                or 'user_regeln.py' in response): # noqa: E127 E129
                response = answer_for_all_fallback # noqa: E127

            if 'Fehler:' in response or '.json' in response:
                response = answer_for_all_fallback

            # --- SAUVEGARDER ---

            if not bypass_cache:
                # utils.log_debug(f"bypass_cache : {bypass_cache}")

                # IMPORTANT : Nous utilisons ici la même hash_input_string (en fonction de mots-clés),

                # que nous avons utilisé pour lire ci-dessus !

                # cache_response(hash_input_string, réponse, user_input_raw, mots-clés=keywords_str)


                cache_core.cache_response(
                    tag_keyword=hash_input_string,
                    response_text=response,
                    clean_user_input=user_input_raw,
                    hash_of_normalized_key=hash_of_normalized_key
                )

            if use_history:
                save_to_history(user_input_raw, response)

            return response


        # --- TRAITEMENT DES ERREURS ---

        except HTTPError as e:
            # Ici, nous interceptons la « Réponse du serveur : 500 ».

            if e.code == 500:
                utils.log_debug("❌ OLLAMA SERVER ERROR (500). Ignoriere Fehlertext für User.")
                # Si vous ne voulez PAS que l'utilisateur voie l'erreur :

                return "Ich habe kurz den Faden verloren. Kannst du das wiederholen?"
            else:
                utils.log_debug(f"API HTTP Error: {e.code}")
                return f"Server Fehler: {e.code}"

        except URLError as e:
            # Si Ollama ne fonctionne pas du tout (Connexion refusée)

            utils.log_debug(f"API Connection Error: {e.reason}")
            return "Fehler: Keine Verbindung zu Ollama."

        except Exception as e:
            # Toutes les autres erreurs

            utils.log_debug(f"API General Error: {e}")
            # return "Une erreur interne s'est produite."

            return (
                "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
                "Es gibt keine Logins, Accounts. "
                "Du bist der einzige Nutzer (Besitzer des Geräts). "
                "Bitte lese Details in der Dokumentation: https://SL5.de/Aura"
            )







    except Exception as e:
        utils.log_debug(f"API Error: {e}")
        return f"Interner Fehler: {e!s}"







