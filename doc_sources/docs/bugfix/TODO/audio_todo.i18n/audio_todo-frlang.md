31.12.'25 18:25 mer.

Aide-mémoire et liste de tâches pour l'organisation :

### Documentation : version "Entrée audio unifiée" (micro + bureau)
**Statut :** Pausiert (Preuve de concept existante, mais non stable/performante).

**Erfahrungen / Résultats :**
* **Routage :** PipeWire/PulseAudio est maintenant disponible, le flux Python (ALSA-Bridge) étant connecté au microphone standard physique (Logique de restauration de flux).
* **Performance :** L'analyse de RMS, VAD et Vosk dans une seule boucle, combinée avec des `pactl`-Aufrufen externes, pour votre dernier CPU (Lüfterdrehen).
* **Signal :** L'index de périphérique correctement configuré n'est souvent qu'un RMS-Pegel d'environ 1,7 an et a été utilisé dans un faux mappage entre ALSA et PipeWire.

---

### Liste de tâches (Future Sprint)
1. **[ ] Intégration WirePlumber :** Utilisation des règles natives PipeWire (`scripts`), pour créer un flux permanent sans crochets `pactl` pour relier.
2. **[ ] Optimisation des performances :** La boucle audio est activée (par exemple, les contrôles RMS sont effectués séparément ou les paramètres VAD sont optimisés).
3. **[ ] Native Mono Sink :** Le système Sink virtuel est sécurisé et fonctionne sur 16 kHz Mono, pour le dernier rééchantillonnage.
4. **[ ] Cartographie de périphérique robuste :** Une méthode stable trouvée, un moniteur-évier virtuel dans `sounddevice` nommément adressé.

---

### Mettre à jour `config/settings.py`
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

**[FR] Résumé :**
Tentative de fusionner l'audio du micro et du bureau à l'aide d'un « puits nul » virtuel. Le routage était instable en raison de la restauration du flux de PipeWire. Une charge CPU élevée a été observée. La logique est maintenant documentée pour une future itération.

Je suis en train de le faire, mais je vais l'utiliser dans un espace de travail avec une solution performante (vieilleicht directement sur PipeWire-Schnittstellen) Erfolg haben! Erledigt für heute.