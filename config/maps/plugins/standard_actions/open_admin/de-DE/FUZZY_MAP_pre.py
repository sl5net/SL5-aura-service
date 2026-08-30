import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())





import runpy

acp = SL5NET_AURA_PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]

CONFIG_DIR = p(__file__).parent


FUZZY_MAP_pre = [

    # EXAMPLE: Aura Admin öffnen open admin panel.
    ('', rf'^{AURA_VARIANTS} Admin\w*\b.*$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' /  'open_admin.py']
    }),



]

