# Autostart systemu Windows

# start_aura.bat

proszę sprawdzić plik `start_aura.bat` w folderze projektu SL5net Aura.

**Opcja A — Folder startowy (najprostsze, widoczne okno konsoli)**

1. Utwórz plik wsadowy, np. `C:\Users\<Twoje imię>\Scripts\aura_engine.bat`:

__KOD_BLOKU_0__

2. Naciśnij `Win + R`, wpisz `Shell:startup` i naciśnij Enter. To otwiera:
`C:\Users\<Twoja nazwa>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
3. Kliknij prawym przyciskiem myszy wewnątrz tego folderu → **Nowy → Skrót** → wskaż `aura_engine.bat`. Teraz działa przy każdym logowaniu.

**Opcja B — Harmonogram zadań (zalecane: ukryte, bez flashowania okna)**

Uruchom to raz w PowerShell:

__KOD_BLOKU_1__

Tworzy to zadanie „AuraEngine”, które uruchamia się przy każdym logowaniu, działa całkowicie w tle i zapisuje w tym samym pliku „aura_engine.log”, co jest używane w wersjach Linux/Mac.

**Testuj bez wylogowywania się:**

__KOD_BLOKU_2__

Dostosuj `Ubuntu` do swojej rzeczywistej nazwy dystrybucji — sprawdź za pomocą:

__KOD_BLOKU_3__

**Sprawdź, czy jest zarejestrowany:**

__KOD_BLOKU_4__

**Wyłącz/usuń:**

__KOD_BLOKU_5__

Czy faktycznie uruchamiasz ten projekt poprzez WSL na tym komputerze z systemem Windows, czy też wymaga on natywnego przepisania w systemie Windows/PowerShell pliku `restart_venv_and_run-server.sh` (bez użycia WSL)?