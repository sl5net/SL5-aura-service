# Sicherheitsarchitektur: Schutz privater Daten (7.8.26 13:22 Fr)

Der Quellcode von „service_api.py“ implementiert eine dreischichtige, voneinander unabhängige Sicherheitsarchitektur zum Schutz privater Daten.

## Übersicht

| Schicht | Mechanismus | Komponente | Schutzziel |
|-------|-----------|-----------|-----------------|
| 1 | Underscore-Rule-Middleware | `service_api.py` | Zugriff auf versteckte Pfade blockieren |
| 2 | API-Schlüsselauthentifizierung | `service_api.py` | Zugriffskontrolle für Endpunkte |
| 3 | Privatsphärenmaskierung und Cache-Isolierung | `service_api.py`, `aura_cache.py` | Datenverschleierung und Cache-Trennung |

---

## Schicht 1: Unterstrich-Regel-Middleware

Jede Anfrage an Pfade oder Ordner mit einem führenden Unterstrich (z. B. „_privat“) wird von der Middleware mit **HTTP 403 Forbidden** hart blockiert.

**Fehlermeldung:**
```
Access to hidden folders (starting with '_') is forbidden.
```

Diese Regel wirkt auf Pfad-/Routing-Ebene und verhindert jeglichen Zugriff auf als privat gekennzeichnete Verzeichnisse.

---

## Schicht 2: API-Schlüsselauthentifizierung

Alle API-Endpunkte sind durch „Depends(verify_api_key)“ geschützt.

Anfragen ohne gültigen „X-API-Key“-Header werden sofort abgelehnt, bevor sie eine Geschäftslogik erreichen.

---

## Schicht 3: Privatsphärenmaskierung und Cache-Isolierung

### Maskierung
Über die API ist „unmasked = False“ die Standardeinstellung. Sensible Daten in API-Antworten werden daher automatisch maskiert.

### Cache-Isolierung
Der „cache_id“-Hash in „aura_cache.py“ wird durch den Titel des aktiven Fensters („_active_window_title“) getrennt.

**Konsequenz:** Cache-Einträge, die im lokalen Terminal erstellt wurden, können nicht über die API gelesen werden, da sie einen anderen „cache_id“-Hash besitzen.

---

## Zusammenfassung

Ihre vertraulichen Daten in „_privat“ sind somit auf allen drei Sprach- und Pfadebenen vor unbefugten API-Zugriffen geschützt:

1. **Pfadebene** – Der Zugriff auf „_“-Ordner ist blockiert
2. **Authentifizierungsebene** – Nur gültigen API-Schlüsseln wird Zugriff gewährt
3. **Datenebene** – Maskierung und Cache-Isolierung verhindern die Datenexfiltration