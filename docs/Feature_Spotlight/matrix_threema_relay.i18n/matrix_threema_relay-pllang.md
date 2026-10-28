> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay.md).*

# Element ↔ Threema Beta GUI Relay

Mały demon, który odzwierciedla wiadomości pomiędzy * * Element Desktop * * (Matrix) i
* * Threema Beta * * (klient pulpitu Threema) na Linuksie / X11, prowadząc obie
Windows jak użytkownik: skróty klawiszowe, schowek i kilka kliknięć myszki.

Żadnych API, żadnych żetonów, żadnych dodatkowych bibliotek Pythona. Tylko standardowe narzędzia linii X11.

# What it does

124; Kierunek 124; Co się dzieje 124;
|---|---|
* * Element → Threema Ostatnia wiadomość * ty * napisany w Element jest czytany i, jeśli jest nowy, wklejony do Threema Beta i wysłany.
* * Threema → Element Ostatnia wiadomość * przychodząca * z otwartego czatu Threema jest kopiowana przez menu kontekstowe, a jeśli jest nowa, wkleja się w Element i wysyła.

Typowe zastosowanie: dyktować lub wpisywać do pomieszczenia Element (na przykład z Aura)
speech- to- text) i aby tekst przybył w czacie Threema, i zobaczyć
Odpowiedzi na Threema pojawiają się w tym samym pomieszczeniu.

Oba Windows muszą być otwarte, zalogowane i wyświetlanie czatu / pokoju, który chcesz przekazać.

# # Loop protection

Naiwne lustro dwukierunkowe odbijałoby każdą wiadomość tam i z powrotem na zawsze. Przekaźnik
zapobiega to krótkotrwałej historii (`relay_history.py`):

1. Każdy tekst jest zapamiętywany * * przed * * jest wysyłany przez 180 sekund.
2. Jeśli tekst pojawia się po drugiej stronie, która jest w tej historii, to jest nasz własny
   echo: jest zaznaczone jako widoczne, ale * * nie * * ponownie przekazane.
3. Tekst, który jest nowy * i * nieznany jest prawdziwym przesłaniem i jest przekazywany.

Teksty są porównywane z zawaloną Whitespace, więc line- break różnice od
kopiowanie / wklejanie nie pokonuje strażnika. Ponieważ wpisy umierają, można wysłać
Ten sam tekst (na przykład "ok") ponownie po przejściu okna.

Na start- up aktualna ostatnia wiadomość z każdej strony jest odczytywana jako * * bazowy * * i jest
* not * transmited. Tylko wiadomości, które docierają po starcie są przekazywane.

# # Wymagania

- Linux z * * X11 * * (`echo $XDG_SESSION_TYPE` musi wydrukować `x11`). Wayland nie jest wspierany.
- `xdotool`, `xclip`, `wmctrl` i `xset` (opcjonalnie, używane do wyłączenia wygaszacza ekranu)
- Element Desktop (klasa WM `element.Element`)
- Threema Beta (klasa WM `threema beta.Threema Beta`, np. Flatpak)
  `ch.threema.threema-desktop`)
- Python 3 z virtualenv projektu
- `zsh` dla skryptu kalibracji jednokrotnej

# # Setup: jednorazowa kalibracja

Threema Beta rysuje własne menu kontekstowe, które nie może być obsługiwane za pomocą klawiatury,
tak przekaźnik kliknie "Kopiuj wiadomość" myszką w pozycjach względem
Okno Threema. Mierz je raz:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

