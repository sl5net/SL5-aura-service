# Test Suites and Verification Scripts

This document outlines the organization and conventions for test scripts and verification tools in AURA.

## Main Test Locations

Developers should place new tests or mocks in the location that best fits their scope:

1- `scripts/test/`
   - Primary directory for functional tests, integration tests, and mock verification scripts.
   - Use subdirectories mirroring plugin paths when writing plugin-specific mocks or tests (e.g., `scripts/test/maps/plugins/game/0ad/signal/de-DE/mock/`).

2- `scripts/py/func/checks/`
   - Automated code integrity checkers, safety validators, and security rule enforcement (e.g., `integrity_checker.py`, `integrity_rules.py`).
   - Use this directory for static verification tools and repository rule checks.

3- `tools/tests/`
   - Command-line utility tests, environment verification, and tool-chain tests.

## Developer Rules for Test Scripts

- **Execution Environment**: Always run test scripts using the virtual environment interpreter (`.venv/bin/python`) or with `PYTHONPATH=.`.
- **No Manual `sys.path` Manipulation**: Never write `sys.path.insert(0, …)` or manually alter `sys.path` inside test or mock scripts. Import paths must be managed by the execution environment or AURA framework itself.

(S, 7.8.'26 13:49 Fri)
