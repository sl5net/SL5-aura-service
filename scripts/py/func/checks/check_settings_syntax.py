import sys
import logging

logger = logging.getLogger(__name__)

def verify_plugin_notation(plugins_config):
    invalid_keys = [key for key in plugins_config.keys() if '.' in key]

    if invalid_keys:
        logger.error("🚨 SYNTAX ERROR in PLUGINS_ENABLED:")
        for key in invalid_keys:
            logger.error(f"   -> Found '.' in '{key}'. Please use '/' as separator.")
            logger.info(f"   -> Found '.' in '{key}'. Please use '/' as separator.")

        sys.exit(1)
    return True