Skrypt prosi o trzy pozycje myszy, każdy z odliczania (nie dotykać
Klawiatura, nie przesuwać lub zmieniać rozmiaru okna:

1. * * Prawidłowe kliknięcie * * ostatnia wiadomość * przychodząca * (bańka po lewej stronie) i zostawić
   Menu otwarte.
2. Przesuń mysz bez kliknięcia na * * "Kopiuj wiadomość" * *.
3. Przesuń mysz na pole wejścia wiadomości * *.

Wynik jest przechowywany w `~/.config/threema-relay.conf`:

124; Klucz 124; Znaczenie 124;
|---|---|
124; `FX` 124; pozioma pozycja kliknięcia jako ułamek szerokości okna 124;
124; `BOTTOM` 124; Kliknij pozycję, piksele powyżej dolnej krawędzi okna 124;
124; `DX`, `DY` X124; przesunięcie z punktu kliknięcia na "Kopiuj wiadomość" 124;
`INPUT_FX`, `INPUT_BOTTOM` X124; Pozycja pola wprowadzania wiadomości XINLINECODEX;
`DELAY_MENU`, `DELAY_COPY` X124; Opcjonalnie czeka w sekundach (domyślnie 0.30 / 0.20) XINLINECODEX 124;

Sprawdź kalibrację za pomocą nowej przychodzącej wiadomości jako ostatniej w czacie:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

Drukuje skopiowany tekst bez jego przesyłania dalej. Kalibracja opiera się na oknie
geometria: jeśli zmienisz rozmiar okna Threema dużo, skalibruj ponownie.

## Użytkowanie

Z katalogu głównego repozytorium:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

Opcje:

| Opcja | Efekt |
|---|---|
| `--poll SECONDS` | Interwał ankiety (domyślnie `2.0`) |
| `--no-threema-to-element` | Tylko element przekaźnika → Threema |
| `--no-element-enter` | Wklej wiadomości Threema do pola wprowadzania Element, ale **nie** wysyłaj ich (bezpieczny tryb testowy) |

Przestań z `Ctrl+C`.

Zalecany pierwszy przebieg: użyj `--no-element-enter`, wyślij sobie wiadomość w Threemie
i sprawdź, czy pojawia się w polu wprowadzania Elementu. Następnie uruchom bez tej opcji.

Przykładowy log:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

Jak to działa

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- * W górę * w kompozytorze Element edytuje ostatnią wiadomość; * Ctrl + A / Ctrl + C * kopie
  to i * Escape * opuszcza tryb edycji. To dlatego tylko * * twój własny * * ostatni element
  Wiadomość jest przekazywana Threemie.
- Dla Threema a * * Sentinel string * * jest najpierw umieszczany w schowku. Jeśli nadal jest
  tam następnie, nic nie zostało skopiowane (na przykład ponieważ Twój własny komunikat jest
  Ostatni i kliknij nie ma bańki) i próba jest ignorowana.

## Pliki

XI124; Plik XI124; Cel XI124;
|---|---|
124; `matrix_threema_relay.py` 124; pętla główna, CLI, logika decyzji (`classify_candidate`) 124;
Read Element 's last own message
`send_to_threema_window.py` XINLINEDE3X X124; Wkleja tekst do Threema Beta XI124;
124; `read_last_threema_message.py` 124; odczytuje ostatnią wiadomość przychodzącą Threemy, ładuje kalibrację 124;
`send_to_element_window.py` `send_to_element_window.py` X124; Wkleja tekst do Elementu XIINLINECODE5X XIR
124; `relay_history.py` 124; ochrona pętli 124;
124; `threema-relay.zsh` 124; narzędzie do kalibracji i ręcznego testowania (`calibrate`, `test`) 124;
124; `test_threema_relay.py` X124; Testy jednostkowe (nie wymagane X11) X124;

Uruchom testy za pomocą:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

# # Ograniczenia

- * * Przekaźnik wykorzystuje ostrość myszy i klawiatury. / Podczas każdego badania Threema i
  Element Windows są skoncentrowane i mysz skacze krótko (jest przywrócony). Nie należy
  wpisz podczas trwania ankiety lub użyj dłuższego `--poll`.
- Przepisuje notatnik na każdym ankiecie.
- * * Own message last in Threema: * * when your own message is the last in the Threema
  Chat, odpowiedź, która dotarła tuż przed tym, jak jej nie widać.
- * * Tylko ostatnia wiadomość * * jest odczytywana na ankietę. Jeśli kilka wiadomości pojawi się w jednym
  interwał, tylko najnowszy jest przekazywany.
- * * Tylko tekst. * * Obrazy, pliki, reakcje i edycje nie są przekazywane.
- * * One chat pair * * Jakiekolwiek czat / pokój jest otwarty w każdym oknie jest używany.
- * * Projekt w polu wejściowym Element * * zostanie połączony z następnym wklejonym
  Wiadomość.
- Tylko X11. Wayland blokuje syntetyczne wejście i zmiany ostrości okna.
- Przekaźnik wyłącza wygaszacz ekranu X11 i DPMS na starcie (`xset s off -dpms`);
  Trzymają się z dala, dopóki nie włączysz ich ponownie lub zalogujesz się ponownie.

## Rozwiązywanie problemów

124; Symptom 124; Prawdopodobna przyczyna / fix 124;
|---|---|
124; `Threema window ... not found` 124; Sprawdź `xdotool search --class "Threema Beta"` i `xprop WM_CLASS` (kliknij okno).
Rerun `calibrate`; uruchomić `test` z komunikatem przychodzącym jako ostatni. Zwiększ `DELAY_MENU` / `DELAY_COPY` w konfiguracji na wolnym komputerze.
`INPUT_FX` / `INPUT_BOTTOM` z kalibracji
tekst Threema pojawia się w elemencie, ale nie jest wysyłany do 124; Przekaźnik został uruchomiony z `--no-element-enter`.
Written by a older script version under a German locale. Kod Pythona akceptuje je; Kalibracja ponownie z aktualnym skryptem pisze kropki. VIId;
