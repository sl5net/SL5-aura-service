import os
from cudatext import *

# How often (ms) to poll open files for external changes.
TIMER_INTERVAL = 1000

ENC_MAP = {
    'UTF-8': 'utf-8',
    'UTF-8-BOM': 'utf-8-sig',
    'CP1251': 'cp1251',
    'CP1252': 'cp1252',
    'ANSI': 'cp1252',
    'CP866': 'cp866',
    'KOI8-R': 'koi8-r',
    'ISO-8859-1': 'iso-8859-1',
    'UTF-16LE': 'utf-16-le',
    'UTF-16BE': 'utf-16-be',
}


class Command:
    def __init__(self):
        self.mtimes = {}   # filename -> last known mtime (float)
        self.enabled = True
        self.timer_started = False
        print("[Disk Wins] Plugin Command instance initialized.")

    def _ensure_timer(self):
        if not self.timer_started:
            timer_proc(TIMER_START, self.on_timer, TIMER_INTERVAL)
            self.timer_started = True
            print(f"[Disk Wins] Timer started with interval {TIMER_INTERVAL}ms.")

    # ---- events -------------------------------------------------
    def on_start(self, ed_self=None):
        self._ensure_timer()
        self._scan_all(initial=True)

    def on_start2(self, ed_self=None):
        self._ensure_timer()
        self._scan_all(initial=True)

    def on_open(self, ed_self):
        self._ensure_timer()
        fn = ed_self.get_filename()
        if fn and fn != '?':
            self._remember(fn)
            
            
    def on_save(self, ed_self):
        fn = ed_self.get_filename()
        if fn and fn != '?':
            self._remember(fn)

    def on_timer(self, tag='', info=''):
        if self.enabled:
            self._scan_all()

    # ---- commands (Plugins menu) ---------------------------------

    def cmd_toggle(self):
        self.enabled = not self.enabled
        msg_status('Disk Wins auto-reload: ' + ('ON' if self.enabled else 'OFF'))

    def cmd_check_now(self):
        self._scan_all()
        msg_status('Disk Wins: checked all open files against disk')

    # ---- internals -------------------------------------------------

    def _remember(self, fn):
        try:
            self.mtimes[fn] = os.path.getmtime(fn)
        except OSError:
            pass

    def _scan_all(self, initial=False):
        for h in ed_handles():
            e = Editor(h)
            fn = e.get_filename()
            if not fn or fn == '?':
                continue

            try:
                disk_mtime = os.path.getmtime(fn)
            except OSError:
                # file deleted/unavailable right now - just skip
                continue

            known = self.mtimes.get(fn)
            if known is None:
                self.mtimes[fn] = disk_mtime
                continue

            if disk_mtime > known + 0.001:
                if initial:
                    # don't fight the session restore on startup
                    self.mtimes[fn] = disk_mtime
                    continue
                self._reload_from_disk(e, fn, disk_mtime)

    def _reload_from_disk(self, e, fn, disk_mtime):
        py_enc = ENC_MAP.get(e.get_prop(PROP_ENC) or 'UTF-8', 'utf-8')
        try:
            with open(fn, 'r', encoding=py_enc, errors='replace') as f:
                text = f.read()
        except OSError:
            return

        carets = e.get_carets()
        try:
            top_line = e.get_prop(PROP_LINE_TOP)
        except Exception:
            top_line = None

        e.set_text_all(text)
        # Disk always wins: drop the "modified" flag, don't ask anything.
        e.set_prop(PROP_MODIFIED, False)

        if carets:
            x0, y0, x1, y1 = carets[0]
            max_line = max(0, e.get_line_count() - 1)
            y0 = min(y0, max_line)
            if y1 >= 0:
                y1 = min(y1, max_line)
            try:
                e.set_caret(x0, y0, x1, y1, CARET_SET_ONE, CARET_OPTION_NO_SCROLL)
            except Exception:
                pass

        if top_line is not None:
            try:
                e.set_prop(PROP_LINE_TOP, top_line)
            except Exception:
                pass

        self.mtimes[fn] = disk_mtime
        msg_status('Disk Wins: "%s" changed on disk -> reloaded (unsaved editor changes discarded)'
                   % os.path.basename(fn))
