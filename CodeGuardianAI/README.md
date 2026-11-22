# 🛡️ CodeGuardian AI

### AI-Powered Python Code Analysis & Debugging Assistant

**Detect potential bugs. Understand the problem. Review a proposed fix. Validate it with available tests.**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-8E75B2)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![JSON](https://img.shields.io/badge/Output-Structured%20JSON-0B7285)

## ✨ Overview

**CodeGuardian AI** is an AI-powered Python debugging assistant that combines a large language model (LLM), automated checks, and an interactive web dashboard.

Developers can submit Python code to receive a structured diagnosis, an explanation of potential issues, and a proposed corrected version. The application then runs the test cases configured in the project and saves analysis reports for later review.

## 🚀 Features

- 🧠 **AI-assisted analysis:** Analyze Python code using Google Gemini.
- 🧾 **Structured diagnosis:** Receive JSON results describing potential bugs, severity, explanations, and uncertainties.
- 🛠️ **Code correction:** Review and download a proposed corrected version.
- 🧪 **Automated checks:** Execute the test cases currently supported by the project.
- 🗂️ **Report history:** Save and inspect analysis reports.
- 📥 **Export:** Download corrected Python code and JSON reports.
- 🖥️ **Interactive dashboard:** Navigate between analysis, history, and project information.

## 🏗️ How It Works

1. Submit Python code through the Streamlit interface.
2. Send the code to Google Gemini for analysis.
3. Receive a structured JSON diagnosis.
4. Display the proposed correction.
5. Run the configured automated tests.
6. Present the results and save a JSON report.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Google Gemini API | LLM-based code analysis |
| Streamlit | Interactive web interface |
| JSON | Structured results and report storage |
| python-dotenv | Environment-based API configuration |
| Subprocess | Execution of configured checks |

## 📁 Project Structure

```text
CodeGuardianAI/
├── app.py
├── main.py
├── test_runner.py
├── report_manager.py
├── requirements.txt
├── .gitignore
├── .env
├── reports/
└── README.md
```

- `app.py` — Streamlit dashboard.
- `main.py` — Gemini integration and code analysis.
- `test_runner.py` — Configured automated tests.
- `report_manager.py` — Report persistence and history.
- `requirements.txt` — Python dependencies.
- `.env` — Local API credentials; never commit this file.
- `reports/` — Locally generated analysis reports.

## ⚙️ Getting Started

### Prerequisites

- Python 3.10 or newer recommended.
- A Google Gemini API key.
- Git, if cloning the repository.

### 1. Clone the repository

Replace the placeholders with your actual GitHub username and repository name.

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

### 2. Create a virtual environment

**Windows — Git Bash**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` has not yet been created, install the project's direct dependencies:

```bash
pip install streamlit google-genai python-dotenv
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own key. Never publish the actual API key.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## 🔐 Security

- Never commit `.env` or expose API credentials.
- Exclude `.venv/`, `__pycache__/`, and generated reports from version control.
- Review AI-generated corrections before using them.
- A subprocess timeout is not a secure sandbox. Do not run untrusted code on your main computer.
- Avoid publishing reports that contain confidential source code or sensitive data.

Suggested `.gitignore`:

```gitignore
.env
.env.*
.venv/
venv/
__pycache__/
*.py[cod]
reports/
*.log
.vscode/
.idea/
.DS_Store
Thumbs.db
```

## 🧪 Current Limitations

The test runner currently supports predefined test scenarios. It is not yet a general-purpose testing platform.

- Test coverage depends on the scenarios configured in the project.
- Passing available tests does not guarantee that a correction is completely correct.
- LLM-generated explanations and fixes may be inaccurate.
- Secure execution of arbitrary code requires additional isolation.

## 🗺️ Roadmap

- [ ] Expand test coverage and edge-case handling.
- [ ] Add generic test generation with developer review.
- [ ] Add static analysis and syntax validation.
- [ ] Introduce secure isolation for code execution.
- [ ] Improve report filtering and comparison.
- [ ] Add unit and integration tests.
- [ ] Add application screenshots and a demo GIF.
- [ ] Explore secure deployment options.

## 🎯 Skills Demonstrated

This project demonstrates practical work with:

- LLM API integration.
- Prompt engineering and structured JSON responses.
- Python application architecture and error handling.
- Automated testing workflows.
- Streamlit UI development.
- JSON persistence and report export.
- Environment-variable configuration.
- Technical documentation and security awareness.

## 🤝 Contributing

Suggestions and improvements are welcome. Please open an issue before proposing major changes, and never include API keys or sensitive source code in public issues.

## 📄 License

No license has been added yet. If you intend to permit reuse, select an appropriate open-source license and add a `LICENSE` file before claiming that the project is licensed.

---

**CodeGuardian AI** · AI-assisted debugging for Python

*Built as a software engineering portfolio project.*
