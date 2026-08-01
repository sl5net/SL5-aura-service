# źródło ~/.zshrc

# ==========================================================================
# AUTOMATYCZNY "tylda/" -> "~/" po naciśnięciu klawisza ENTER
# ==========================================================================
zaakceptuj-zastąpienie-linii() {
BUFFER="${BUFOR//tylda\//~/}"
zle .accept-line
}
zle -N zastąpienie linii akceptacji

# źródło ~/.zshrc