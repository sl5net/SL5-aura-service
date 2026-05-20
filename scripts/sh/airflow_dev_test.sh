#!/usr/bin/env zsh
# =============================================================================
# airflow_dev_test.sh
# Schnelles Testen von Aura Airflow DAGs ohne CLI-Overhead.
# Verwendung: ./scripts/sh/airflow_dev_test.sh [dag_id] [task_id]
# Beispiel:   ./scripts/sh/airflow_dev_test.sh aura_quiz_validation
# =============================================================================

set -euo pipefail

export LANG=de_DE.UTF-8
export LC_ALL=de_DE.UTF-8

# --- Farben ---
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

if [ "${OS:-}" = "Windows_NT" ] || [ -n "${WINDIR:-}" ]; then
  tmp_dir='C:/tmp'
else
  tmp_dir='/tmp'
fi
PROJECT_ROOT="$(realpath "$(tr -d '\r' < "$tmp_dir/sl5_aura/sl5net_aura_project_root")")"


DAG_ID="${1:-aura_quiz_validation}"
TASK_ID="${2:-}"

echo "${YELLOW}=== Aura Airflow Dev-Test ===${NC}"
echo "Project Root : $PROJECT_ROOT"
echo "DAG          : $DAG_ID"

# --- .venv aktivieren ---
source "$PROJECT_ROOT/.venv/bin/activate"
export AIRFLOW_HOME="$PROJECT_ROOT/orchestration"
export AIRFLOW__CORE__DAGS_FOLDER="$PROJECT_ROOT/orchestration/dags"

# --- DAG parsen (schnellster Check) ---
echo "\n${YELLOW}[1/3] Parse-Check...${NC}"
python3 "$PROJECT_ROOT/orchestration/dags/aura_orchestration_dag.py" 2>&1 \
  | grep -v "DeprecatedImportWarning\|deprecated\|py.warnings" \
  | grep -v "^$" || true
echo "${GREEN}✅ Parse OK${NC}"

# --- Schema-Validierung direkt testen ---
echo "\n${YELLOW}[2/3] Quiz-Schema-Validierung...${NC}"
python3 - << 'PYEOF'
import sys, json
sys.path.insert(0, ".")
# Warnings unterdrücken
import warnings; warnings.filterwarnings("ignore")
from orchestration.dags.aura_orchestration_dag import _validate_quiz_schema, QUIZ_DB_PATH

if not QUIZ_DB_PATH.exists():
    print(f"❌ quiz_db.json nicht gefunden: {QUIZ_DB_PATH}")
    sys.exit(1)

data = json.loads(QUIZ_DB_PATH.read_text(encoding="utf-8"))
errors = _validate_quiz_schema(data)
if errors:
    print(f"❌ Schema ungültig ({len(errors)} Fehler):")
    for e in errors:
        print(f"   - {e}")
    sys.exit(1)
else:
    print(f"✅ Schema valid! {len(data)} Frage(n) gefunden.")
PYEOF

# --- ZIM-Check testen ---
echo "\n${YELLOW}[3/3] ZIM-Datei-Check...${NC}"
python3 - << 'PYEOF'
import sys, warnings; warnings.filterwarnings("ignore")
from orchestration.dags.aura_orchestration_dag import ZIM_WATCH_DIR
zim = ZIM_WATCH_DIR / "wikipedia_de_all_mini.zim"
if zim.exists():
    mb = zim.stat().st_size / (1024**2)
    print(f"✅ ZIM gefunden: {zim} ({mb:.1f} MB)")
else:
    print(f"⚠️  ZIM nicht gefunden (normal): {zim}")
    print("   → Pipeline würde mit AirflowSkipException übersprungen.")
PYEOF

echo "\n${GREEN}=== Dev-Test abgeschlossen ===${NC}"
echo "Tipp: 'airflow dags reserialize' nach DAG-Änderungen ausführen."
