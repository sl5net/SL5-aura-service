# Protokollfilterprofile

Der aktive Protokollfilter ist immer „config/filters/settings_local_log_filter.py“.

## Profile

Vordefinierte Profile werden in „config/filters/.backlock/“ gespeichert:

| Profil | Beschreibung |
|---|---|
| `first_run` | Minimale Ausgabe – nur Fehler und Status. Wird beim ersten Start automatisch angewendet. |
| „normal“ | Standardfilter für den täglichen Gebrauch. |

## Profil manuell wechseln

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

## Fügen Sie ein benutzerdefiniertes Profil hinzu

1. Erstellen Sie einen neuen Ordner unter „config/filters/.backlock/my_profile/“.
2. Kopieren Sie eine vorhandene Datei „settings_local_log_filter.py“ hinein und bearbeiten Sie sie entsprechend Ihren Anforderungen
3. Wenden Sie es wie oben gezeigt mit „cp“ an

## Automatischer Profilwechsel

Beim ersten Start erkennt Aura, dass das Verzeichnis „log/“ noch nicht existiert und
kopiert automatisch das Profil „first_run“ als aktiven Filter.