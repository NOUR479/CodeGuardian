
import json
from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path("reports")


def save_report(code, diagnosis, test_result, attempts):
    REPORTS_DIR.mkdir(exist_ok=True)

    report = {
        "date": datetime.now().astimezone().isoformat(),
        "original_code": code,
        "diagnosis": diagnosis,
        "tests": test_result,
        "attempts": attempts
    }

    filename = datetime.now().strftime("report_%Y%m%d_%H%M%S_%f.json")
    path = REPORTS_DIR / filename

    path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    return path


def show_history():
    REPORTS_DIR.mkdir(exist_ok=True)
    files = sorted(REPORTS_DIR.glob("report_*.json"), reverse=True)

    if not files:
        print("Aucun rapport enregistré.")
        return

    for file in files:
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            diagnosis = data.get("diagnosis", {})
            tests = data.get("tests", {})

            print(f"\nRapport : {file.name}")
            print("Date :", data.get("date", "Inconnue"))
            print("Bug :", diagnosis.get("bug_type", "Inconnu"))
            print("Tests réussis :", tests.get("success", False))
        except (OSError, json.JSONDecodeError):
            print(f"Rapport illisible : {file.name}")
