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

# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py

# Ask_ollama.py

import datetime
import os

# importer une torche


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

# à partir de sentence_transformers importer SentenceTransformer, util



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



# def extreme_standardize_prompt_text(texte) :

# global STOP_WORDS_DE_EXTREME

#
# # Initialiser le stemmer allemand

# stemmer = AllemandStemmer()

#
#
# #1. Tout en minuscules

# texte = texte.inférieur()

#
# #2. Remplacez TOUS les nombres, heures et symboles monétaires par des caractères génériques

# text = re.sub(r'\d+([.,]\d+)?', ' [NUMBER] ', text) # Par ex. '10', '10,5'

# texte = re.sub(r'[€$£%]', ' ', texte)

#
# #3. Suppression radicale de presque tous les caractères spéciaux et signes de ponctuation

# texte = re.sub(r'[^a-zäöüß\s]', ' ', texte)

#
# #4. Réduisez les espaces à un seul espace et coupez-les

# texte = re.sub(r'\s+', ' ', text).strip()

#
# #5. Tokenisation (séparation des mots)

# mots = text.split()

#
# #6. Arrêter la suppression et la racine des mots

# mots_tiges = []

# pour mot en mots :

# si le mot n'est pas dans STOP_WORDS_DE_EXTREME :

# # Réduisez le mot à sa racine (stemming)

# stemmed_words.append(stemmer.stem(mot))

#
# #7. Réassembler les mots en une chaîne

# texte = ' '.join(stemmed_words)

#
# utils.log_debug(f"keywords<lastLine<extreme_standardize_prompt_text : 🔎 {text.strip()} 🔍")

#
# retourner texte.strip()



# --- Exemple de test ---

# Question 1 : « Combien de maisons devons-nous choisir dans la région ? »

# Raconté : "nous avons le choix de l'espace dans la maison"

# Racine extrême : "wiel haus hab area wahl" (après la suppression du mot vide)


# Invite 2 : « La maison est chère, mais très agréable. »

# Extreme Stemmed : "maison chère et belle"


# Question 3 : « Combien de maisons y a-t-il dans la région ? »

# Extreme Stemmed : « quelle superficie de la maison »


# 1. Charger le modèle (localement, environ 80 Mo, très rapide)

# « all-MiniLM-L6-v2 » est la norme industrielle pour les recherches locales rapides

# modèle = SentenceTransformer('all-MiniLM-L6-v2')


_model = None  # Globaler Cache für das Modell

def get_embedding_model():
    """
    Lazy loader for the embedding model.
    Only loads torch and the model into RAM when actually needed.
    """
    # global _model
    # if _model is None:
    #     utils.log_debug("🚀 Loading Embedding Model (Lazy Load)…")
    #     from sentence_transformers import SentenceTransformer
    #     _model = SentenceTransformer('all-MiniLM-L6-v2')
    # return _model


# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py:153


log = logging.getLogger("simulate_conversation")
GITHUB_BASE = "https://github.com/sl5net/SL5-aura-service/blob/master"

def get_github_url(file_path):
    """Erstellt den passenden GitHub-Link aus dem lokalen Pfad."""
    rel_path = ""
    if "STT/" in str(file_path):
        rel_path = str(file_path).split("STT/")[1]
    elif "SL5-aura-service/" in str(file_path):
        rel_path = str(file_path).split("SL5-aura-service/")[1]
    if rel_path:
        url = f"{GITHUB_BASE}/{rel_path}"
        log.debug(f"get_github_url: {file_path} -> {url}")
        return url
    log.warning(f"get_github_url: kein STT/ oder SL5-aura-service/ in Pfad: {file_path}")
    return None


