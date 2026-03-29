In addition to the many search options, there is probably a full-text search in your development environment, You can also use:

scripts/search_rules/search_rules.sh

This allows you to search in the existing maps or in the source code or documentation. and then you can open peace you found in your favorite edior or open it on github or ... please configure the script as you need it.

MAPS_DIR is configurable via positional arg or environment variable

script keeps its hard-coded default but allows overrides:

- Priority: 1) first positional parameter ($1), 2) existing MAPS_DIR env var,
  3) hard-coded default "$PROJECT_ROOT/config/maps".
- Improves flexibility for CI, local overrides and testing without editing the script.
- Adds quoting and a directory existence check to fail early if the path is invalid.

Example usage:
- ./search_rules.sh                 uses default
- ./search_rules.sh ./docs    uses provided path
- MAPS_DIR=/env/maps ./search_rules.sh

This preserves backward compatibility while making configuration explicit.

There is also a version for Windows PC (in this folder) that can do a little less : search_rules.ps1


(s, 28.3.'26 23:07 Sat)
