# Pierwsze kroki w systemie Windows

## Krok 1: Uruchom instalację
Kliknij dwukrotnie plik `setup/windows11_setup_with_ahk_copyq.bat`.
- Kliknij prawym przyciskiem myszy → „Uruchom jako administrator”, jeśli pojawi się monit.
- Skrypt instaluje Python, AutoHotkey v2, CopyQ i pobiera modele głosowe (~4 GB).
- Zajmuje to około 8-10 minut.

## Krok 2: Uruchom Aurę
Kliknij dwukrotnie plik `start_aura.bat` w folderze projektu.
Powinieneś usłyszeć dźwięk uruchamiania — Aura jest gotowa.

**Nic się nie stało?** Sprawdź dziennik:
log\aura_engine.log

## Krok 3: Skonfiguruj swój skrót
Instalator automatycznie instaluje CopyQ. Aby włączyć dyktowanie:
1. Otwórz CopyQ → Polecenia → Dodaj polecenie
2. Ustaw polecenie na:
cmd /c echo. > C:\tmp\sl5_record.trigger
3. Przypisz globalny skrót (np. `F9`)

## Krok 4: Pierwsze dyktando
1. Kliknij dowolne pole tekstowe
2. Naciśnij klawisz skrótu — poczekaj na powiadomienie „Słucham…”
3. Powiedz „Witaj, świecie”
4. Naciśnij ponownie klawisz skrótu — pojawi się tekst

## Krok 5: Znajdź polecenia głosowe
Powiedz: **„Wyszukiwanie aury”** — otworzy się okno ze wszystkimi dostępnymi regułami.

## Rozwiązywanie problemów
| Objaw | Napraw |
|---|---|
| Brak dźwięku uruchamiania | Sprawdź `log\aura_engine.log` |
| Klawisz skrótu nic nie robi | Sprawdź, czy utworzono `C:\tmp\sl5_record.trigger` |
| Tekst nie wpisany | Sprawdź, czy `type_watcher.ahk` jest uruchomiony w Menedżerze zadań |
| Awaria na starcie | Uruchom instalację ponownie jako Administrator |

> Pełne rozwiązywanie problemów: [TROUBLESHOOTING.md](../../TROUBLESHOOTING.i18n/TROUBLESHOOTING-pllang.md)