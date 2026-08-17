# Log Filter Profiles

The active log filter is always `config/filters/settings_local_log_filter.py`.

## Profiles

Predefined profiles are stored in `config/filters/.backlock/`:

| Profile | Description |
|---|---|
| `first_run` | Minimal output — errors and status only. Applied automatically on first start. |
| `normal` | Standard filter for everyday use. |

## Switch profile manually

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

## Add a custom profile

1. Create a new folder under `config/filters/.backlock/my_profile/`
2. Copy an existing `settings_local_log_filter.py` into it and edit to your needs
3. Apply it with `cp` as shown above

## Automatic profile switching

On first start, Aura detects that the `log/` directory does not yet exist and
automatically copies the `first_run` profile as the active filter.