def save_to_aura_db(question, answer, file_path, use_semantics=False):
    """
    Version 1.2.0: Saves dialogue pairs including a semantic vector embedding.
    Enables the 'Self-Learning' loop for the interactive chat.
    """
    prompt_hash = hashlib.md5(question.encode('utf-8')).hexdigest()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    clean_input = question.lower().replace("?", "").strip()

    embedding_blob = None
    if use_semantics: # Nur für den interaktiven Chat aktivieren
        import pickle
        model = get_embedding_model()
        embedding = model.encode(question)
        embedding_blob = pickle.dumps(embedding)

    github_link = get_github_url(file_path)

    try:
        # conn = sqlite3.connect(DB_PATH)

        conn = sqlite3.connect(utils.DB_FILE, timeout=90)
        conn.execute("PRAGMA journal_mode=WAL;")

        cursor = conn.cursor()

        # 1. Enregistrez dans les « invites » - incluant désormais l'EMBEDDING

        cursor.execute("""
            INSERT OR IGNORE INTO prompts (hash, prompt_text, last_used, clean_input, keywords, embedding)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (prompt_hash, question, now, clean_input, "radio_deep_dive", embedding_blob))

        # 2. Enregistrer dans « Réponses »

        cursor.execute("""
            INSERT INTO responses (prompt_hash, response_text, created_at, usage_count, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_hash, answer, now, 0, github_link))

        # 3. Mettre à jour le tableau de suivi

        current_mtime = os.path.getmtime(file_path)
        cursor.execute("""
            INSERT OR REPLACE INTO radio_processed_files (file_path, last_mtime, last_generated)
            VALUES (?, ?, ?)
        """, (str(file_path), current_mtime, now))

        conn.commit()
        conn.close()
        # utils.log_debug(f"✅ Enregistré (y compris le vecteur) : {question[:30]}…")

    except Exception as e:
        print(f"Database Error: {e}")


def get_semantic_match(user_text):
    # 1. Encodez une fois l'entrée de l'utilisateur


    # from sentence_transformers import util
    # model = get_embedding_model()
    # user_embedding = model.encode(user_text, convert_to_tensor=True)
    try:
        conn = sqlite3.connect(utils.DB_FILE, timeout=90)
        c = conn.cursor()
        # 2. Récupérer les intégrations PRÉ-CALCULÉES (BLOB)

        c.execute("SELECT hash, embedding FROM prompts WHERE embedding IS NOT NULL")
        rows = c.fetchall()
        best_hash, max_sim = None, 0.0

        SEMANTIC_THRESHOLD = 0.7  # Live-Betrieb
        # SEUIL SÉMANTIQUE = -1,0 # Le test correspond toujours


        for db_hash, blob in rows:
            # 3. Chargez le vecteur depuis BLOB (pas de model.encode ici !)

            pass
            # db_embedding = torch.from_numpy(pickle.loads(blob)).to(user_embedding.device)
            # db_embedding = model.encode(user_text, convert_to_tensor=True)


            # similarity = util.cos_sim(user_embedding, db_embedding).item()

            # if similarity > max_sim:
            #     max_sim, best_hash = similarity, db_hash
        if best_hash and max_sim > SEMANTIC_THRESHOLD:
            c.execute("SELECT response_text FROM responses WHERE prompt_hash=? LIMIT 1", (best_hash,))
            res = c.fetchone()

            conn.close()

            if res:
                utils.play_cache_hit_sound()
                return res[0]
        return None
    except Exception as e:
        utils.log_debug(f"Semantic Error: {e}")
        return None


# def get_semantic_match_22222 (user_text) :

# """

# Effectue une recherche sémantique de la meilleure réponse correspondante.

# Utilise la similarité cosinus pour trouver des correspondances même sans chevauchements exacts de mots clés.

# """

# # utils.init_db()

#
# # Convertir l'entrée de l'utilisateur en une intégration vectorielle

# user_embedding = model.encode(user_text, convert_to_tensor=True)

#
# try:

# conn = sqlite3.connect(utils.DB_FILE)

# c = conn.curseur()

# # Récupérer les intégrations pré-calculées à partir de la base de données

# c.execute("SELECT hash, prompt_text FROM invites")

# lignes = c.fetchall()

#
# utils.log_debug(f"DEBUG : la recherche sémantique a chargé les intégrations {len(rows)} à partir de {utils.DB_FILE}")

#
# best_hash = Aucun

# max_similarité = 0,0

# seuil = 0,3

# seuil = -1,0

#
# pour une ligne en lignes :

# db_hash, db_text = ligne[0], ligne[1]

