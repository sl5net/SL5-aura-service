#!/bin/bash
# scripts/dev/enable_setup_sudo_for_today.sh

# Ausführen:
# ./scripts/dev/enable_setup_sudo_for_today.sh 8

# Prüfen, ob/wann der Timer noch läuft:
# systemctl list-timers | grep sl5-sudo-expire

# Manuell vorzeitig beenden (z.B. wenn er früher Feierabend macht):
# sudo rm -f /etc/sudoers.d/99_setup
# sudo systemctl stop sl5-sudo-expire.timer 2>/dev/null || true


set -e

SUDOERS_FILE="/etc/sudoers.d/99_setup"
HOURS="${1:-8}"   # default: 8 hours validity

# old before 24.8.'26 11:19 Mon

# echo "linus ALL=(root) NOPASSWD: /usr/bin/apt-get, /usr/bin/apt, /usr/bin/add-apt-repository, /usr/bin/mv, /usr/bin/chmod, /usr/bin/dpkg" \
  #  | sudo tee "${SUDOERS_FILE}" > /dev/null

# new 24.8.'26 11:20 Mon

CURRENT_USER="${USER:-$(whoami)}"
echo "${CURRENT_USER} ALL=(ALL) NOPASSWD: ALL" \
  | sudo tee "${SUDOERS_FILE}" > /dev/null

sudo chmod 0440 "${SUDOERS_FILE}"

echo "[INFO] NOPASSWD rule active for ${HOURS}h."

# Reset existing timer unit if already loaded
sudo systemctl stop sl5-sudo-expire.timer sl5-sudo-expire.service 2>/dev/null || true
sudo systemctl reset-failed sl5-sudo-expire.timer sl5-sudo-expire.service 2>/dev/null || true

# Schedule automatic removal
sudo systemd-run --on-active="${HOURS}h" --unit=sl5-sudo-expire \
  /usr/bin/rm -f "${SUDOERS_FILE}"

echo "[INFO] Will auto-expire at: $(date -d "+${HOURS} hours")"
