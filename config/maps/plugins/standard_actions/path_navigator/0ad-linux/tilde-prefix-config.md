# source ~/.zshrc

# =========================================================================
# AUTOMATIc "tilde/" -> "~/" when ENTER-key
# =========================================================================
accept-line-override() {
    BUFFER="${BUFFER//tilde\//~/}"
    zle .accept-line
}
zle -N accept-line accept-line-override

# source ~/.zshrc
