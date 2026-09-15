import os
import sys
import time

for p in ['/opt/cudatext/cudatext/py', '/opt/cudatext/py', '/usr/share/cudatext/py']:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from cudatext import MB_ICONINFO, MB_OK, PROP_MODIFIED, Editor, ed_handles, msg_box, msg_status
from .config_storage import load_plugin_state, save_plugin_state

LOG_FILE = '/tmp/cuda_silent_close.log'


def _log(msg):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass


_log("Module loaded")


CONFIG_FILENAME = 'cuda_silent_close.json'


class Command:
    def __init__(self):
        self.enabled = load_plugin_state(CONFIG_FILENAME, default_state=False)
        _log(f"Command initialized (enabled={self.enabled})")

    def cmd_toggle(self):
        self.enabled = not self.enabled
        save_plugin_state(CONFIG_FILENAME, self.enabled)
        state_label = 'ON' if self.enabled else 'OFF'
        msg_status(f"Silent Close: {state_label}")
        _log(f"Silent Close toggled to: {state_label}")
        msg_box(f"Silent Close is now {state_label}", MB_OK | MB_ICONINFO)
        
    def on_close_pre(self, ed_self):
        if not self.enabled:
            return
        _log("on_close_pre called")
        if ed_self is not None:
            try:
                ed_self.set_prop(PROP_MODIFIED, False)
                _log("PROP_MODIFIED set to False")
            except Exception as ex:
                _log(f"Error in on_close_pre: {ex}")

    def on_exit_pre(self, ed_self):
        if not self.enabled:
            return
        _log("on_exit_pre called")
        for h in ed_handles():
            try:
                Editor(h).set_prop(PROP_MODIFIED, False)
            except Exception as ex:
                _log(f"Error in on_exit_pre: {ex}")
                
                
                
