# source ~/.zshrc

# =========================================================================
# AUTOMATIQUE "tilde/" -> "~/" avec la touche ENTER
# =========================================================================
accepter-line-override() {
BUFFER="${BUFFER//tilde\//~/}"
zle .accepter-ligne
}
zle -N accepter-ligne accepter-ligne-override

# source ~/.zshrc