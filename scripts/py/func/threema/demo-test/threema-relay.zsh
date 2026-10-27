#!/usr/bin/env zsh
# threema-relay.zsh - Threema Beta (Flatpak) -> Element per X11-Automatisierung
#
# Befehle:
#   calibrate        Offsets interaktiv messen und in der Config speichern
#   test             Letzte eingehende Nachricht kopieren und ausgeben (kein Einfuegen)
#   once             Kopieren und in Element einfuegen (ein Durchlauf)
#   watch            Auf Threema-Benachrichtigungen (D-Bus) warten und bei jeder 'once' ausfuehren
#   send-threema [TEXT]   Text (Argument oder stdin) in Threema einfuegen, Hash wird vorher gemerkt
#   forget           Hash-Speicher leeren
#
# Benoetigt: xdotool, xclip, sha1sum, flock; optional: notify-send, dbus-monitor (fuer watch)

zmodload zsh/mathfunc
export LC_NUMERIC=C      # sonst schreibt printf '0,9353' (deutsche Locale) und die Arithmetik bricht
SCRIPT=${0:A}

CONF=${XDG_CONFIG_HOME:-$HOME/.config}/threema-relay.conf
STATE=${XDG_RUNTIME_DIR:-/tmp}/threema-relay
mkdir -p "$STATE"
HASHES=$STATE/hashes
LOCK=$STATE/lock
touch "$HASHES"

# ---- Defaults (werden durch 'calibrate' in $CONF ueberschrieben) ----
THREEMA_CLASS="Threema Beta"
ELEMENT_CLASS="^element"
FX=0.30              # Klick-X als Anteil der Fensterbreite (links = eingehende Nachrichten)
BOTTOM=110           # Klick-Y: Pixel oberhalb der Fensterunterkante (letzte Bubble)
DX=12; DY=14         # Offset Klickpunkt -> 'Copy Message'
INPUT_FX=0.50        # Eingabefeld: X-Anteil
INPUT_BOTTOM=40      # Eingabefeld: Pixel ueber der Fensterunterkante
DELAY_MENU=0.30      # Wartezeit bis das Kontextmenue offen ist
DELAY_COPY=0.20      # Wartezeit nach Klick auf 'Copy Message'
WATCH_DELAY=0.6      # Wartezeit nach Benachrichtigung, bis Nachricht im Chat steht
SEND_ENTER=0         # 1 = nach Einfuegen in Threema Return druecken
ELEMENT_ENTER=0      # 1 = nach Einfuegen in Element Return druecken
RESTORE_FOCUS=1      # 1 = vorheriges Fenster wieder aktivieren
MAXHASH=50
CLOSE_MENU=click     # click | escape | none : wie ein offenes Menue bei Fehlschlag geschlossen wird

