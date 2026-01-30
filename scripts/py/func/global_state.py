# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
import threading

# Lock to protect access to the sequence ID and the out-of-order cache
SEQUENCE_LOCK = threading.Lock()

# The last successfully processed chunk ID. All new output must be this ID + 1.
LAST_PROCESSED_ID = 0

# Cache to store chunks that arrived out of order. Key is the expected ID (int), Value is the chunk data.
OUT_OF_ORDER_CACHE = {}

# A mapping of all active session IDs to their last processed chunk ID.
# This prevents one long session from blocking a subsequent new session.
# Key: Session ID (e.g., thread ID or unique counter), Value: Last processed Chunk ID
SESSION_LAST_PROCESSED = {}

# scripts/py/func/global_state.py:18
SIGNATURE_TIMES = {}

