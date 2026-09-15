import os
import sys

for p in ['/opt/cudatext/cudatext/py', '/opt/cudatext/py', '/usr/share/cudatext/py']:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from cudatext import ed_handles
from .reset_modified import discard_all_editors_modified, discard_editor_modified


class Command:
    def on_close_pre(self, ed_self):
        discard_editor_modified(ed_self)

    def on_exit_pre(self, ed_self):
        discard_all_editors_modified(ed_handles())
