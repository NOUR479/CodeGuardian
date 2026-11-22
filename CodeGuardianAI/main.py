# code 1

# import os

# from dotenv import load_dotenv
# from google import genai

# # Charger les variables du fichier .env
# load_dotenv()

# # Récupérer la clé API
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError(
#         "Clé API absente. Vérifie ton fichier .env."
#     )

# # Créer le client API
# client = genai.Client(api_key=api_key)

# # Exemple de code contenant un bug
# code = """
# def calculate_average(numbers):
#     return sum(numbers) / len(numbers)

# print(calculate_average([]))
# """

# # Définir la consigne envoyée au modèle
# prompt = f"""
# Tu es un assistant spécialisé en analyse de code Python.

# Analyse le code suivant.

# 1. Identifie les bugs potentiels.
# 2. Explique pourquoi ils se produisent.
# 3. Propose une correction.
# 4. Donne un test permettant de vérifier la correction.

# Ne prétends pas avoir exécuté le code.

# Code à analyser :
# ```python
# {code}
# ```
# """

# # Envoyer la requête à l'API
# response = client.models.generate_content(
#     model="gemini-3.8-flash",
#     contents=prompt,
# )

# # Afficher la réponse
# print("=== Analyse de CodeGuardian AI ===")
# print(response.text)

#code2

# import os
# import json

# from dotenv import load_dotenv
# from google import genai

# # 1. Charger la clé API
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("La clé GEMINI_API_KEY est absente.")

# # 2. Initialiser le client
# client = genai.Client(api_key=api_key)

# # 3. Code à analyser
# code = """
# def get_user_name(user):
#     return user["name"].upper()

# print(get_user_name(None))
# """

# # 4. Demander un diagnostic structuré
# prompt = f"""
# Tu es un expert en analyse de code Python.

# Analyse le code fourni et retourne UNIQUEMENT un objet JSON valide
# respectant exactement cette structure :

# {{
#     "bug_found": true,
#     "bug_type": "ZeroDivisionError",
#     "severity": "high",
#     "explanation": "Explication du problème",
#     "fix_code": "Code Python corrigé",
#     "tests": [
#         "assert calculate_average([10, 20]) == 15"
#     ],
#     "uncertainties": []
# }}

# Règles :
# - bug_found est un booléen.
# - bug_type est une chaîne ou null.
# - severity vaut low, medium, high ou critical.
# - explanation et fix_code sont des chaînes.
# - tests et uncertainties sont des listes de chaînes.
# - Les tests doivent correspondre au code corrigé.
# - Ne prétends pas avoir exécuté les tests.
# - Si aucun bug n'est détecté, utilise false pour bug_found.

# Code à analyser :
# {code}
# """

# # 5. Appeler l'API en demandant du JSON
# response = client.models.generate_content(
#     model="gemini-3.5-flash-lite",
#     contents=prompt,
#     config={
#         "response_mime_type": "application/json"
#     }
# )

# # 6. Convertir le JSON en dictionnaire Python
# try:
#     report = json.loads(response.text)

#     # Vérifier les champs indispensables
#     required_fields = {
#         "bug_found",
#         "bug_type",
#         "severity",
#         "explanation",
#         "fix_code",
#         "tests",
#         "uncertainties",
#     }

#     if not isinstance(report, dict):
#         raise ValueError("Le résultat JSON doit être un objet.")

#     if not required_fields.issubset(report.keys()):
#         raise ValueError("Il manque des champs dans le diagnostic.")

#     if not isinstance(report["bug_found"], bool):
#         raise ValueError("bug_found doit être un booléen.")

#     if report["severity"] not in {
#         "low", "medium", "high", "critical"
#     }:
#         raise ValueError("Niveau de gravité invalide.")

#     if not all(
#         isinstance(report[field], str)
#         for field in ("explanation", "fix_code")
#     ):
#         raise ValueError("Le diagnostic contient des champs invalides.")

#     if not all(
#         isinstance(report[field], list)
#         and all(isinstance(item, str) for item in report[field])
#         for field in ("tests", "uncertainties")
#     ):
#         raise ValueError("Les tests ou incertitudes sont invalides.")

# except (json.JSONDecodeError, ValueError, TypeError) as error:
#     print("Diagnostic invalide :", error)
#     raise SystemExit(1)

# # 7. Afficher le diagnostic
# print("\n=== CODEGUARDIAN AI ===")
# print("Bug détecté :", report["bug_found"])
# print("Type :", report["bug_type"])
# print("Gravité :", report["severity"])
# print("\nExplication :")
# print(report["explanation"])
# print("\nCorrection proposée :")
# print(report["fix_code"])
# print("\nTests proposés :")

# for test in report["tests"]:
#     print("-", test)

# print("\nIncertitudes :")

# for uncertainty in report["uncertainties"]:
#     print("-", uncertainty)




# code 3

# import os
# import json

# from dotenv import load_dotenv
# from google import genai
# from test_runner import run_tests


# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("La clé GEMINI_API_KEY est absente.")

# client = genai.Client(api_key=api_key)

# # Code volontairement incorrect
# code = """
# def get_user_name(user):
#     return user["name"].upper()

# print(get_user_name(None))
# """

# prompt = f"""
# Tu es un expert en correction de bugs Python.

# Analyse ce code et propose une correction.

# Retourne uniquement un JSON avec ces champs :
# - bug_found : booléen
# - bug_type : chaîne ou null
# - severity : low, medium, high ou critical
# - explanation : chaîne
# - fix_code : code Python complet corrigé
# - uncertainties : liste de chaînes

# Le code corrigé doit conserver la fonction get_user_name
# et retourner une chaîne vide si user est None ou si la clé
# name est absente.

# Ne prétends pas avoir exécuté le code.

# Code à analyser :
# {code}
# """

# response = client.models.generate_content(
#     model="gemini-3.5-flash-lite",
#     contents=prompt,
#     config={"response_mime_type": "application/json"},
# )

# try:
#     report = json.loads(response.text)

#     if not isinstance(report, dict):
#         raise ValueError("Le diagnostic doit être un objet JSON.")

#     fix_code = report.get("fix_code")

#     if not isinstance(fix_code, str) or not fix_code.strip():
#         raise ValueError("Le correctif est absent ou invalide.")

#     if len(fix_code) > 10000:
#         raise ValueError("Le correctif est trop volumineux.")

# except (json.JSONDecodeError, ValueError, TypeError) as error:
#     print("Diagnostic invalide :", error)
#     raise SystemExit(1)

# print("\n=== 1. ANALYSE GEMINI ===")
# print("Bug détecté :", report.get("bug_found"))
# print("Type :", report.get("bug_type"))
# print("Gravité :", report.get("severity"))
# print("Explication :", report.get("explanation"))

# print("\n=== 2. CORRECTION PROPOSÉE ===")
# print(fix_code)

# print("\n=== 3. EXÉCUTION DES TESTS ===")
# result = run_tests(fix_code)

# print(result["stdout"])

# if result["success"]:
#     print("VERDICT : TESTS RÉUSSIS")
# else:
#     print("VERDICT : ÉCHEC DES TESTS")
#     print(result["stderr"])

# print("\n=== 4. RAPPORT FINAL ===")
# if result["success"]:
#     print("Le correctif passe tous les tests définis.")
# else:
#     print("Le correctif ne passe pas tous les tests.")

# print("Attention : cela ne prouve pas l'absence de tous les bugs.")





# code 4
 
import os
import json

from dotenv import load_dotenv
from google import genai
from test_runner import run_tests
from report_manager import save_report, show_history

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY est absente du fichier .env")

client = genai.Client(api_key=api_key)
MODEL = "gemini-3.8-flash"
MAX_ATTEMPTS = 3


def analyze_code(code, previous_error=""):
    prompt = f"""
Tu es CodeGuardian AI, un assistant expert en débogage Python.

Analyse le code et retourne uniquement un JSON valide contenant :
- bug_found : bool
- bug_type : string
- severity : low, medium, high ou critical
- explanation : string
- fix_code : code Python complet corrigé
- uncertainties : liste de chaînes

Contraintes :
- Conserve le comportement attendu du programme.
- Pour get_user_name, retourne "" si user est None
  ou si la clé name est absente.
- Ne prétends jamais avoir exécuté le code.
- Si un test a échoué, corrige le problème indiqué.

Erreur des tests précédents :
{previous_error}

Code à analyser :
{code}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )

    report = json.loads(response.text)

    if not isinstance(report, dict):
        raise ValueError("Le rapport JSON doit être un objet.")

    fix_code = report.get("fix_code")

    if not isinstance(fix_code, str) or not fix_code.strip():
        raise ValueError("Gemini n'a pas fourni de correction valide.")

    if len(fix_code) > 10000:
        raise ValueError("Le code corrigé est trop volumineux.")

    return report


def main():
    print("=" * 50)
    print("       CODEGUARDIAN AI")
    print("   Analyse et correction de bugs Python")
    print("=" * 50)

    choice = input("\n1. Analyser du code\n2. Consulter l'historique\nChoix : ")

    if choice == "2":
        show_history()
        return

    if choice != "1":
        print("Choix invalide.")
        return

    print("=" * 50)

    print("\nColle ton code Python.")
    print("Tape END sur une ligne seule pour terminer.\n")

    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip() == "END":
            break

        lines.append(line)

    code = "\n".join(lines)

    if not code.strip():
        print("Aucun code fourni.")
        return

    previous_error = ""

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n--- ANALYSE {attempt}/{MAX_ATTEMPTS} ---")

        try:
            report = analyze_code(code, previous_error)
        except Exception as error:
            print("Erreur pendant l'appel à Gemini ou le traitement JSON.")
            print("Détail :", str(error))
            return

        print("Bug détecté :", report.get("bug_found"))
        print("Type :", report.get("bug_type"))
        print("Gravité :", report.get("severity"))
        print("Explication :", report.get("explanation"))
        print("Incertitudes :", report.get("uncertainties", []))

        print("\n--- CORRECTION PROPOSÉE ---")
        print(report["fix_code"])

        print("\n--- TESTS AUTOMATIQUES ---")
        result = run_tests(report["fix_code"], code)

        if result["stdout"]:
            print(result["stdout"])

        if result["success"]:
            print("VERDICT : TESTS RÉUSSIS")
            print("Le correctif passe les tests configurés.")
            break

        print("VERDICT : ÉCHEC DES TESTS")
        previous_error = result["stderr"] or result["stdout"]
        print(previous_error)

        if attempt < MAX_ATTEMPTS:
            print("Nouvelle tentative de correction...")
    else:
        print("\nÉCHEC : aucune correction n'a passé les tests.")

    try:
        path = save_report(code, report, result, attempt)
        print("Rapport enregistré :", path)
    except (OSError, TypeError, ValueError) as error:
        print("Impossible d'enregistrer le rapport :", error)

    print("\n--- RAPPORT FINAL ---")
    print("Tentatives effectuées :", attempt)
    print("Tests réussis :", result["success"])
    print("Attention : réussir ces tests ne garantit pas "
          "l'absence de tous les bugs.")


if __name__ == "__main__":
    main()
 