#
# # Calculer la similarité sémantique

# db_embedding = model.encode(db_text, convert_to_tensor=True)

# similarité = util.cos_sim(user_embedding, db_embedding).item()

#
# si similarité > max_similarity :

# max_similarity = similarité

# meilleur_hash = db_hash

#
# si best_hash et max_similarity > seuil :

# utils.log_debug(f"🧠 Correspondance sémantique ! Score : {max_similarity:.2f}")

#
# utils.log_debug(f"🚀 Correspondance instantanée trouvée ! (Hash : {best_hash[:8]})")

#
# c.exécuter(

# "SELECT réponse_texte FROM réponses WHERE prompt_hash=? ORDER BY note DESC, créé_à DESC LIMIT 1",

# (meilleur_hash,))

# resp_row = c.fetchone()

# conn.close()

#
# si resp_row :

# utils.play_cache_hit_sound()

# # return f"[MODE IMMÉDIATE] : {resp_row[0]}"

# retourner f"{resp_row[0]}"

#
# retourner db_text

#
# retourner Aucun

# sauf exception comme e :

# utils.log_debug(f"Erreur sémantique : {e}")

# retourner Aucun


# --- CORRESPONDANCE INSTANTANÉE ---

def get_instant_match(user_text):
    """
    Sucht in der DB nach Keywords, die dem User-Text am ähnlichsten sind.
    Nutzt Python Set-Intersection (Schnittmenge) statt LLM.
    """
    # utils.init_db()


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


# Ask_ollama.py



# def get_professional_keywords(texte) :

# retourner extreme_standardize_prompt_text(texte)

#
# """

# Approche hybride : filtrez d’abord les déchets, puis déterminez les mots-clés.

# """

# #1. Liste de mots vides hardcore pour les commandes vocales

# # ignore_words = {

# # "aura", "ordinateur", "pc", "système", "bonjour", "hé", "s'il vous plaît", "merci",

# # "créer", "faire", "faire", "faire", "générer", "afficher", "afficher",

# # "un", "un", "un", "le", "le", "cela", "et", "ou", "avec",

# # "rules", "rule", "text", "string" # Souvent des mots de remplissage dans votre contexte

# # }

#
#
# synonymes = {

# # commandes

# "create": "nouveau", "create": "nouveau", "generate": "nouveau", "make": "nouveau",

# "make": "nouveau", "write": "nouveau", "add": "nouveau", "nouveau": "nouveau",

# # Infos

# "show": "info", "show": "info", "where": "info", "how": "info", "help": "info", "explain": "info",

# # Supprimer

# "delete": "supprimer", "supprimer": "supprimer", "oublier": "supprimer",

# # Contexte

# "config": "config", "configuration": "config", "settings": "config",

# "regex": "règle", "règles": "règle", "modèle": "règle"

# }

#
# ignore_words = {

# "aura", "ordinateur", "pc", "système", "bonjour", "hé", "salut",

# "s'il vous plaît", "merci", "temps", "juste", "rapidement", "sous peu",

# "un", "un", "un", "un", "un",

# "le", "le", "cela", "dem", "den",

# "et", "ou", "avec", "de", "dans", "dans", "à", "pour", "sur", "pour",

# "est", "sont", "était", "serait", "peut", "vous", "moi", "et", "je"

# }

#
# try:

# # Nettoyer le texte

# mots = re.findall(r'\w+', text.lower())

#
# jetons_finals = []

# pour w en mots :

# #1. Ignorer?

# si w dans ignore_words :

# continuer

#
# #2. Remplacer le synonyme ?

# si w dans les synonymes :

# final_tokens.append(synonymes[w])

# autre:

# #3. Tenez parole

# final_tokens.append(w)

#
# sinon final_tokens :

# retour ""

#
# # 4. Trier : "Lumière allumée" et "On lumière" deviennent identiques ("on light")

# # final_kws = trié(liste(set(final_tokens)))

# # return " ".join(final_kws)

#
#
#
#
#
# pertinent_words = [w pour w dans final_tokens si w pas dans ignore_words et len(w) > 2]

# clean_text = " ".join(mots_pertinents)