[[ -r $CONF ]] && source "$CONF"
# Kommas aus aelteren Config-Dateien reparieren (0,9353 -> 0.9353)
FX=${FX//,/.}; BOTTOM=${BOTTOM//,/.}; INPUT_FX=${INPUT_FX//,/.}

# ---------------------------------------------------------------------
die()  { print -u2 -- "FEHLER: $*"; exit 1 }
info() { print -u2 -- "$*" }

for t in xdotool xclip sha1sum flock; do
  command -v $t >/dev/null || die "'$t' fehlt"
done

find_win() {   # $1 = Klassen-Regex; liefert die erste ausreichend grosse Fenster-ID
  local id flag X Y WIDTH HEIGHT SCREEN WINDOW
  for flag in --onlyvisible ""; do        # erst sichtbare, dann auch unsichtbare (z. B. minimierte)
    for id in $(xdotool search ${flag:+$flag} --class "$1" 2>/dev/null); do
      eval "$(xdotool getwindowgeometry --shell $id 2>/dev/null)"
      if (( ${WIDTH:-0} > 300 && ${HEIGHT:-0} > 300 )); then
        print -- $id
        return 0
      fi
    done
  done
  return 1
}

debug_windows() {
  local id c
  info "== wmctrl -lx =="
  command -v wmctrl >/dev/null && wmctrl -lx >&2
  for c in "$THREEMA_CLASS" "$ELEMENT_CLASS"; do
    info "== alle Fenster mit Klasse '$c' =="
    for id in $(xdotool search --class "$c" 2>/dev/null); do
      info "ID $id  Name='$(xdotool getwindowname $id 2>/dev/null)'"
      xdotool getwindowgeometry $id >&2 2>&1
    done
    info "== davon sichtbar =="
    xdotool search --onlyvisible --class "$c" >&2 2>&1
  done
  info "== Config =="
  cat "$CONF" >&2
}

geom() {       # setzt WX WY WW WH
  local X Y WIDTH HEIGHT SCREEN WINDOW
  eval "$(xdotool getwindowgeometry --shell $1)"
  WX=$X; WY=$Y; WW=$WIDTH; WH=$HEIGHT
}

mouse_pos() {  # setzt MX MY
  local X Y SCREEN WINDOW
  eval "$(xdotool getmouselocation --shell)"
  MX=$X; MY=$Y
}

hash_of() { printf %s "$1" | sha1sum | cut -d' ' -f1 }
seen()    { grep -qx -- "$1" "$HASHES" 2>/dev/null }
remember() {
  print -- "$1" >> "$HASHES"
  tail -n $MAXHASH "$HASHES" > "$HASHES.tmp" && mv "$HASHES.tmp" "$HASHES"
}

trim() { local s="$1"; s="${s%"${s##*[![:space:]]}"}"; print -rn -- "$s" }

countdown() {  # $1 = Sekunden, $2 = Text
  info ""
  info ">>> $2"
  command -v notify-send >/dev/null && notify-send -t $(( $1 * 1000 )) "threema-relay" "$2" 2>/dev/null
  local i
  for (( i=$1; i>0; i-- )); do printf '\r    noch %2d s ' $i >&2; sleep 1; done
  printf '\r    erfasst.      \n' >&2
}

# ---------------------------------------------------------------------
calibrate() {
  local WID WX WY WW WH MX MY P1X P1Y P2X P2Y P3X P3Y
  WID=$(find_win "$THREEMA_CLASS") || die "Threema-Fenster nicht gefunden"
  xdotool windowactivate --sync $WID
  info "Fenster nicht mehr verschieben/skalieren waehrend der Kalibrierung."

  countdown 10 "1/3: RECHTSKLICK auf die letzte EINGEHENDE Nachricht (linke Bubble). Menue offen lassen, Maus dort ruhen lassen."
  mouse_pos; P1X=$MX; P1Y=$MY

  countdown 7 "2/3: Maus (ohne Klick) auf 'Copy Message' bewegen und ruhen lassen."
  mouse_pos; P2X=$MX; P2Y=$MY
  geom $WID; close_menu

  countdown 7 "3/3: Maus (ohne Klick) auf das Eingabefeld bewegen (zum Schreiben)."
  mouse_pos; P3X=$MX; P3Y=$MY

  geom $WID
  local nFX nBOTTOM nDX nDY nIFX nIB
  nFX=$(printf '%.4f' $(( (P1X - WX) * 1.0 / WW )))
  nBOTTOM=$(( WY + WH - P1Y ))
  nDX=$(( P2X - P1X ))
  nDY=$(( P2Y - P1Y ))
  nIFX=$(printf '%.4f' $(( (P3X - WX) * 1.0 / WW )))
  nIB=$(( WY + WH - P3Y ))

  mkdir -p "${CONF:h}"
  {
    print "# erzeugt von threema-relay.zsh calibrate am $(date '+%F %T')"
    print "FX=$nFX"
    print "BOTTOM=$nBOTTOM"
    print "DX=$nDX"
    print "DY=$nDY"
    print "INPUT_FX=$nIFX"
    print "INPUT_BOTTOM=$nIB"
  } > "$CONF"
  info ""
  info "Gespeichert in $CONF:"
  cat "$CONF" >&2
  info ""
  info "Naechster Schritt: '$SCRIPT test' mit einer frischen eingehenden Nachricht als letzter im Chat."
}

# ---------------------------------------------------------------------
close_menu() {   # nutzt WX WY WW WH MX MY des Aufrufers
  case "$CLOSE_MENU" in
    escape) xdotool key Escape ;;
    none)   ;;
    *)      xdotool mousemove $(( int(WX + WW * 0.5) )) $(( int(WY + WH * 0.25) )) click 1
            xdotool mousemove $MX $MY ;;
  esac
}

