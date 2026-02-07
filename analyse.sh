HASH="83b1f43"
# 1. Die spezifischen Code-Änderungen
git diff $HASH..HEAD -- aura_engine.py > ~/aura_engine_$HASH.txt
git diff $HASH..HEAD -- scripts/py/func/map_reloader.py > ~/map_reloader_$HASH.txt
git diff $HASH..HEAD -- config/maps/plugins/standard_actions/zip_all/de-DE/zip.py > ~/zip_logic_$HASH.txt

# 2. Den massiven Diff filtern (nur relevante Begriffe suchen)
git diff $HASH..HEAD | grep -Ei "zip|pack|unpack|auth_key|_alerts|encrypted" -C 5 > filtered_diff_$HASH.txt

# 3. Alle erstellten Dateien in Kate öffnen
kate aura_engine_$HASH.txt map_reloader_$HASH.txt zip_logic_$HASH.txt filtered_diff_$HASH.txt

# git diff 83b1f43..HEAD -- aura_engine.py > ~/t.txt && kate ~/t.txt
