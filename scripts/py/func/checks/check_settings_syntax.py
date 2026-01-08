import sys
import logging

logger = logging.getLogger(__name__)


def verify_plugin_notation(plugins_config):
    if not plugins_config:
        msg = "🚨 FATAL: PLUGINS_ENABLED is empty. Check your settings files."
        print(msg)
        logger.critical(msg)
        sys.exit(1)

    invalid_keys = [key for key in plugins_config.keys() if '.' in key]

    if invalid_keys:
        header = "\n" + "!" * 60 + "\n🚨 CONFIGURATION ERROR: Invalid Plugin Notation\n" + "!" * 60
        print(header)
        logger.error(header)

        for key in invalid_keys:
            suggestion = key.replace('.', '/')
            detail = f"   -> Invalid: '{key}' | Suggested: '{suggestion}'"
            print(detail)
            logger.error(detail)

        print("!" * 60 + "\n")
        # Ensure logs are flushed before exiting
        logging.shutdown()
        sys.exit(1)

    return True