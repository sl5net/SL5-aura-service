# ソース ~/.zshrc

# ===================================================================
# ENTERキーを押すと自動 "チルダ/" -> "~/"
# ===================================================================
accept-line-override() {
BUFFER="${BUFFER//チルダ\//~/}"
zle .accept-line
}
zle -N accept-line accept-line-override

# ソース ~/.zshrc