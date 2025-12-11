# config/maps/plugins/wannweil/de-DE/calculator.py

def execute(match_data):
    """ Führt eine einfache Berechnung durch, basierend auf Regex-Gruppen. """
    try:
        match_obj = match_data['regex_match_obj']

        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        result = 0
        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        elif operator == "mal":
            result = num1 * num2
        elif operator == "geteilt durch":
            if num2 == 0:
                return "Ich kann nicht durch Null teilen, das gibt nur Ärger."
            result = num1 / num2

        return f"Das Ergebnis von {num1} {operator} {num2} ist {result}."

    except (IndexError, ValueError):
        return "Ich konnte die Zahlen in deiner Frage nicht verstehen."

