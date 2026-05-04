import logging
import os
import sys
from pathlib import Path

# 1. Get PROJECT_ROOT using your project's specific logic
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

# 2. Define the path to this plugin's directory
PLUGIN_DIR = PROJECT_ROOT / "config" / "maps" / "plugins" / "z_fallback_llm" / "de-DE"

# 3. Add PLUGIN_DIR to sys.path to allow absolute imports of sibling modules
if str(PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGIN_DIR))


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("embedding_migration")

# Configuration (Adjust paths if necessary)
# DB_FILE = "aura_cache.db" # Replace with your actual DB path from utils

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

    logger.info(f"Loading model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 1. Ensure the column exists (Safety check)
        try:
            cursor.execute("ALTER TABLE prompts ADD COLUMN embedding BLOB")
            logger.info("Added 'embedding' column to 'prompts' table.")
        except sqlite3.OperationalError:
            logger.info("'embedding' column already exists.")

        # 2. Fetch all rows where embedding is missing
        cursor.execute("SELECT hash, prompt_text FROM prompts WHERE embedding IS NULL")
        rows = cursor.fetchall()

        if not rows:
            logger.info("No rows found that require migration.")
            return

        logger.info(f"Starting migration for {len(rows)} rows...")

        for i, (prompt_hash, prompt_text) in enumerate(rows):
            # Generate embedding
            embedding = model.encode(prompt_text)
            # Serialize to binary BLOB
            embedding_blob = pickle.dumps(embedding)

            # Update the database
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

if __name__ == "__main__":
    migrate_database()
