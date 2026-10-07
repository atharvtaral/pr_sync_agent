# 🤖 Dual-Agent GitHub Automation Pipeline

An automated Python-based GitHub workflow system that uses **Gemini LLMs, Streamlit, and PyGithub** to automate code reviews and cross-repository code synchronization.

## 🌟 Overview

This project contains two independent automation agents managed through a central pipeline and an interactive Streamlit dashboard.

```text
                  ┌────────────────────────┐
                  │   GitHub Pull Request  │
                  └───────────┬────────────┘
                              │
                    Trigger Pipeline
                              │
                     ┌────────┴────────┐
                     │                 │
                     ▼                 ▼
          ┌───────────────────┐  ┌───────────────────┐
          │     Agent 1       │  │     Agent 2       │
          │   AI Reviewer     │  │ Cross-Repo Sync   │
          └─────────┬─────────┘  └─────────┬─────────┘
                    │                      │
             Analyze Git Diff       Sync Branch & Files
                    │                      │
                    ▼                      ▼
             GitHub PR Review       Repository B / PR
```

### Agent 1 — AI Code Reviewer

The AI Code Reviewer:

1. Fetches Pull Request changes from **Repo A**.
2. Sends the relevant code diff to the Gemini LLM.
3. Analyzes the code changes.
4. Generates a structured Markdown review.
5. Posts the review directly to the GitHub Pull Request.

### Agent 2 — Cross-Repository Sync Agent

The Cross-Repository Sync Agent:

1. Detects changes in **Repo A**.
2. Synchronizes branches and changed files.
3. Applies the changes to **Repo B**.
4. Creates or updates a Pull Request in the target repository.

---

## ✨ Features

- 🤖 AI-powered Pull Request code reviews
- 🧠 Gemini LLM integration
- 🐙 GitHub API integration using PyGithub
- 🔄 Cross-repository branch and file synchronization
- 🖥️ Interactive Streamlit dashboard
- ⚙️ CLI-based pipeline execution
- 🚀 GitHub Actions automation
- 🧪 Tests for both automation agents
- 🔐 Environment-based configuration

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core application |
| Gemini LLM | AI-powered code review |
| Streamlit | Interactive web dashboard |
| PyGithub | GitHub API integration |
| GitHub Actions | CI/CD automation |
| python-dotenv | Environment configuration |

---

## 📁 Project Structure

```text
pr-sync-agent/
│
├── .github/
│   └── workflows/
│       └── agent_pipeline.yml       # GitHub Actions workflow
│
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
│
├── app/
│   ├── __init__.py
│   ├── config.py                    # Environment configuration
│   │
│   ├── github_api/
│   │   ├── __init__.py
│   │   └── client.py                # GitHub API client
│   │
│   ├── review/
│   │   ├── __init__.py
│   │   ├── prompts.py               # Gemini prompt templates
│   │   └── reviewer_agent.py        # AI reviewer agent
│   │
│   └── sync/
│       ├── __init__.py
│       └── sync_agent.py            # Cross-repository sync agent
│
├── tests/
│   ├── __init__.py
│   ├── test_reviewer.py             # Reviewer tests
│   └── test_sync.py                 # Sync tests
│
├── .env                             # Local credentials (do not commit)
├── .gitignore
├── main.py                          # Pipeline entry point
├── README.md
├── requirements.txt
└── streamlit_app.py                 # Streamlit dashboard
```

---

# 🚀 Setup & Installation

## Prerequisites

Make sure the following are installed:

- Python 3.10 or higher
- Git
- GitHub Personal Access Token (PAT)
- Gemini API Key

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/pr-sync-agent.git
cd pr-sync-agent
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the root directory:

```ini
# GitHub Credentials
GITHUB_TOKEN=your_github_personal_access_token

# Source Repository
REPO_A_NAME=username/repo-a

# Target Repository
REPO_B_NAME=username/repo-b

# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# LLM Model
LLM_MODEL_NAME=gemma-4-26b-a4b-it

# Testing Configuration
TEST_PR_NUMBER=1
TEST_BRANCH_NAME=feature/sync-test
```

## Environment Variables

| Variable | Description |
|---|---|
| `GITHUB_TOKEN` | GitHub Personal Access Token |
| `REPO_A_NAME` | Source repository in `owner/repository` format |
| `REPO_B_NAME` | Target repository in `owner/repository` format |
| `GEMINI_API_KEY` | Gemini API key |
| `LLM_MODEL_NAME` | LLM model used for code review |
| `TEST_PR_NUMBER` | Pull Request number used for testing |
| `TEST_BRANCH_NAME` | Branch used for synchronization tests |

> ⚠️ **Security:** Never commit `.env`, GitHub tokens, or Gemini API keys to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# 🖥️ Running the Application

## Streamlit Dashboard

Start the interactive dashboard:

```bash
streamlit run streamlit_app.py
```

Streamlit will provide a local URL where the dashboard can be accessed.