#
# sinon clean_text :

# return "" # Pas de mots-clés (mieux que des ordures)

#
# # Essayez YAKE sur le texte nettoyé

# importer du yake

# kw_extractor = yake.KeywordExtractor(lan="de", n=1, dedupLim=0.9, top=3)

# mots-clés = kw_extractor.extract_keywords(clean_text)

#
# # Renvoie la liste triée

# final_kws = trié([k[0].lower() pour k dans les mots-clés])

# retourner " ".join (final_kws)

#
# sauf ImportError :

# # Repli sans YAKE

# return " ".join(sorted(list(set(relevant_words))))

# sauf exception :

# retour ""



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
        readme_path = Path(__file__).parent / "README_AI-delang.md"
        if readme_path.exists():
            return readme_path.read_text(encoding='utf-8').strip()[:6000]

        hint = (
            "README_AI-delang.md nicht gefunden.\n"
            "Bitte erstelle sie mit einer großen AI (z.B. Claude/GPT) und folgendem Prompt:\n\n"
            "---\n"
            "Lies die Datei README.md dieses Projekts und erstelle daraus eine kompakte\n"
            "Version für ein lokales Ollama-Modell (llama3.2, 3B Parameter).\n"
            "Anforderungen:\n"
            "- Max 2000 Zeichen\n"
            "- Kein Markdown, nur Fließtext\n"
            "- Fakten: Python, Regeln als Tupel in FUZZY_MAP_pre.py,\n"
            "  Pipeline: Vosk → PUNCTUATION_MAP → FUZZY_MAP_pre → LanguageTool → FUZZY_MAP\n"
            "- Trigger: /tmp/sl5_record.trigger\n"
            "- Kein GUI, kein JSON, kein YAML\n"
            "- Sprache: Deutsch, technisch, direkt\n"
            "Speichern als README_AI-delang.md\n"
            f"Speichern als: {readme_path}"
            "---"
        )
        print(hint)
        log.info(hint)

        return None
    except Exception:
        return None
        # utils.log_debug(f"get readme Error: {e}")



def get_clipboard_content():
    if not utils.BRIDGE_FILE.exists(): return None
    try:
        content = utils.BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content:
            return content
        return None
    except Exception:
        return None


