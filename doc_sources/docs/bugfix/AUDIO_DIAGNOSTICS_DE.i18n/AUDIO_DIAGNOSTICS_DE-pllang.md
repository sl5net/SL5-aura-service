# Wersja niemiecka: `AUDIO_DIAGNOSTICS_DE.md`

# Linux-diagnostyka audio dla aury

Beim gleichzeitigen Betrieb vom Aura Service können Audio-Konflikte auftreten (Przekroczenia limitów czasu, „Urządzenie zajęte” lub Konflikte częstotliwości próbkowania). Diese Befehle helfen bei der Fehlersuche.

### 1. Geräte identifizieren
Zeigt alle Audio-Geräte aus Sicht der Python-Umgebung an:
__KOD_BLOKU_0__
* **Ziel:** Notiere die **Index-Nummer** i die **Hardware-ID (hw:X,Y)** określa Mikrofony.

### 2. Czy sprzęt jest uszkodzony?
Wenn Fehler wie „Device Busy” lub „Timeout” auftreten, prüfe, welcher Prozess (PID) blokowanie sprzętu:
__KOD_BLOKU_1__
* **Wskazówka:** Wenn `pipewire` lub `wireplumber` erscheint, verwaltet der Sound-Server das Gerät. Wenn eine `python3` lub `obs` PID direkt auf einem PCM-Gerät erscheint, blockieren diese evtl. den Zugriff für inny.

### 3. Monitorowanie Echtzeit (PipeWire)
Für moderne Manjaro-Systeme mit PipeWire ist dies das wichtigste Tool:
__KOD_BLOKU_2__
* **Ziel:** Prüfe die Spalte `ERR` auf Fehler und stelle sicher, dass Aura (16000 Hz) i OBS (48000 Hz) keine CPU-Überlastung durch Resampling verursachen.

### 4. Überwachung von Audio-Events
Verfolge live, kiedy Mikrofone stummgeschaltet werden oder neue Streams enstehen:
__KOD_BLOKU_3__
* **Anwendung:** Starte umiera i dann Aura. Wenn sofort viele `remove`-Events kommen, bricht ein Prozess ab oder wird vom System abgewiesen.

### 5. Test bezpośredni sprzętu
Testet, ob das Mikrofon auf Hardware-Ebene funktioniert (umgeht PulseAudio/PipeWire). Nimmt 5 sekund na:
__KOD_BLOKU_4__
* **Ergebnis:** Wenn dies funktioniert, Aura aber nicht, Liegt das Problem in der Konfiguration des Sound-Servers, nicht an der Hardware.

### 6. Reset Notfall
Kompletny zestaw audio systemu Falls das:
__KOD_BLOKU_5__

---

**Wskazówka dla przepływu pracy:** Um Ausgaben direkt in Kate zu betrachten, hänge einfach `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