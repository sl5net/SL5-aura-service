# fonte ~/.zshrc

# =====================================================================
# AUTOMÁTICO "til/" -> "~/" quando a tecla ENTER
# =====================================================================
aceitar substituição de linha() {
BUFFER="${BUFFER//til\//~/}"
zle .accept-line
}
zle -N aceitar linha aceitar substituição de linha

# fonte ~/.zshrc