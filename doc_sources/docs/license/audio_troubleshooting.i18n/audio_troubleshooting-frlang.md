# Dépannage audio (Linux)

## Problème : Espeak / Fallback est silencieux
Si l'audio de secours (explication) n'est pas audible, il est probablement coupé dans le mixeur sonore du système (par exemple, PulseAudio ou PipeWire).

### Le "truc des chaînes longues" pour réactiver le son
Les fragments audio courts disparaissent souvent trop rapidement de l'interface graphique du mixeur pour être réactivés manuellement. Pour résoudre ce problème, forcez un long flux audio :

__CODE_BLOCK_0__