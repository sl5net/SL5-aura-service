# Ausführen von 0 A.D. mit Aura-Sprachsteuerung auf Systemen mit geringem RAM (Linux Mint)

Dieses Handbuch dokumentiert die Einrichtung und Speicheroptimierung für die Ausführung der Sprachsteuerung **sl5net Aura** neben **0 A.D.** auf älterer oder speicherbeschränkter Linux Mint-Hardware.

## Ziel-Hardware- und Systemprofil
- **Gerät**: Lenovo ThinkPad T520 (Laptop)
- **CPU**: Intel Core i7-2620M (Dual-Core bei 2,70 GHz – 3,40 GHz)
- **Speicher**: 5,67 GiB RAM
- **Swap**: 4 GiB effektiver Swap
- **Betriebssystem**: Linux Mint 21.3 Virginia (64-Bit)
- **Desktop-Umgebung**: Cinnamon 6.0.5 (X11 Display Server)
- **Anwendungsziel**: 0 n. Chr. (Aszendent des Imperiums)

## Speicherverwaltung und Architektur
Auf Systemen mit ≤ 6 GiB RAM erfordert die gleichzeitige Ausführung einer umfangreichen Desktop-Umgebung, eines 3D-RTS-Spiels (0 n. Chr.) und einer Spracherkennung einen strengen Speicherschutz:

1. **Priorität des Vosk-Sprachmodells**:
- Verwendet „vosk-model-small-de“ (oder eine gleichwertige Sprache) für einen geringen Speicherbedarf (~300–500 MB).
- Die Beibehaltung des Vosk-Modells hat Priorität, um die Reaktionsfähigkeit der Befehle während des Spiels in Echtzeit sicherzustellen.

2. **Automatische LanguageTool-Eviction**:
– Der Java-Prozess von LanguageTool kann ca. 1,34 GiB RSS verbrauchen.
- Wenn der verfügbare RAM unter „CRITICAL_THRESHOLD_MB“ (2,0 GiB) fällt, beendet Auras „model_manager“ LanguageTool sofort, um ~1,3 GiB RAM für das Spiel freizugeben.
- Eine 5-minütige Abklingzeit („set_lingual_tool_cooldown“) verhindert, dass LanguageTool während des aktiven Spiels neu startet und den Speicher überlastet.

## Verifizierungsbefehle
So überprüfen Sie den Systemspeicher und den Prozessstatus:
__CODE_BLOCK_0__