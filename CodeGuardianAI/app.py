
import json
from pathlib import Path

import streamlit as st

from main import analyze_code
from test_runner import run_tests
from report_manager import save_report


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CodeGuardian AI | Intelligent Code Review",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

REPORTS_DIR = Path("reports")

# =========================================================
# DESIGN CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #0b1020;
    --panel: #121a2e;
    --panel-light: #18233b;
    --border: #263451;
    --text: #edf2ff;
    --muted: #94a3bd;
    --accent: #8b7cff;
    --cyan: #4dd9e8;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #20234a 0%, transparent 35%),
        radial-gradient(ellipse at 90% 10%, #102d42 0%, transparent 30%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

p, li, label {
    color: #c4cee2;
}

[data-testid="stHeader"] {
    background: rgba(11, 16, 32, 0.85);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #0d1426;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 24px 4px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    font-size: 25px;
    background: linear-gradient(135deg, #8173ff, #35cfe1);
    box-shadow: 0 8px 30px #6558ff35;
}

.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f4f6ff;
}

.brand-subtitle {
    font-size: 11px;
    color: #91a0bd;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.hero {
    padding: 34px;
    border: 1px solid #344168;
    border-radius: 24px;
    background: linear-gradient(125deg, #1b2342 0%, #151d33 55%, #102b3a 100%);
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}

.hero-tag {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 30px;
    background: #8b7cff20;
    border: 1px solid #8b7cff55;
    color: #c4bcff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: clamp(30px, 4vw, 46px);
    line-height: 1.15;
    margin: 0 0 14px 0;
}

.hero p {
    font-size: 15px;
    line-height: 1.8;
    color: #b7c4dc;
    max-width: 720px;
    margin-bottom: 0;
}

.gradient-text {
    background: linear-gradient(90deg, #a69bff, #55dce8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.section-title {
    font-size: 23px;
    font-weight: 700;
    margin: 22px 0 6px 0;
}

.section-description {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 20px;
}

.feature-card {
    background: linear-gradient(145deg, #172139, #111a2d);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 22px;
    min-height: 160px;
}

.feature-icon {
    font-size: 26px;
    margin-bottom: 12px;
}

.feature-title {
    color: #f0f3ff;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
}

.feature-text {
    color: #9eacc6;
    font-size: 13px;
    line-height: 1.7;
}

.panel {
    background: #121a2e;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.status-pill {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
}

.status-ok {
    background: #123d35;
    color: #68e5b9;
    border: 1px solid #226b59;
}

.status-warning {
    background: #49351b;
    color: #ffd18a;
    border: 1px solid #7c5828;
}

.status-danger {
    background: #4a222d;
    color: #ff9cac;
    border: 1px solid #7c3446;
}

div[data-testid="stMetric"] {
    background: #151f35;
    border: 1px solid var(--border);
    padding: 18px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #a9b7d0;
}

div[data-testid="stMetricValue"] {
    color: #f2f5ff;
    font-family: 'Space Grotesk', sans-serif;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 11px;
    min-height: 43px;
    font-weight: 700;
    border: 1px solid #3a4565;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #7968f8, #387fda);
    color: white;
    border: none;
    box-shadow: 0 6px 22px #6254f530;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #9a8dff;
    color: white;
    transform: translateY(-1px);
}

.stTextArea textarea {
    background: #090f1d !important;
    color: #dce8ff !important;
    border: 1px solid #33415f !important;
    border-radius: 13px !important;
    font-family: Consolas, 'Courier New', monospace !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

.stTextArea textarea:focus {
    border-color: #8b7cff !important;
    box-shadow: 0 0 0 1px #8b7cff !important;
}

[data-testid="stExpander"] {
    background: #121a2e;
    border: 1px solid var(--border);
    border-radius: 13px;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #293650;
}

.footer {
    text-align: center;
    color: #71809d;
    font-size: 12px;
    padding: 30px 0 5px 0;
}

.small-label {
    color: #94a3bd;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
}

div[data-testid="stRadio"] label {
    color: #d8e1f5;
}

@media (max-width: 768px) {
    .hero {
        padding: 23px;
    }
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# FONCTIONS UTILITAIRES
# =========================================================

def load_reports():
    if not REPORTS_DIR.exists():
        return []

    reports = []

    for file in sorted(
        REPORTS_DIR.glob("report_*.json"),
        reverse=True,
    ):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            data["_filename"] = file.name
            reports.append(data)
        except (OSError, json.JSONDecodeError):
            continue

    return reports


def severity_class(severity):
    severity = str(severity).lower()

    if severity in ("low", "faible"):
        return "status-ok"

    if severity in ("medium", "moyenne", "moyen"):
        return "status-warning"

    return "status-danger"


def show_footer():
    st.markdown("""
    <div class="footer">
        CODEGUARDIAN AI &nbsp;•&nbsp; Intelligent Code Analysis
        <br><br>
        Built with Python, Streamlit and Google Gemini
    </div>
    """, unsafe_allow_html=True)


def show_hero(title, description, tag="AI-POWERED CODE ANALYSIS"):
    st.markdown(f"""
    <div class="hero">
        <div class="hero-tag">✦ {tag}</div>
        <h1>{title}</h1>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-name">CodeGuardian</div>
            <div class="brand-subtitle">AI Code Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="small-label">WORKSPACE</div>',
                unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Accueil",
            "Analyser du code",
            "Historique",
            "À propos",
        ],
        label_visibility="collapsed",
        format_func=lambda item: {
            "Accueil": "⌂  Accueil",
            "Analyser du code": "⌘  Analyse de code",
            "Historique": "◷  Historique",
            "À propos": "ⓘ  À propos",
        }[item],
    )

    st.markdown("---")

    st.markdown("""
    <div class="panel">
        <div class="feature-title">✦ Intelligence artificielle</div>
        <div class="feature-text">
            Analyse intelligente, correction proposée et vérification
            par les tests configurés.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Version 1.0 • Projet d'ingénierie")


# =========================================================
# ACCUEIL
# =========================================================

if page == "Accueil":
    reports = load_reports()
    total = len(reports)
    passed = sum(
        1 for item in reports
        if item.get("tests", {}).get("success") is True
    )
    failed = total - passed

    show_hero(
        "Write code.<br><span class='gradient-text'>Find bugs. Fix smarter.</span>",
        "Un assistant intelligent qui analyse votre code Python, "
        "explique les problèmes détectés et propose des corrections "
        "accompagnées de tests automatisés.",
        "YOUR AI-POWERED DEBUGGING WORKSPACE",
    )

    st.markdown('<div class="section-title">Vue d’ensemble</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-description">'
        'Suivez vos analyses et accédez rapidement aux fonctionnalités.'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Analyses enregistrées", total)

    with c2:
        st.metric("Tests réussis", passed)

    with c3:
        st.metric("Autres résultats", failed)

    st.markdown('<div class="section-title">Tout ce dont vous avez besoin</div>',
                unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔎</div>
            <div class="feature-title">Analyse intelligente</div>
            <div class="feature-text">
                Identifiez les bugs et comprenez leur origine grâce
                à un diagnostic structuré par IA.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Correction proposée</div>
            <div class="feature-text">
                Obtenez une version corrigée de votre code,
                accompagnée d'une explication du problème.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧪</div>
            <div class="feature-title">Tests automatisés</div>
            <div class="feature-text">
                Vérifiez la correction avec les jeux de tests
                disponibles et consultez le résultat.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    left, right = st.columns([2, 1])

    with left:
        st.markdown("""
        <div class="panel">
            <div class="feature-title">Prêt à améliorer votre code ?</div>
            <div class="feature-text">
                Collez votre code Python, lancez l'analyse et consultez
                le diagnostic ainsi que les tests disponibles.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        if st.button("🚀  Commencer l'analyse", type="primary",
                     use_container_width=True):
            st.session_state["page_navigation"] = "Analyser du code"
            st.rerun()

    show_footer()


# =========================================================
# ANALYSE DE CODE
# =========================================================

elif page == "Analyser du code":
    show_hero(
        "Analyse de code",
        "Collez votre code Python pour détecter les problèmes, "
        "obtenir une correction proposée et vérifier les tests disponibles.",
        "INTELLIGENT DEBUGGING",
    )

    default_code = '''def get_user_name(user):
    return user["name"].upper()

print(get_user_name(None))
'''

    if "code_input" not in st.session_state:
        st.session_state["code_input"] = default_code

    st.markdown('<div class="section-title">01 / Votre code source</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-description">'
        'Langage supporté actuellement : Python'
        '</div>',
        unsafe_allow_html=True,
    )

    code = st.text_area(
        "Éditeur Python",
        key="code_input",
        height=310,
        label_visibility="collapsed",
        placeholder="Collez votre code Python ici...",
    )

    col_action, col_hint = st.columns([1, 2])

    with col_action:
        analyze_clicked = st.button(
            "✦  Analyser et corriger",
            type="primary",
            use_container_width=True,
        )

    with col_hint:
        st.caption("L'analyse utilise l'API Gemini et les tests configurés.")

    if analyze_clicked:
        if not code.strip():
            st.warning("Veuillez coller du code Python avant de lancer l'analyse.")
        else:
            with st.spinner("Analyse du code en cours..."):
                try:
                    report = analyze_code(code)

                    st.session_state["latest_report"] = report
                    st.session_state["latest_original_code"] = code

                    with st.spinner("Vérification par les tests disponibles..."):
                        result = run_tests(report["fix_code"], code)

                    st.session_state["latest_test_result"] = result

                    report_path = save_report(
                        code,
                        report,
                        result,
                        attempts=1,
                    )

                    st.session_state["latest_report_path"] = str(report_path)

                except Exception as error:
                    st.error("L'analyse n'a pas pu être terminée.")
                    st.exception(error)

    report = st.session_state.get("latest_report")
    result = st.session_state.get("latest_test_result")
    original_code = st.session_state.get("latest_original_code", "")

    if report and result:
        st.markdown("---")
        st.markdown('<div class="section-title">02 / Diagnostic intelligent</div>',
                    unsafe_allow_html=True)

        found = report.get("bug_found", "Inconnu")
        severity = report.get("severity", "Inconnue")
        bug_type = report.get("bug_type", "Non précisé")

        m1, m2, m3 = st.columns(3)

        with m1:
            st.metric(
                "Bug détecté",
                "Oui" if found is True else (
                    "Non" if found is False else str(found)
                ),
            )

        with m2:
            st.metric("Niveau de gravité", str(severity).upper())

        with m3:
            st.metric(
                "Vérification",
                "Réussie" if result.get("success") else "À vérifier",
            )

        st.markdown(f"""
        <div class="panel">
            <div class="small-label">Type de problème</div>
            <h3>{str(bug_type)}</h3>
            <div class="feature-text">
                {str(report.get("explanation", "Aucune explication fournie.")).replace("<", "&lt;").replace(">", "&gt;")}
            </div>
        </div>
        """, unsafe_allow_html=True)

        uncertainties = report.get("uncertainties", [])
        if uncertainties:
            with st.expander("Points à vérifier et incertitudes"):
                for item in uncertainties:
                    st.write(f"• {item}")

        st.markdown('<div class="section-title">03 / Correction proposée</div>',
                    unsafe_allow_html=True)

        tab_fix, tab_original = st.tabs(
            ["✨ Code corrigé", "Code original"]
        )

        with tab_fix:
            st.code(report.get("fix_code", ""), language="python")
            st.download_button(
                "📥 Télécharger le code corrigé",
                data=report.get("fix_code", ""),
                file_name="corrected_code.py",
                mime="text/x-python",
                use_container_width=True,
            )

        with tab_original:
            st.code(original_code, language="python")

        st.markdown('<div class="section-title">04 / Résultats des tests</div>',
                    unsafe_allow_html=True)

        if result.get("success"):
            st.success("Les tests configurés ont réussi.")
        else:
            st.warning(
                "Les tests ont échoué ou aucun jeu de tests indépendant "
                "n'est disponible pour ce code."
            )

        if result.get("stdout"):
            with st.expander("Afficher la sortie des tests"):
                st.code(result["stdout"])

        if result.get("stderr"):
            with st.expander("Afficher les détails ou erreurs"):
                st.code(result["stderr"])

        export_data = {
            "original_code": original_code,
            "diagnosis": report,
            "tests": result,
            "report_path": st.session_state.get("latest_report_path"),
        }

        st.download_button(
            "📄 Télécharger le rapport complet (JSON)",
            data=json.dumps(export_data, ensure_ascii=False, indent=4),
            file_name="codeguardian_report.json",
            mime="application/json",
        )

        st.info(
            "La réussite des tests configurés ne garantit pas "
            "l'absence de tous les bugs. N'exécutez pas du code non fiable."
        )

    show_footer()


# =========================================================
# HISTORIQUE
# =========================================================

elif page == "Historique":
    show_hero(
        "Historique des analyses",
        "Retrouvez vos diagnostics enregistrés, consultez les corrections "
        "proposées et exportez les rapports précédents.",
        "YOUR ANALYSIS ARCHIVE",
    )

    reports = load_reports()

    if not reports:
        st.info("Aucun rapport disponible. Lancez d'abord une analyse.")
    else:
        total = len(reports)
        passed = sum(
            1 for item in reports
            if item.get("tests", {}).get("success") is True
        )

        a, b = st.columns(2)
        a.metric("Rapports enregistrés", total)
        b.metric("Tests réussis", passed)

        search = st.text_input(
            "🔎 Rechercher dans l'historique",
            placeholder="Nom du rapport ou type de bug...",
        )

        filtered = []

        for item in reports:
            diagnosis = item.get("diagnosis", {})
            filename = item.get("_filename", "")
            bug_type = str(diagnosis.get("bug_type", ""))

            if (
                search.lower() in filename.lower()
                or search.lower() in bug_type.lower()
            ):
                filtered.append(item)

        st.markdown(f"**{len(filtered)} rapport(s) affiché(s)**")

        for item in filtered:
            diagnosis = item.get("diagnosis", {})
            tests = item.get("tests", {})
            filename = item.get("_filename", "Rapport")
            date = item.get("date", "Date inconnue")

            with st.expander(
                f"📄 {filename}  |  {diagnosis.get('bug_type', 'Bug non précisé')}"
            ):
                c1, c2, c3 = st.columns(3)
                c1.metric("Gravité", str(diagnosis.get("severity", "Inconnue")).upper())
                c2.metric(
                    "Bug détecté",
                    str(diagnosis.get("bug_found", "Inconnu")),
                )
                c3.metric(
                    "Tests",
                    "Réussis" if tests.get("success") else "À vérifier",
                )

                st.caption(f"Date : {date}")

                st.markdown("**Explication**")
                st.write(diagnosis.get("explanation", "Non disponible"))

                tab1, tab2 = st.tabs(["Code original", "Correction proposée"])

                with tab1:
                    st.code(item.get("original_code", ""), language="python")

                with tab2:
                    st.code(diagnosis.get("fix_code", ""), language="python")
                    st.download_button(
                        "Télécharger la correction",
                        data=diagnosis.get("fix_code", ""),
                        file_name=f"corrected_{filename.replace('.json', '.py')}",
                        mime="text/x-python",
                        key=f"fix_{filename}",
                    )

                st.download_button(
                    "Télécharger le rapport JSON",
                    data=json.dumps(item, ensure_ascii=False, indent=4),
                    file_name=filename,
                    mime="application/json",
                    key=f"json_{filename}",
                )

    show_footer()


# =========================================================
# À PROPOS
# =========================================================

elif page == "À propos":
    show_hero(
        "À propos de CodeGuardian AI",
        "Un projet d'ingénierie logicielle qui associe intelligence "
        "artificielle générative, analyse de code et tests automatisés.",
        "ABOUT THE PROJECT",
    )

    st.markdown('<div class="section-title">Notre objectif</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        CodeGuardian AI aide les développeurs à comprendre et corriger
        les erreurs de leurs programmes Python. Le système produit un
        diagnostic structuré, propose une correction et lance les jeux
        de tests disponibles pour apporter un premier niveau de vérification.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Technologies utilisées</div>',
                unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)

    with t1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🐍</div>
            <div class="feature-title">Python</div>
            <div class="feature-text">
                Logique métier, orchestration de l'analyse et tests.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✦</div>
            <div class="feature-title">Google Gemini</div>
            <div class="feature-text">
                Analyse du code, diagnostic structuré et correction proposée.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">▣</div>
            <div class="feature-title">Streamlit & JSON</div>
            <div class="feature-text">
                Interface web interactive, historique et export des rapports.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Fonctionnalités</div>',
                unsafe_allow_html=True)

    st.markdown("""
    - Analyse du code Python avec un modèle de langage.
    - Diagnostic structuré en JSON.
    - Proposition de code corrigé.
    - Exécution des tests configurés.
    - Enregistrement des rapports.
    - Consultation de l'historique et export des résultats.
    """)

    st.markdown('<div class="section-title">Limites et sécurité</div>',
                unsafe_allow_html=True)

    st.warning(
        "Les résultats de l'IA peuvent être inexacts. Les tests disponibles "
        "ne couvrent pas nécessairement tous les cas. L'exécution de code "
        "dans un sous-processus avec un délai maximal n'est pas un sandbox "
        "sécurisé : évitez le code non fiable."
    )

    show_footer()
