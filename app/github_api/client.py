from importlib import import_module
from typing import Any

from app.config import config


def get_github_client() -> Any:
    """Initializes and returns the PyGithub client authenticated with GITHUB_TOKEN."""
    if not config.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN is missing in environment variables or app configuration.")
    github = import_module("github")
    return github.Github(config.GITHUB_TOKEN)


def get_repo_a() -> Any:
    """Fetches and returns the PyGithub Repository object for Repo A."""
    if not config.REPO_A_NAME:
        raise ValueError("REPO_A_NAME is missing in environment variables or app configuration.")
    gh = get_github_client()
    return gh.get_repo(config.REPO_A_NAME)


def get_repo_b() -> Any:
    """Fetches and returns the PyGithub Repository object for Repo B."""
    if not config.REPO_B_NAME:
        raise ValueError("REPO_B_NAME is missing in environment variables or app configuration.")
    gh = get_github_client()
    return gh.get_repo(config.REPO_B_NAME)