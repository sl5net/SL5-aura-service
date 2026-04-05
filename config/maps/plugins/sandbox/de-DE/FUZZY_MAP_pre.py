# projects/py/STT/config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
# import runpy

# PROJECT_ROOT = Path("C:/tmp" if platform.system()=="Windows" else "/tmp")/"sl5_aura"/"sl5net_aura_project_root"
# tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
# PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())


#
# acp = PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
# AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]
# WAKE_PHANTOM = runpy.run_path(acp)["WAKE_PHANTOM"]

# SEARCH_SCRIPT = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"
#
nix = """
Inzwischen eigentlich ein schönes Wetter heuteWie ist das Wetter heute

"""
FUZZY_MAP_pre = [
    #('ASp', fr'^(Auri)$', 100, {'flags': re.IGNORECASE,}),
    #('AS', fr'^{AURA_VARIANTS}\b.*\b(ölkjlkj|suchen|zu)$', 100, {'flags':re.IGNORECASE,}),
    #('A', fr'^{AURA_VARIANTS}\b.*\b(suche|zu)$', 100, {'flags': re.IGNORECASE,}),
    #################################################
    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[Path(PROJECT_ROOT) / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################
]
