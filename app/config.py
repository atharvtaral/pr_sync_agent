# import os

# try:
#     from dotenv import load_dotenv  # type: ignore[reportMissingImports]
# except ImportError:  # pragma: no cover
#     def load_dotenv(*args, **kwargs):
#         return False

# # Load environment variables from .env file
# load_dotenv()


# class Config:
#     """Central configuration management for the PR Sync & AI Review Agent."""

#     # GitHub Credentials & Repositories
#     GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
#     REPO_A_NAME: str = os.getenv("REPO_A_NAME", "")
#     REPO_B_NAME: str = os.getenv("REPO_B_NAME", "")

#     # LLM / Gemini Credentials
#     GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
#     OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
#     LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gemma-4-26b-a4b-it")

#     # PR Metadata (passed during workflow or execution)
#     PR_NUMBER: int = int(os.getenv("PR_NUMBER", 0))
#     BRANCH_NAME: str = os.getenv("BRANCH_NAME", "")

#     @classmethod
#     def validate(cls) -> None:
#         """Validates that essential environment variables are set."""
#         missing = []
#         if not cls.GITHUB_TOKEN:
#             missing.append("GITHUB_TOKEN")
#         if not cls.REPO_A_NAME:
#             missing.append("REPO_A_NAME")

#         if missing:
#             raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


# # Instantiated config object for easy import
# config = Config()








import os
import streamlit as st

def get_secret(key: str, default: str = "") -> str:
    # 1. First check standard Environment Variables (.env)
    val = os.getenv(key)
    if val:
        return val
    # 2. Check Streamlit Cloud Secrets (st.secrets)
    try:
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default

class Config:
    GITHUB_TOKEN: str = get_secret("GITHUB_TOKEN")
    REPO_A_NAME: str = get_secret("REPO_A_NAME")
    REPO_B_NAME: str = get_secret("REPO_B_NAME")
    GEMINI_API_KEY: str = get_secret("GEMINI_API_KEY")
    LLM_MODEL_NAME: str = get_secret("LLM_MODEL_NAME", "gemma-4-26b-a4b-it")

    @property
    def PR_NUMBER(self) -> int:
        val = get_secret("TEST_PR_NUMBER", "1")
        return int(val) if val.isdigit() else 1

    @property
    def BRANCH_NAME(self) -> str:
        return get_secret("TEST_BRANCH_NAME", "feature/test-sync")

    def validate(self):
        missing = []
        if not self.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not self.REPO_A_NAME:
            missing.append("REPO_A_NAME")
        if not self.REPO_B_NAME:
            missing.append("REPO_B_NAME")
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

config = Config()