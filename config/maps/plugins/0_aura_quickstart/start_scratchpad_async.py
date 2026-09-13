# config/maps/plugins/0_aura_quickstart/start_scratchpad_async.py:1
import asyncio
import sys
import os

async def start():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "config/maps/plugins/0_aura_quickstart/open_scratchpad_action.py", "--no-block",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
        stdin=asyncio.subprocess.DEVNULL,
    )
    # sofort weiter; proc kann überwacht werden falls nötig
    return proc

# in deinem event-loop aufrufen
# asyncio.create_task(start()) oder await start()
