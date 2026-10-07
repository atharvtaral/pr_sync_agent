import os

try:
    from dotenv import load_dotenv  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    def load_dotenv(*args, **kwargs):
        return False

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration management for the PR Sync & AI Review Agent."""

    # GitHub Credentials & Repositories
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    REPO_A_NAME: str = os.getenv("REPO_A_NAME", "")
    REPO_B_NAME: str = os.getenv("REPO_B_NAME", "")

    # LLM / Gemini Credentials
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gemma-4-26b-a4b-it")

    # PR Metadata (passed during workflow or execution)
    PR_NUMBER: int = int(os.getenv("PR_NUMBER", 0))
    BRANCH_NAME: str = os.getenv("BRANCH_NAME", "")

    @classmethod
    def validate(cls) -> None:
        """Validates that essential environment variables are set."""
        missing = []
        if not cls.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not cls.REPO_A_NAME:
            missing.append("REPO_A_NAME")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


# Instantiated config object for easy import
config = Config()