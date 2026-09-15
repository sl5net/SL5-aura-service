import os
import sys
import time

for p in ['/opt/cudatext/cudatext/py', '/opt/cudatext/py', '/usr/share/cudatext/py']:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from cudatext import PROP_MODIFIED, Editor, ed_handles

LOG_FILE = '/tmp/cuda_silent_close.log'


def _log(msg):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass


_log("Module loaded")


class Command:
    def __init__(self):
        _log("Command initialized")

    def on_close_pre(self, ed_self):
        _log("on_close_pre called")
        if ed_self is not None:
            try:
                ed_self.set_prop(PROP_MODIFIED, False)
                _log("PROP_MODIFIED set to False")
            except Exception as ex:
                _log(f"Error in on_close_pre: {ex}")

    def on_exit_pre(self, ed_self):
        _log("on_exit_pre called")
        for h in ed_handles():
            try:
                Editor(h).set_prop(PROP_MODIFIED, False)
            except Exception as ex:
                _log(f"Error in on_exit_pre: {ex}")
