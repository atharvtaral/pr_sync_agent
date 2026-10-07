# import os
# from importlib import import_module

# try:
#     ChatOpenAI = import_module("langchain_openai").ChatOpenAI
# except ModuleNotFoundError:
#     ChatOpenAI = import_module("langchain_community.chat_models").ChatOpenAI

# def get_llm():
#     model_name = os.getenv("LLM_MODEL_NAME", "gemma-4-26b-a4b-it")
#     base_url = os.getenv("GEMINI_API_KEY", None)
    
#     return ChatOpenAI(
#         model=model_name,
#         base_url=base_url, 
#         temperature=0.2
#     )






"""
Agent 1: AI Code Reviewer Agent.
Fetches PR diffs, sends them to Gemini LLM for analysis, and posts review comments.
"""

from importlib import import_module

try:
    ChatOpenAI = import_module("langchain_openai").ChatOpenAI
except ModuleNotFoundError:
    ChatOpenAI = import_module("langchain_community.chat_models").ChatOpenAI
from app.config import config
from app.github_api.client import get_repo_a
from app.review.prompts import CODE_REVIEW_SYSTEM_PROMPT, get_review_prompt


def get_llm():
    """Initializes and returns the ChatOpenAI client configured for Gemini API."""
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in environment variables or configuration.")

    return ChatOpenAI(
        model=config.LLM_MODEL_NAME,
        openai_api_key=config.GEMINI_API_KEY,
        openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
        temperature=0.2,
    )


def generate_review(pr_diff: str, pr_title: str = "Automated PR Review") -> str:
    """Sends the code diff to Gemini LLM and receives structured review feedback."""
    if not pr_diff.strip():
        return "⚠️ No code diff provided or empty diff."

    llm = get_llm()
    prompt = get_review_prompt(pr_title, pr_diff)

    messages = [
        ("system", CODE_REVIEW_SYSTEM_PROMPT),
        ("human", prompt),
    ]

    response = llm.invoke(messages)
    return response.content


def run_reviewer_agent(pr_number: int) -> str:
    """Fetches PR diff from Repo A, generates AI code review, and posts it as a PR comment."""
    print(f"🔍 Fetching PR #{pr_number} from Repo A...")
    repo_a = get_repo_a()
    pr = repo_a.get_pull(pr_number)

    # Fetch all changed files diff
    files = list(pr.get_files())
    diff_text = "\n".join([f"--- {f.filename}\n+++ {f.filename}\n{f.patch}" for f in files if f.patch])

    if not diff_text.strip():
        print("⚠️ No code changes found in this PR.")
        return "No code changes found in PR."

    print("🤖 Generating AI Review via Gemini LLM...")
    review_markdown = generate_review(pr_diff=diff_text, pr_title=pr.title)

    print("💬 Posting review comment on GitHub PR...")
    comment = pr.create_issue_comment(review_markdown)

    print(f"✅ AI Review posted successfully: {comment.html_url}")
    return comment.html_url