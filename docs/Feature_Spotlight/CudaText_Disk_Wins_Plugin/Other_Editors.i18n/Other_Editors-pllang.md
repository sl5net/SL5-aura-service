# Automatyczne przeładowanie w innych edytorach

W tym dokumencie opisano, jak skonfigurować automatyczne przeładowywanie na urządzeniu zewnętrznym
zmiany plików w popularnych edytorach — i dlaczego to często **nie wystarczy**
w trybie Aura Oma.

---

## Kate (KDE)

### Organizować coś

1. **Ustawienia → Konfiguruj Kate → Otwórz/Zapisz → Zaawansowane**
2. Włącz:
- **„Automatycznie przeładuj pliki”**

### Co działa

- Gdy bufor jest **niezmieniony**, Kate natychmiast ładuje plik ponownie.
- To wystarczy do czystego trybu przeglądania.

### Co **nie** działa (i dlaczego nie działa w trybie Oma)

- Gdy tylko naciśniesz **pojedynczy klawisz** w buforze (nawet tylko
spacja lub przypadkowe naciśnięcie klawisza), bufor jest uważany za „zmodyfikowany”.
- Od tego momentu Kate **zawsze** przy każdej zewnętrznej zmianie pyta:
> "Plik został zmieniony zewnętrznie. Czy chcesz go załadować ponownie?"
- W trybie Oma użytkownik może nie być przy komputerze lub może nie widzieć
dialog — Aura pisze dalej, ale edytor pozostaje na starej wersji.
- **Kate nie ma ustawienia**, które dyskretnie odrzuca niezapisane zmiany bufora
na korzyść wersji dyskowej.

> **Konkluzja:** Kate nie nadaje się do trybu Oma, gdy tylko użytkownik
> przypadkowo wpisałem w edytorze.

---

## Kod VS

### Organizować coś

W `settings.json`:

__KOD_BLOKU_0__

### Ograniczenia

- `autoSave` zapisuje bufor — nadpisuje zmiany Aury plikiem
wersja lokalna, a nie odwrotnie.
- Nadal pojawia się monit o niezapisane zmiany.
- Brak opcji "dysk zawsze wygrywa".

---

## Emacs

__KOD_BLOKU_1__

### Ograniczenia

- Ładuje się automatycznie tylko wtedy, gdy bufor pozostaje niezmieniony.
- Pyta, kiedy bufor jest modyfikowany.

---

## Vim/Neovim

__KOD_BLOKU_2__

### Ograniczenia

- `autoread` ładuje się ponownie tylko wtedy, gdy bufor jest niezmieniony.
- Nie zastępuje automatycznie „zmodyfikowanego” bufora.

---

## CudaText (bez wtyczki)

W `user.json`:

__KOD_BLOKU_3__

### Ograniczenia

- Wszystkie wartości `ui_notif_confirm` (0–4) pokazują jakąś formę podpowiedzi —
modalne lub bezmodalne.
- Nie ma wartości **nie**, która oznacza: „Załaduj natychmiast, nigdy nie pytaj”.
- Dlatego wymagana jest wtyczka `cuda_disk_wins`.

---

## Przegląd

| Redaktor | Automatyczne przeładowanie (bez zmian) | Automatyczne przeładowanie (zmodyfikowane) | Licencja |
|--------|------------------------------|----------------------|--------|
| Kate | Tak | Zawsze pyta | Otwarte źródło |
| Kod VS | Tak | Zawsze pyta | Otwarte źródło |
| Wzniosły tekst | Tak | Zawsze pyta | Zastrzeżone |
| Emacs | Tak | Zawsze pyta | Otwarte źródło |
| Vim | Tak | Zawsze pyta | Otwarte źródło |
| CudaText (bez wtyczki) | Tak | Zawsze pyta | Otwarte źródło |
| **CudaText + wygrane na dysku** | Tak | **Brak podpowiedzi** | Otwarte źródło |

---

## Dlaczego żaden redaktor nie może tego zrobić od razu po wyjęciu z pudełka

Ciche odrzucanie niezapisanych zmian jest uważane za **ogromną utratę danych
błąd** w tworzeniu oprogramowania. Żaden poważny edytor nie oferuje ustawień
„zastąp mój bufor bez pytania”. To jest słuszne i ważne –
do normalnej pracy programisty.

Jednakże w trybie Aura Oma priorytet jest odwrotny: aura jest źródłem
prawdy, a bufor edytora ludzkiego jest drugorzędny. Dlatego też
Aby wymusić to zachowanie, wymagana jest wyraźna interwencja wtyczki
ten konkretny przypadek użycia.