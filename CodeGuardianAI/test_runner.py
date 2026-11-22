
import subprocess
import sys
import tempfile
from pathlib import Path


def run_tests(corrected_code, original_code=""):
    if "get_user_name" in original_code:
        tests = """
assert get_user_name({"name": "Alice"}) == "ALICE"
assert get_user_name(None) == ""
assert get_user_name({}) == ""
print("Tests get_user_name réussis.")
"""
    elif "calculate_average" in original_code:
        tests = """
assert calculate_average([10, 20, 30]) == 20
assert calculate_average([-5, 5]) == 0
try:
    calculate_average([])
except (ValueError, ZeroDivisionError):
    pass
else:
    raise AssertionError("La liste vide doit être gérée.")
print("Tests calculate_average réussis.")
"""
    else:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Aucun jeu de tests indépendant disponible pour ce code."
        }

    program = corrected_code + "\n\n" + tests

    with tempfile.TemporaryDirectory() as directory:
        file_path = Path(directory) / "test_code.py"
        file_path.write_text(program, encoding="utf-8")

        try:
            result = subprocess.run(
                [sys.executable, str(file_path)],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Temps maximal d'exécution dépassé."
            }