def load_history():
    if not utils.MEMORY_FILE.exists(): return []
    try:
        with open(utils.MEMORY_FILE, 'r', codage='utf-8') as f:
            return json.load(f)
    except Exception:
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
    except Exception:
        pass


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
    print("\n--- DEBUG START 28.4.'26 21:31 Tue ---")

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

        # user_input_raw = (match_obj.group(2) si len(groups) >= 2 sinon

        # match_obj.group(1) si len(groups) >= 1 sinon

        # match_obj.group(0)).strip()


        # prends toujours le dernier groupe

        user_input_raw = groups[-1].strip() if groups else match_obj.group(0).strip()
        user_input_raw = user_input_raw.lower()

        utils.log_debug(f"⏱️{secDauerSeitExecFunctionStart()}s")
        utils.log_debug(f"Input: {user_input_raw}:'{user_input_raw}'")

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
                except Exception:
                    pass
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

        # --- PROFIL TECH AURA (base et faits) ---

        # --- PROFIL TECH AURA (base et faits) ---

        AURA_TECH_PROFILE_2911252235Sat = (  # noqa: F841
            "Du bist SL5 Aura. Antworte auf Deutsch. Sei extrem kurz.\n"

            "ANWEISUNG FÜR DICH:\n"
            "Unterscheide selbstständig:\n"
            "1. WISSENSFRAGE (Wo/Was/Wie) -> Nur den Fakt nennen (1 Satz).\n"
            "2. HANDLUNG (Erstelle/Schreibe) -> Nur Dateiname und Code-Block.\n\n"

            "BEISPIELE (Nutze diesen Stil):\n"
            "User: 'Wo sind die Configs?'\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: 'Wie starte ich die Aufnahme?'\n"
            "Aura: Durch Erstellen der Datei '/tmp/sl5_record.trigger'.\n\n"

            "SYSTEM-FAKTEN (Strict Grounding):\n"
            "About: Privacy-first voice assistant framework. Core is offline. Scripts allow hybrid usage.\n"
            "1. Tech Stack: Python (87%), Shell (9%), PowerShell (2%), Vosk (Offline-Modelle ~4GB), LanguageTool. KEIN Java/C++, KEINE .exe, KEIN PDF-Support.\n"
            "2. Interface: 100% 'Headless' Hintergrund-Dienst. Interaktion NUR via Mikrofon (Input) & Terminal-Logs (Output). ES GIBT KEINE 'OBERFLÄCHE', KEINE GUI, KEIN Web-UI.\n"
            "3. Logik & Config: KEIN JSON/YAML! Regeln sind reine Python-Dateien (z.B. 'FUZZY_MAP_pre.py') mit Regex-Listen.\n"
            "   - In config/ befinden sich alle KONFIGURATION .\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer) oder spezifisch `^meinBefehl$`. (KEIN Button, reiner Code!)\n"
            "   - Syntax WICHTIG: Nutze Python 're' Syntax. Für Alternativen (ODER) nutze zwingend '|' ohne Leerzeichen!\n"
            "     FALSCH: `(Hans Max Luis)` -> RICHTIG: `(Hans|Max|Luis)`\n"
            "     FALSCH: `[Licht Lampe]`   -> RICHTIG: `(Licht|Lampe)`\n"
            "   - Lade-Reihenfolge: Plugin-ORDNER werden alphabetisch geladen (A-Z).\n"
            "   - Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "   - Stopp (Full-Match): Die Pipeline stoppt, wenn ein Regex von Anfang (`^`) bis Ende (`$`) matcht. Da Voice-Input einzeilig ist, sind Anker wichtig.\n"
            "   - In config/ befinden sich alle KONFIGURATIONEN.\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer). \n"
            # EXAMPLE: Chancelier

            "   Beispiel Regel-Tupel: ('Angela Merkel', r'^(Chancelier|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "4. Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"
            "   - Beispiele: Offline-Wikipedia, SQLite-Booksearch, Ollama AI (Lokal).\n"
            "   - Ausnahme: Das 'Translate'-Plugin nutzt Online-APIs (mit lokalem Cache), benötigt also Internet.\n"
            "5. Security & Tools: \n"
            "   - Dateisuche: NUR via 'git ls-files | fzf'.\n"
            "   - Findet Aura eine versteckte '. Dateiname .py'(Punkt am Anfang), nutzt es deren Passwort zum Entpacken von _ einName .zip (OPTIONAL, nicht vorhanden).\n"
            "6. OS: Linux, Windows, macOS. (Kein Smartphone).\n"
            "7. Installation: Dauert ca. 10-20 Minuten (Download großer Sprachmodelle, >4GB). Updates sind schnell, Erst-Installation NICHT.\n"
            "   - App-Update: Via 'git pull' (Sekunden).\n"
            "   - Modell-Update: Lösche den entsprechenden Ordner in 'models/' und starte das Setup-Skript erneut. (Dauert 10-20 Min, >4GB Download).\n"
            "8. Externe Trigger (CopyQ, AutoKey, AHK): Steuerung erfolgt NUR durch Erstellen einer leeren Datei (File-Watch). KEINE API, KEINE Config!\n"
            "   - Pfad Linux/Mac: `/tmp/sl5_record.trigger`\n"
            "   - Pfad Windows: `c:\\tmp\\sl5_record.trigger`\n"
            "   - Funktion: Datei erstellen = Aufnahme/Verarbeitung starten.\n"
            "9. Verhalten: Erfinde KEINE visuellen Elemente. Fasse dich EXTREM kurz (Max 15 Wörter)."

            "BEISPIEL-DIALOGE (Lerne die Unterscheidung!):\n"
            "User: 'Wo finde ich die Konfiguration?'\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/'.\n\n"

            "User: 'Welche Datei startet die Aufnahme in Linux?'\n"
            "Aura: Das Erstellen der Datei '/tmp/sl5_record.trigger' commence le Enregistrement  dans Linux .\n\n"

            "BEISPIEL-INTERAKTION (Folge diesem Format strikt!):\n"
            "User: 'Erstelle Regeln für Licht.'\n"
            "Aura: Erstelle 'licht_control.py' in 'config/maps/':\n"
        )

        AURA_TECH_PROFILE_2911252311Sat_8sec_superFast = (  # noqa: F841
            "Du bist SL5 Aura, ein Offline-Sprachassistent.\n"
            "Deine Aufgabe: Technischer Support. Antworte EXTREM kurz.\n\n"

            "STRIKTE REGELN:\n"
            "1. Aura nutzt NUR Python-Dateien (.py) und Tupel.\n"
            "2. Wenn der User nach YAML, JSON oder Importen fragt: IGNORIERE ES.\n"
            "3. Schreibe KEINEN Programm-Logik-Code (Kein 'with open', kein 'import', kein 'def').\n"

            "- KEIN 'Meta-Talk' (Kein: 'Du hast gefragt...', Kein: 'Hier ist der Code').\n"
            "- KEINE Höflichkeitsfloskeln.\n"
            "- Wenn Code gefragt ist: ZUERST Dateiname (snake_case.py), DANN Code-Block.\n"
            "- Wenn Info gefragt ist: Nur den Fakt nennen (Max 1 Satz).\n\n"

            "SYSTEM-WISSEN:\n"
            "1. Config-Ort: 'config/maps/' (Reine Python-Dateien).\n"
            "2. Logik: Regex Listen (Top-Down Pipeline). Nutze Python 're'.\n"
            "3. Trigger: Datei '/tmp/sl5_record.trigger' commence Enregistrement.\n"
            "4. Suche: Nur 'git ls-files'. Keine DB.\n"
            "5. Umgebung: Headless (Keine GUI). Offline (Kein 'requests' Modul nutzen!).\n\n"

            "MUSTER-ANTWORTEN (Kopiere diesen Stil strikt):\n\n"

            "User: Wo liegen die Konfigurationen?\n"
            "Aura: Die Konfigurationen befinden sich als Python-Dateien im Ordner 'config/maps/'.\n\n"

            "User: Wie starte ich die Aufnahme?\n"
            "Aura: Durch Erstellen der Datei '/tmp/sl5_record.trigger'.\n\n"

            "User: Erstelle eine Regel für Bundeskanzlerin.\n"
            # EXAMPLE: Chancelier

            "   Beispiel Regel-Tupel: ('Angela Merkel', r'^(Chancelier|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "User: Erstelle eine Regel für Full-Match.\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer). \n"
            "```"
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
            "Aura: FUZZY_MAP_pre.py\n"
            "('immer Ergebnis', r'^.*$')\n"
            "```python\n"
            # EXAMPLE: Aucun

            "('Ersetzung', r'^.*$')\n"
            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: Wiki

            "('Ersetzung', r'^Wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"

        )

        AURA_TECH_PROFILE_3011250003Sun = (  # noqa: F841
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte kurz & präzise.\n\n"

            "WICHTIGSTE REGELN:\n"
            "1. KEIN 'Meta-Talk'. Antworte direkt mit der Lösung.\n"
            "2. Wenn User nach Regeln fragen: Gib IMMER ein Python-Beispiel (Dateiname + Code).\n"
            "3. DATEINAMEN: Passend zum Thema (z.B. 'config/maps/pdf/de-DE/FUZZY_MAP_pre.py').\n"
            "4. WICHTIG: Regex matcht auf GESPROCHENEN TEXT, nicht auf Dateien!\n"
            # EXAMPLE: fichier de cartes de configuration py

            "   - Falsch: r'configuration/cartes/déposer.py'\n"
            # EXAMPLE: ouvrir le fichier

            "   - Richtig: r'ouvrir déposer (.*)'\n\n"

            "SYSTEM-WISSEN:\n"
            "- Config: 'config/maps/' (Python-Dateien).\n"
            # EXAMPLE: Expression régulière

            "- Logik: Tupel `('Ergebnis-Text', r'Expression régulière', Prio, Flags)`.\n"
            "- Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "- Vosk (Audio) > Maps (FUZZY_MAP_pre.py) > LanguageTool (Opt.) > Maps (FUZZY_MAP.py) > Output (Text & TTS).\n"


            "- Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"

            "- Trigger: '/tmp/sl5_record.trigger' (Commence/Arrêté Enregistrement).\n"
            "- Umgebung: Headless, Offline.\n\n"


            "MUSTER-ANTWORTEN (Kopiere diesen Stil):\n\n"

            "User: Wo sind die Regeln?\n"
            "Aura: In 'config/maps/' als Python-Dateien.\n\n"

            "User: Wo sind die Configs?\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: Erstelle eine Regel für Kanzlerin.\n"
            "Aura: kanzlerin_map.py\n"
            "```python\n"
            "# Regel-Tupel: (Name, Regex, Priorität, Flags)\n"
            # EXAMPLE: Chancelier

            "('Angela Merkel', r'^(Chancelier|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "```\n\n"

            "User: Erstelle eine Catch-All Regel.\n"
            "Aura: config/maps/system/de-DE/FUZZY_MAP_pre.py\n"
            "```python\n"
            # EXAMPLE: Aucun

            "('Kein Treffer', r'^.*$', 10, {})\n"
            "```\n\n"

            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: Wiki

            "('Wiki', r'^Wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"
            "```"
        )

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


        full_match_text = match_obj.group(0).lower()
        slow_triggers = ["slow", "langsam", "genau", "gründlich", "normal"]
        # is_slow_request = any(w dans user_input_raw.lower() pour w dans slow_triggers)

        is_slow_request = any(w in full_match_text for w in slow_triggers)

        if is_slow_request:
            utils.log_debug("Mode: SLOW/DETAILED")
            system_role = AURA_NORMAL_PROFILE  # Der ausführliche Prompt
            ollama_params = {
                "temperature": 0.3,
                "mirostat": 2,
                "num_predict": 512
            }
            bypass_cache = True  # Im Slow-Mode immer frisch generieren
        else:
            system_role = AURA_TECH_PROFILE  # Der extrem kurze Prompt
            ollama_params = {
                "temperature": 0.1,
                "num_predict": 100
            }
            bypass_cache = False  # Normaler Modus nutzt den semantischen Cache

        print("\n--- DEBUG START 28.4.'26 21:31 Tue ---")
        print(f"Raw Input: '{user_input_raw}'")
        print(f"Is Slow Triggered: {is_slow_request}")
        print(f"Selected Profile: {'NORMAL' if is_slow_request else 'TECH'}")






















        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "zusammenfassung"]
        trigger_readme = ["hilfe", "dokumentation", "readme", "read me", "wie funktioniert", "was kannst du"]
        no_cache_keywords = ["witz", "spruch", "zufall", "random"]

        context_data = ""
        mode_prefix = "STD"  # Standard Mode
        system_role = f"{AURA_TECH_PROFILE}"
        use_history = True
        input_lower = user_input_raw.lower()
        bypass_cache = bypass_cache

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
                content_preview = content[:50] + str(len(content))
                # Le hachage du contenu devient une partie du préfixe -> modifications du contenu = modifications du cache

                clip_hash = hashlib.md5(content_preview.encode()).hexdigest()
                mode_prefix = f"CLIP_{clip_hash}"

                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                system_role = "Du bist ein Assistent. Analysiere die Daten."
                use_history = False
                bypass_cache = True

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

        # utils.log_debug(f"🔑 base_for_hash : '{base_for_hash}'")

        # utils.log_debug(f"🔑 hash_input_string : '{hash_input_string}'")


        # Invite complète pour l'IA (reste telle qu'elle était, pour le contexte)

        full_prompt_for_generation = f"{system_role}\n{context_data}\nUser: {user_input_raw}\nAura:"
        if use_history:
            hist = load_history()
            full_prompt_for_generation = f"{system_role}\nVerlauf: {json.dumps(hist)}\n{context_data}\nUser: {user_input_raw}\nAura:"

        # --- VÉRIFICATION DU CACHE ---


        if not bypass_cache:
            # Maintenant, nous recherchons avec le mot-clé hash !

            # utils.log_debug(f"11111 hash_input_string: '{hash_input_string}'") # 'STD|aura_empty_request'

            # utils.log_debug(f"11111 GLOBAL_NORMALIZED_KEY : '{GLOBAL_NORMALIZED_KEY}'") # 'aura_empty_request'

            cached_resp, expired = cache_core.get_cached_response(GLOBAL_NORMALIZED_KEY)

            if cached_resp:
                utils.log_debug(f"cached_resp: {cached_resp}")
                if use_history:
                    save_to_history(user_input_raw, cached_resp)
                    # cible = utils.DB_FILE

                    # save_to_aura_db (user_input_raw, cached_resp, cible)


                utils.SUM_PER_CACHE = utils.SESSION_CACHE_HITS / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0
                sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
                utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()
                utils.SUM_PER_CACHE = utils.SUM_PER_CACHE

                return cached_resp

            # 2. NOUVEAU : Repli sémantique (si la correspondance exacte est manquante/expirée)

            semantic_resp = get_semantic_match(user_input_raw)
            if semantic_resp:
                utils.log_debug("🎯 Semantic Cache Hit!")
                utils.SESSION_CACHE_HITS += 1
                return semantic_resp


            if expired:
                utils.log_debug("♻️ Cache Entry EXPIRED.")

            # --- GÉNÉRATION D'IA (API OLLAMA) ---

        # utils.log_debug("Cache MISS. Envoi d'une requête API à Ollama...")


        payload = {
            "model": "llama3.2",
            "prompt": full_prompt_for_generation,
            "stream": False,
            "keep_alive": 0,
            "options": {
                "temperature": 0.1,
                **ollama_params,
                "top_k": 20,
                "num_predict": 100,
                "stop": ["User:", "Verlauf:", "System:", "Aura:"]
            }
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(OLLAMA_API_URL, data=data, headers={'Content-Type': 'application/json'})

            # Délai d'attente augmenté à 120 s pour des raisons de sécurité

            with urllib.request.urlopen(req, timeout=90) as response:
                api_response = json.loads(response.read().decode('utf-8'))

            utils.SUM_PER_CACHE = (utils.SESSION_CACHE_HITS / utils.SESSION_COUNT) if utils.SESSION_COUNT > 0 else 0
            sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
            utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()

            session_sec_average = utils.SESSION_SEC_SUM / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0

            utils.log_debug(
                f"Nr. {utils.SESSION_COUNT} | CACHE_HITS:{utils.SESSION_CACHE_HITS} 📊 CacheHITs/Nr.: {sum_per_cache_str} | "
                f"⌚ Gespart: ~{session_sec_average * utils.SESSION_CACHE_HITS:.1f}s")

            raw_text = api_response.get("response", "")

            utils.log_debug(f"DEBUG: Unzensierte KI-Antwort: '{raw_text[:200]}...'")


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

            # --- SAVE (Seulement lorsqu'il n'est pas en mode bypass) ---

            if not bypass_cache:
                target = utils.DB_FILE

                # Nous devons nous assurer que save_to_aura_db ne plante pas,

                # si 'target' n'est pas un vrai fichier.

                try:
                    # save_to_aura_db (user_input_raw, réponse, cible)

                    save_to_aura_db(user_input_raw, response, target, use_semantics=True)
                except Exception as e:
                    utils.log_debug(f"Speichern in DB fehlgeschlagen: {e}")

                # Alimenter également le cache classique

                cache_core.cache_response(
                    tag_keyword=hash_input_string,
                    response_text=response,
                    clean_user_input=user_input_raw,
                    hash_of_normalized_key=hash_of_normalized_key,
                )

            # --- HISTORIQUE (Toujours à la fin, si activé) ---

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
            # return "Un événement s'est produit."

            return (
                "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
                "Es gibt keine Logins, Accounts. "
                "Du bist der einzige Nutzer (Besitzer des Geräts). "
                "Bitte lese Details in der Dokumentation: https://SL5.de/Aura"
            )






    # config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py:1252

    except Exception as e:
        utils.log_debug(f"API Error: {e}")
        return f"Interner Fehler: {e!s} (2026-0506-0626)"







