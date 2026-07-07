# Quelle ~/.zshrc

# ======================================================================
# AUTOMATISCH „tilde/“ -> „~/“ bei ENTER-Taste
# ======================================================================
Accept-line-override() {
BUFFER="${BUFFER//tilde\//~/}"
zle .accept-line
}
zle -N Accept-Line Accept-Line-Override

# Quelle ~/.zshrc