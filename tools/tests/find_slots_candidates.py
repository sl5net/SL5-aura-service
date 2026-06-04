import ast
import os

# Signalwörter für Klassen, von denen es meistens VIELE Instanzen gibt
GOOD_KEYWORDS = ['Event', 'Token', 'Data', 'Message', 'Payload', 'Model', 'Item', 'State', 'Info']

# Signalwörter für Klassen, von denen es meistens nur EINE Instanz gibt (Singletons)
BAD_KEYWORDS = ['Manager', 'Service', 'Handler', 'Controller', 'Engine', 'App', 'Factory', 'System']

def is_dataclass(class_node):
    """Prüft, ob die Klasse eine Dataclass ist und ob slots=True fehlt."""
    for dec in class_node.decorator_list:
        # Check für @dataclass
        if isinstance(dec, ast.Name) and dec.id == 'dataclass':
            return True, "Ist eine @dataclass (Perfekter Kandidat!)"
        # Check für @dataclass(kwarg=...)
        if isinstance(dec, ast.Call) and getattr(dec.func, 'id', '') == 'dataclass':
            # Prüfen, ob slots=True schon gesetzt ist
            has_slots = any(
                k.arg == 'slots' and
                (isinstance(k.value, ast.Constant) and k.value.value is True)
                for k in dec.keywords
            )
            if not has_slots:
                return True, "Ist eine @dataclass (ohne slots=True -> Perfekter Kandidat!)"
    return False, ""

def analyze_class(class_node, filepath):
    name = class_node.name

    # 1. Ist es ein Manager/Service? -> Ignorieren
    if any(bad in name for bad in BAD_KEYWORDS):
        return None

    # 2. Ist es eine Dataclass? -> Sofort vorschlagen
    is_dc, reason = is_dataclass(class_node)
    if is_dc:
        return reason

    # 3. Hat es einen verdächtig guten Namen?
    if any(good in name for good in GOOD_KEYWORDS):
        return f"Namenskonvention deutet auf Daten-Objekt hin ('{name}')"

    # 4. Struktur-Analyse: Nur __init__ und kaum andere Methoden?
    methods = [m for m in class_node.body if isinstance(m, ast.FunctionDef)]
    if methods:
        # Wenn die Klasse eine __init__ hat und insgesamt sehr klein ist (z.B. max 3 Methoden)
        has_init = any(m.name == '__init__' for m in methods)
        if has_init and len(methods) <= 3:
            return "Kleine Klasse, hauptsächlich Datenstruktur (wenig Methoden)"

    return None

def find_candidates(directory):
    exclude_dirs = {'.venv', '.git', '.env', 'venv', '__pycache__', 'doc_sources'}



    candidates = []

    for root, dirs, files in os.walk(directory):
        # Ignoriere versteckte Ordner und Venvs
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=filepath)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            reason = analyze_class(node, filepath)
                            if reason:
                                candidates.append((filepath, node.name, reason))
                except Exception:
                    pass # Parse-Fehler überspringen (z.B. bei ungültiger Syntax)

    # Ergebnisse formatiert ausgeben
    print("=== POTENZIELLE KANDIDATEN FÜR __slots__ ===\n")
    if not candidates:
        print("Keine eindeutigen Kandidaten gefunden.")
        return

    # Nach Dateipfad sortieren, damit es übersichtlich ist
    candidates.sort(key=lambda x: x[0])

    for filepath, class_name, reason in candidates:
        print(f"Datei:  {filepath}")
        print(f"Klasse: {class_name}")
        print(f"Grund:  {reason}")
        print("-" * 50)

if __name__ == '__main__':
    find_candidates('.')
