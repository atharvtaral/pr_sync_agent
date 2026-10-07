"""
Tests for Agent 1 (AI Code Reviewer).
Includes offline mock tests and optional live GitHub PR tests.
"""

import os
from importlib import import_module

try:
    load_dotenv = import_module("dotenv").load_dotenv
except ImportError:  # pragma: no cover - optional dependency for local env loading
    def load_dotenv(*args, **kwargs):
        return False

from app.review.prompts import get_review_prompt, CODE_REVIEW_SYSTEM_PROMPT
from app.review.reviewer_agent import generate_review, run_reviewer_agent

load_dotenv()

MOCK_DIFF = """
diff --git a/app/database.py b/app/database.py
index e69de29..4b825dc 100644
--- a/app/database.py
+++ b/app/database.py
@@ -0,0 +1,8 @@
+import os
+import sqlite3
+
+def connect_db():
+    # HARDCODED SECRET WARNING
+    db_password = "super_secret_password_123"
+    connection = sqlite3.connect("database.db")
+    return connection
"""


def test_offline_llm_review():
    """Tests LLM code review generation using a mock diff (No GitHub connection needed)."""
    print("🚀 [Test 1] Testing LLM Reviewer with Mock Diff...\n")
    try:
        review_output = generate_review(MOCK_DIFF)
        print("✅ LLM Review Generated Successfully:")
        print("=" * 60)
        print(review_output)
        print("=" * 60)
    except Exception as e:
        print(f"❌ LLM Review Test Failed: {e}")


def test_live_pr_review(pr_number: int):
    """Tests fetching a live PR diff from Repo A and posting an AI review comment."""
    print(f"\n🔍 [Test 2] Testing Live PR Review on Repo A (PR #{pr_number})...")
    try:
        result = run_reviewer_agent(pr_number)
        print("✅ Live PR Review Posted Successfully!")
        print("=" * 60)
        print(result)
        print("=" * 60)
    except Exception as e:
        print(f"❌ Live PR Review Test Failed: {e}")


if __name__ == "__main__":
    # 1. Run local offline test
    test_offline_llm_review()

    # 2. Run live PR test if TEST_PR_NUMBER is defined in .env
    test_pr_num = os.getenv("TEST_PR_NUMBER")
    if test_pr_num:
        test_live_pr_review(int(test_pr_num))
    else:
        print("\n💡 Tip: Add `TEST_PR_NUMBER=1` to your .env file to test live GitHub PR posting.")