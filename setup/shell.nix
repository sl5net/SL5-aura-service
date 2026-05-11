# setup/shell.nix
#
# 👋 Not on NixOS? This file is only for NixOS users — ignore it.
#    Use your platform's setup script instead:
#      Linux (Ubuntu):  bash setup/ubuntu_setup.sh
#      Linux (openSUSE): bash setup/suse_setup.sh
#      macOS:           bash setup/macos_setup.sh
#      Windows:         setup/windows11_setup.ps1
#
# ⚠️  EXPERIMENTAL ...#
# ⚠️  EXPERIMENTAL — UNTESTED by the authors (we don't run NixOS).
#     Written by analogy with ubuntu_setup.sh. Please report what breaks!
#
# HOW TO USE:
#   1. Enter this shell from the project root:
#          nix-shell setup/shell.nix
#   2. Then run the setup script (once, to install everything):
#          bash setup/nixos_setup.sh
#   3. To start the server on subsequent runs:
#          nix-shell setup/shell.nix --run "bash scripts/restart_venv_and_run-server.sh"
#      or just: nix-shell setup/shell.nix  (then run the script manually)
#
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  name = "aura-dev-shell";
  buildInputs = with pkgs; [
    # --- Python ---
    python311
    python311Packages.pip
    python311Packages.virtualenv

    # --- C libraries needed by Python wheels ---
    stdenv.cc.cc.lib
    zlib
    glib

    # --- Audio dependencies ---
    portaudio
    alsa-lib
    libpulseaudio

    # --- Java >= 17 (required for LanguageTool) ---
    jdk21

    # --- Core tools (mirrors ubuntu_setup.sh apt-get installs) ---
    unzip
    wget
    ffmpeg
    fzf
    inotify-tools
    xclip
    xvfb-run   # provides xvfb

    # --- SDL2 (used by some Python packages) ---
    SDL2
    SDL2_image
    SDL2_mixer
    SDL2_ttf
    freetype

    # --- dotool: NOT available here, must be in configuration.nix ---
    # See docs/LINUX_WAYLAND_dotool.md and the warning in nixos_setup.sh
  ];

  shellHook = ''
    # Makes C libraries visible to Python wheels inside the venv
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:${pkgs.alsa-lib}/lib:${pkgs.libpulseaudio}/lib:${pkgs.glib}/lib:$LD_LIBRARY_PATH"

    echo ""
    echo "⚠️  EXPERIMENTAL SETUP — UNTESTED"
    echo "    This shell.nix was written for NixOS but has not been verified by its authors."
    echo "    If something breaks, please let us know and we'll fix it together!"
    echo ""
    echo "First time setup? Run:"
    echo "  bash setup/nixos_setup.sh"
    echo ""
    echo "To start Aura (after setup):"
    echo "  bash scripts/restart_venv_and_run-server.sh"
    echo ""
  '';
}