## CLI Pipeline

Run the complete automation pipeline:

```bash
python main.py
```

---

# 🧪 Testing

## Agent 1 — AI Code Reviewer

Run the reviewer tests:

```bash
python -m tests.test_reviewer
```

## Agent 2 — Cross-Repository Sync

Run the synchronization tests:

```bash
python -m tests.test_sync
```

> **Note:** Integration tests may require valid GitHub credentials and access to the configured repositories.

---

# ⚙️ GitHub Actions CI/CD

The project supports automatic execution through GitHub Actions.

The workflow file is:

```text
.github/workflows/agent_pipeline.yml
```

## Configure GitHub Secrets

In **Repo A**, open:

```text
Settings → Secrets and variables → Actions
```

Add the following secrets:

| Secret | Description |
|---|---|
| `BOT_GITHUB_TOKEN` | GitHub PAT with access to Repo A and Repo B |
| `GEMINI_API_KEY` | Gemini API key |
| `TARGET_REPO_B_NAME` | Target repository in `owner/repository` format |

Example:

```text
TARGET_REPO_B_NAME=username/repo-b
```

Once configured, the workflow can automatically run when a Pull Request is created or updated in Repo A.

---

# 🔄 Automation Workflow

```text
Developer creates / updates Pull Request
                    │
                    ▼
             GitHub Actions
                    │
                    ▼
          Pipeline Orchestrator
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
     ┌──────────┐        ┌──────────┐
     │  Agent 1 │        │  Agent 2 │
     │AI Review │        │ Repo Sync│
     └────┬─────┘        └────┬─────┘
          │                   │
          ▼                   ▼
      Gemini LLM          Repository B
          │                   │
          ▼                   ▼
    GitHub PR Review      Mirror PR
```

---

# 🧠 Agent 1 — AI Review Flow

```text
GitHub Pull Request
        │
        ▼
Fetch PR Diff
        │
        ▼
Build Structured Prompt
        │
        ▼
Gemini LLM
        │
        ▼
Generate Code Review
        │
        ▼
Post Review to GitHub
```

---

# 🔄 Agent 2 — Sync Flow

```text
Repository A
      │
      ▼
Detect Changed Files
      │
      ▼
Create / Update Branch
      │
      ▼
Apply Changes
      │
      ▼
Repository B
      │
      ▼
Create / Update Pull Request
```

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │     GitHub PR       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Pipeline Orchestrator│
                         │       main.py       │
                         └──────────┬──────────┘
                                    │
                   ┌────────────────┴────────────────┐
                   │                                 │
                   ▼                                 ▼
          ┌──────────────────┐              ┌──────────────────┐
          │     Agent 1      │              │     Agent 2      │
          │   AI Reviewer    │              │ Cross-Repo Sync  │
          └────────┬─────────┘              └────────┬─────────┘
                   │                                 │
                   ▼                                 ▼
              Gemini LLM                       Repository B
                   │                                 │
                   ▼                                 ▼
             GitHub Review                    Mirror Pull Request
```

---

# 📌 Important Files

| File | Description |
|---|---|
| `main.py` | Main CLI entry point and pipeline orchestrator |
| `streamlit_app.py` | Interactive Streamlit dashboard |
| `app/config.py` | Application configuration |
| `app/github_api/client.py` | GitHub authentication and API operations |
| `app/review/prompts.py` | Gemini prompt templates |
| `app/review/reviewer_agent.py` | AI code reviewer implementation |
| `app/sync/sync_agent.py` | Cross-repository synchronization implementation |
| `.github/workflows/agent_pipeline.yml` | GitHub Actions automation |

---

# 🔒 Security

This application works with GitHub repositories and external AI APIs.

Never commit sensitive credentials such as:

```text
.env
GitHub Personal Access Tokens
Gemini API Keys
```

For GitHub Actions, always store credentials using **GitHub Secrets**.

Use the minimum permissions required by the automation.

---

# 🧪 Development Commands

Run the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

Run the CLI pipeline:

```bash
python main.py
```

Run Agent 1 tests:

```bash
python -m tests.test_reviewer
```

Run Agent 2 tests:

```bash
python -m tests.test_sync
```

---

# 🚀 Future Improvements

- [ ] Support multiple target repositories
- [ ] Inline GitHub review comments
- [ ] AI review severity classification
- [ ] Automatic review summaries
- [ ] Configurable synchronization rules
- [ ] Support additional LLM providers
- [ ] Improved retry and error handling
- [ ] Webhook-based triggering
- [ ] Detailed execution logs
- [ ] GitHub App authentication
- [ ] Docker deployment
- [ ] Production monitoring and alerting

---

# 📄 License

Add your preferred license here.

Example:

```text
MIT License
```

---

# 👨‍💻 Author

**Atharv Taral**

GitHub: https://github.com/atharvtaral

---

⭐ If you find this project useful, please consider giving the repository a star!
