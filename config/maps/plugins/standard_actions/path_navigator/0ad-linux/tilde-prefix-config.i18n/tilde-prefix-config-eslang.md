# fuente ~/.zshrc

# ===========================================================================
# AUTOMÁTICO "tilde/" -> "~/" cuando se pulsa la tecla ENTER
# ===========================================================================
aceptar-anulación-línea() {
BUFFER="${BUFFER//tilde\//~/}"
zle .accept-línea
}
zle -N aceptar-línea aceptar-anular línea

# fuente ~/.zshrc