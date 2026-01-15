# file scripts/py/func/log_memory_details.py
import os
import psutil
from .config.dynamic_settings import settings


# --- Start of suggested DEBUG memory analysis snippet ---

def log4DEV(text: str, logger):
    if not settings.DEV_MODE_all_processing:
        # print('10:not DEV_MODE_all_processing: return')
        return
    import inspect
    caller_script_name = "unknown"
    caller_file_and_line = "unknown:0"
    caller_line = 0

    stack = inspect.stack()
    # Find the frame that is *not* log_memory_details itself
    # and also not an internal inspect frame
    for frame_info in stack:
        # Check if the function name is not log_memory_details
        # and if it's not part of the inspect module itself
        if frame_info.function != 'log4DEV' and \
           not frame_info.filename.startswith(inspect.__file__):
            try:
                # Get the base name of the calling script
                caller_script_name = os.path.basename(frame_info.filename)
                # Get the full path of the calling script and its line number

                caller_line= frame_info.lineno
                # caller_file_and_line = f"XYZ:{os.path.relpath(frame_info.filename)}:{caller_line}"


                # caller_file_and_line = f"XYZ:{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
                caller_file_and_line = f"🍒 {os.path.relpath(caller_script_name)}:{caller_line}"
                break # Found the caller, exit loop
            except Exception as e:
                logger.debug(f"Error getting caller info: {e}")
                pass # Continue to next frame if there's an issue with this one

    if not settings.DEV_MODE:
        print('10:not settings.DEV_MODE: return')
        return


    # Construct the log message for the memory details
    logger.info(f"{caller_file_and_line} {text}")
    # return caller_file_and_line, caller_script_name, caller_file_and_line


def log_memory_details(stage: str, logger):
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()

# Tip: Remove lines in log you dont interesting in. Example
# ^(?!.*(Memory|RSS|Data Segment)).*\n$

    import inspect

    caller_script_name = "unknown"
    caller_file_and_line = "unknown:0"

    stack = inspect.stack()
    # Find the frame that is *not* log_memory_details itself
    # and also not an internal inspect frame
    for frame_info in stack:
        # Check if the function name is not log_memory_details
        # and if it's not part of the inspect module itself
        if frame_info.function != 'log_memory_details' and \
           not frame_info.filename.startswith(inspect.__file__):
            try:
                # Get the base name of the calling script
                caller_script_name = os.path.basename(frame_info.filename)
                # Get the full path of the calling script and its line number
                caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
                break # Found the caller, exit loop
            except Exception as e:
                logger.debug(f"Error getting caller info: {e}")
                pass # Continue to next frame if there's an issue with this one

    # Construct the log message for the memory details
    logger.info(f"--- Memory {caller_script_name} {caller_file_and_line} {stage} --- Tip: ^(?!.*(Memory|RSS|VMS|Data Segment)).*\\n ")

    logger.info(f" RSS: {mem_info.rss / (1024 * 1024):.2f} MB") # (Physical RAM used by process)
    # logger.info(f" VMS: {mem_info.vms / (1024 * 1024):.2f} MB") # (Total virtual memory)
    # logger.info(f"  Shared Memory: {mem_info.shared / (1024 * 1024):.2f} MB")
    # On Linux, these might be more relevant for detailed breakdown
    # logger.info(f" Data Segment: {getattr(mem_info, 'data', 0) / (1024 * 1024):.2f} MB") # Specific to some OS, like Linux

    """
    DEBUG:
    if getattr(settings, "DEV_MODE_memory", False):
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"Line 135", logger)

    Wir haben ein Speicherleck in Python-Objekten da Data Segment mit jedem Arbeitsschritt kontuierlich ansteigt.
    Data Segment:Ist auch sehr aufschlussreich, da hier die dynamisch allokierten Daten (Objekte, Listen, etc.) liegen.
    Wenn dieser Wert kontinuierlich steigt, deutet es sehr stark auf ein Speicherleck in Python-Objekten hin.
    """

    # logger.info(f"  Text Segment: {getattr(mem_info, 'text', 0) / (1024 * 1024):.2f} MB") # Specific to some OS, like Linux
    # logger.info(f"  Stack Size: {getattr(mem_info, 'stack', 0) / (1024 * 1024):.2f} MB") # Specific to some OS, like Linux
    logger.info("-")
    logger.info("-")
    return mem_info.rss

# Call this at the very beginning of your script
# log_memory_details("Script Start",logger)
# log_memory_details("After Vosk Model Load",logger)