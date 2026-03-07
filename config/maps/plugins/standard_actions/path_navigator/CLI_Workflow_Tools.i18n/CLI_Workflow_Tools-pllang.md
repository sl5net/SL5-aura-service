### Dokument Markdown: `STT/settings/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md`

__KOD_BLOKU_0__
# Funkcja otwierająca ścieżkę pliku ze schowka systemowego w Kate
funkcja k {
# Sprawdź, czy xclip jest dostępny
Jeśli ! polecenie -v xclip &> /dev/null; Następnie
echo „Błąd: xclip jest wymagany, ale nie zainstalowany.”
powrót 1
fi
XSPACEbreakX
# 1. Pobierz zawartość schowka
CLIPBOARD_CONTENT=$(xclip -schowek wyboru -o 2>/dev/null)
XSPACEbreakX
# Sprawdź, czy schowek jest pusty
jeśli [ -z "${CLIPBOARD_CONTENT}" ]; Następnie
echo "Błąd: Schowek jest pusty. Nie ma nic do otwarcia."
powrót 1
fi

# 2. Sprawdź zawartość wielowierszową (upewnij się, że używana jest tylko jedna ścieżka pliku)
LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
XSPACEbreakX
jeśli ["${LINE_COUNT}" -gt 1 ]; Następnie
echo "Błąd: Schowek zawiera ${LINE_COUNT} linii. Obsługiwane są tylko jednowierszowe ścieżki plików."
powrót 1
fi
XSPACEbreakX
# 3. Wydrukuj polecenie przed wykonaniem (opinia użytkownika)
echo "kate \"${CLIPBOARD_CONTENT}\""
XSPACEbreakX
# 4. Ostateczna egzekucja
# Podwójne cudzysłowy wokół treści poprawnie obsługują nazwy plików ze spacjami.
# Znak „&” uruchamia polecenie w tle, uwalniając terminal.
Kate „${CLIPBOARD_CONTENT}” i
}
__KOD_BLOKU_1__