#!/bin/bash
# setup/helpers/system-deps-ubuntu.sh
#
# Shared list of Debian/Ubuntu system packages
# from source via pip.
# pycairo publishes no Linux wheels on PyPI, so this is needed on every
# Debian/Ubuntu machine -- CI or local -- before `pip install PyGObject`.
# (s, 14.9.'26 11:49 Mon)

# Sourced by:
#   - setup/ubuntu_setup.sh
#   - .github/workflows/ubuntu_recording_trigger.yml
PYGOBJECT_BUILD_DEPS_UBUNTU="libgirepository-2.0-dev libcairo2-dev"
