### 2. `Tilde_Shell_Hack.md`
*Ten plik wyjaśnia obejście ograniczenia Aury dotyczące wiodących znaków specjalnych, dokumentując zarówno podstawienie `tyldy/`, jak i widżet integracji Zsh.*

__KOD_BLOKU_0__
# ==========================================================================
# Automatyczne podstawienie „tylda/” -> „~/” po Enter
# ==========================================================================
zaakceptuj-zastąpienie-linii() {
BUFFER="${BUFOR//tylda\//~/}"
zle .accept-line
}
zle -N zastąpienie linii akceptacji
__KOD_BLOKU_1__