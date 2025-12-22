# config/maps/plugins/standard_actions/de-DE/calculator.py
# STT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/calculator.py
def execute(match_data):
    """ Führt eine einfache Berechnung durch, basierend auf Regex-Gruppen. """
    try:
        match_obj = match_data['regex_match_obj']

        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        result = 0
        if operator == "plus" or operator == "+":
            result = num1 + num2
        elif operator == "minus" or operator == "-":
            result = num1 - num2
        elif operator == "mal" or operator == "*":
            result = num1 * num2
        elif operator == "geteilt durch" or operator == "/":
            if num2 == 0:
                return "Ich kann nicht durch Null teilen, das gibt nur Ärger."
            result = num1 / num2

        return f"Das Ergebnis von {num1} {operator} {num2} ist {result}."

    except (IndexError, ValueError):
        return f"Ich konnte die Zahlen in deiner Frage nicht verstehen. num1:{num1} operator:{operator} num2:{num2}"

