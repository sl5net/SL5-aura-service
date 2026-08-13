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

from scripts.py.func.get_project_root import get_aura_project_root
import logging
import os

if __name__ == "__main__":

    import sys
    from pathlib import Path

    # 1. Obtenga SL5NET_AURA_PROJECT_ROOT usando la lógica específica de su proyecto

    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

    # 2. Defina la ruta al directorio de este complemento.

    PLUGIN_DIR = SL5NET_AURA_PROJECT_ROOT / "config" / "maps" / "plugins" / "z_fallback_llm" / "de-DE"

    # 3. Agregue PLUGIN_DIR a sys.path para permitir importaciones absolutas de módulos hermanos

    if str(PLUGIN_DIR) not in sys.path:
        sys.path.insert(0, str(PLUGIN_DIR))


    # Registro de configuración

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("embedding_migration")

    # Configuración (Ajuste las rutas si es necesario)

    # DB_FILE = "aura_cache.db" # Reemplace con su ruta de base de datos real desde las utilidades


    import os
    from pathlib import Path

    import pickle
    import sqlite3

    from sentence_transformers import SentenceTransformer


    DB_FILE = str(PLUGIN_DIR / "llm_cache.db")

    MODEL_NAME = 'all-MiniLM-L6-v2'

    def migrate_database():
        """
        Backfills missing embeddings for existing prompts in the database.
        This allows legacy data to be searchable via semantic search.
        """
        if not Path(DB_FILE).exists():
            logger.error(f"Database file {DB_FILE} not found!")
            return

        logger.info(f"Loading model: {MODEL_NAME}…")
        model = SentenceTransformer(MODEL_NAME)

        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # 1. Asegúrese de que la columna exista (comprobación de seguridad)

            try:
                cursor.execute("ALTER TABLE prompts ADD COLUMN embedding BLOB")
                logger.info("Added 'embedding' column to 'prompts' table.")
            except sqlite3.OperationalError:
                logger.info("'embedding' column already exists.")

            # 2. Busque todas las filas donde falta la incrustación

            cursor.execute("SELECT hash, prompt_text FROM prompts WHERE embedding IS NULL")
            rows = cursor.fetchall()

            if not rows:
                logger.info("No rows found that require migration.")
                return

            logger.info(f"Starting migration for {len(rows)} rows…")

            for i, (prompt_hash, prompt_text) in enumerate(rows):
                # Generar incrustación

                embedding = model.encode(prompt_text)
                # Serializar a BLOB binario

                embedding_blob = pickle.dumps(embedding)

                # Actualizar la base de datos

                cursor.execute(
                    "UPDATE prompts SET embedding = ? WHERE hash = ?",
                    (embedding_blob, prompt_hash)
                )

                if (i + 1) % 10 == 0:
                    logger.info(f"Progress: {i + 1}/{len(rows)} rows processed.")

            conn.commit()
            logger.info("Migration completed successfully!")

        except Exception as e:
            logger.error(f"Migration failed: {e}")
        finally:
            if conn:
                conn.close()

    migrate_database()

else:
    pass
