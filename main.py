"""
Main Entry Point / Orchestrator for Dual-Agent GitHub Automation System.
Triggers Agent 1 (AI Code Reviewer) and Agent 2 (Cross-Repo Sync Agent).
"""

import sys
from app.config import config
from app.review.reviewer_agent import run_reviewer_agent
from app.sync.sync_agent import run_sync_agent


def main():
    print("=" * 60)
    print("🚀 Starting Dual-Agent GitHub Orchestrator")
    print("=" * 60)

    try:
        # Validate configuration & required environment variables
        config.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)

    pr_number = config.PR_NUMBER
    branch_name = config.BRANCH_NAME

    if not pr_number:
        print("❌ Error: PR_NUMBER environment variable is missing or invalid.")
        sys.exit(1)

    print(f"📌 Target PR: #{pr_number}")
    print(f"📌 Target Branch: {branch_name or 'N/A'}")
    print("-" * 60)

    # -------------------------------------------------------------
    # 1. Execute Agent 1: AI Code Reviewer
    # -------------------------------------------------------------
    print("\n🤖 [Step 1/2] Executing Agent 1 (AI Code Reviewer)...")
    try:
        review_result = run_reviewer_agent(pr_number)
        print("✅ Agent 1 Completed: AI Review comment posted on Repo A PR.")
    except Exception as e:
        print(f"⚠️ Agent 1 Error: {e}")

    # -------------------------------------------------------------
    # 2. Execute Agent 2: Cross-Repo Sync Agent
    # -------------------------------------------------------------
    print("\n🔄 [Step 2/2] Executing Agent 2 (Cross-Repo Sync Agent)...")
    if not branch_name:
        print("⚠️ Skipping Agent 2: BRANCH_NAME is not specified.")
    else:
        try:
            synced_pr_url = run_sync_agent(pr_number=pr_number, branch_name=branch_name)
            print(f"✅ Agent 2 Completed: Branch & PR synced to Repo B.")
            print(f"🔗 Synced PR URL: {synced_pr_url}")
        except Exception as e:
            print(f"⚠️ Agent 2 Error: {e}")

    print("\n" + "=" * 60)
    print("🎉 All Orchestration Tasks Finished Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()