# Kopiert die letzte eingehende Nachricht; Ergebnis in $TXT.
# Rueckgabe: 0 = Text kopiert, 1 = nichts kopiert, 2 = Fehler
copy_from_threema() {
  local WID WX WY WW WH MX MY CX CY SENT
  WID=$(find_win "$THREEMA_CLASS") || { info "Threema-Fenster nicht gefunden"; return 2 }
  PREV_WIN=$(xdotool getactivewindow 2>/dev/null)
  geom $WID
  mouse_pos

  SENT="__relay_sentinel_${RANDOM}_${RANDOM}__"
  printf %s "$SENT" | xclip -selection clipboard -i

  (( CX = int(WX + WW * FX) ))
  (( CY = WY + WH - BOTTOM ))

  xdotool windowactivate --sync $WID
  sleep 0.15
  xdotool mousemove $CX $CY click 3
  sleep $DELAY_MENU
  xdotool mousemove $(( CX + DX )) $(( CY + DY )) click 1
  sleep $DELAY_COPY
  xdotool mousemove $MX $MY

  TXT=$(xclip -selection clipboard -o 2>/dev/null)
  if [[ "$TXT" == "$SENT" || -z "$TXT" ]]; then
    close_menu                    # evtl. haengendes Menue schliessen
    return 1
  fi
  TXT=$(trim "$TXT")
  return 0
}

restore_focus() {
  (( RESTORE_FOCUS )) && [[ -n "$PREV_WIN" ]] && xdotool windowactivate "$PREV_WIN" 2>/dev/null
}

paste_into_element() {
  local EID
  EID=$(find_win "$ELEMENT_CLASS") || { info "Element-Fenster nicht gefunden"; return 1 }
  # Clipboard enthaelt bereits den Text; sicherheitshalber erneut setzen
  printf %s "$TXT" | xclip -selection clipboard -i
  xdotool windowactivate --sync $EID
  sleep 0.2
  xdotool key --clearmodifiers ctrl+v
  (( ELEMENT_ENTER )) && { sleep 0.1; xdotool key Return }
  return 0
}

do_test() {
  copy_from_threema
  case $? in
    0) info "--- kopierter Text ---"; print -r -- "$TXT"; info "--- Hash: $(hash_of "$TXT") ---";;
    1) info "Nichts kopiert (Sentinel unveraendert). Offsets pruefen oder letzte Nachricht war eigene.";;
  esac
  restore_focus
}

relay_once() {
  exec 9>"$LOCK"
  flock -n 9 || { info "Lauf aktiv, ueberspringe"; return 0 }
  local rc h
  copy_from_threema; rc=$?
  if (( rc != 0 )); then restore_focus; return $rc; fi

  h=$(hash_of "$TXT")
  if seen "$h"; then
    info "Schon gesehen/gesendet (Hash $h) -> ignoriert"
    restore_focus
    return 0
  fi
  remember "$h"
  paste_into_element
  restore_focus
  info "Weitergeleitet: ${TXT[1,60]}"
}

send_threema() {
  local txt WID WX WY WW WH CX CY
  if (( $# )); then txt="$*"; else txt=$(cat); fi
  txt=$(trim "$txt")
  [[ -z "$txt" ]] && die "kein Text"
  WID=$(find_win "$THREEMA_CLASS") || die "Threema-Fenster nicht gefunden"
  PREV_WIN=$(xdotool getactivewindow 2>/dev/null)

  remember "$(hash_of "$txt")"      # VOR dem Senden merken -> Schleifenschutz
  printf %s "$txt" | xclip -selection clipboard -i

  geom $WID
  (( CX = int(WX + WW * INPUT_FX) ))
  (( CY = WY + WH - INPUT_BOTTOM ))
  xdotool windowactivate --sync $WID
  sleep 0.2
  xdotool mousemove $CX $CY click 1
  sleep 0.1
  xdotool key --clearmodifiers ctrl+v
  (( SEND_ENTER )) && { sleep 0.1; xdotool key Return }
  restore_focus
}

watch_notifications() {
  command -v dbus-monitor >/dev/null || die "dbus-monitor fehlt"
  info "Warte auf Threema-Benachrichtigungen (Strg+C beendet) ..."
  local line n=0 hit=0
  dbus-monitor "interface='org.freedesktop.Notifications',member='Notify'" 2>/dev/null |
  while IFS= read -r line; do
    if [[ $line == *member=Notify* ]]; then n=10; hit=0; continue; fi
    if (( n > 0 )); then
      (( n-- ))
      if (( ! hit )) && [[ ${line:l} == *threema* ]]; then
        hit=1
        sleep $WATCH_DELAY
        relay_once
      fi
    fi
  done
}

# ---------------------------------------------------------------------
case "${1:-}" in
  calibrate) calibrate ;;
  test)      do_test ;;
  once)      relay_once ;;
  watch)     watch_notifications ;;
  send-threema) shift; send_threema "$@" ;;
  debug)     debug_windows ;;
  forget)    : > "$HASHES"; info "Hash-Speicher geleert" ;;
  *) sed -n '2,13p' "$0" ;;
esac
