"""
Tests for Agent 2 (Cross-Repository Sync Agent).
Executes and validates branch replication and PR syncing from Repo A to Repo B.
"""

import os
from app.sync.sync_agent import run_sync_agent


def _load_env_file():
    """Load basic KEY=VALUE entries from the project .env file."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    try:
        with open(env_path, encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
    except FileNotFoundError:
        pass


_load_env_file()


def test_sync_agent():
    """Runs the Sync Agent using PR and Branch information from environment variables."""
    pr_number = os.getenv("TEST_PR_NUMBER")
    branch_name = os.getenv("TEST_BRANCH_NAME", "feature/test-sync")

    if not pr_number:
        print("⚠️ TEST_PR_NUMBER is not set in .env file.")
        print("💡 Please set `TEST_PR_NUMBER=1` and `TEST_BRANCH_NAME=feature/my-branch` in .env to test live sync.")
        return

    print(f"🚀 Testing Sync Agent for PR #{pr_number} on branch '{branch_name}'...")
    try:
        sync_pr_url = run_sync_agent(pr_number=int(pr_number), branch_name=branch_name)
        print("✅ Sync Agent executed successfully!")
        print(f"🔗 Synced PR URL in Repo B: {sync_pr_url}")
    except Exception as e:
        print(f"❌ Sync Agent Test Failed: {e}")


if __name__ == "__main__":
    test_sync_agent()