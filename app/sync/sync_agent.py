"""
Agent 2: Cross-Repository Sync Agent.
Replicates branches and pull request changes from Repo A to Repo B.
"""

import os

try:
    from github import GithubException  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    class GithubException(Exception):
        def __init__(self, status=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.status = status

from app.config import config
from app.github_api.client import get_repo_a, get_repo_b


def ensure_branch_exists(repo_b, branch_name: str, base_branch: str = "main"):
    """
    Checks if a branch exists in Repo B. If not, creates it from the base branch.
    """
    try:
        repo_b.get_branch(branch_name)
        print(f"✅ Branch '{branch_name}' already exists in Repo B.")
    except GithubException as e:
        if e.status == 404:
            print(f"🔹 Branch '{branch_name}' not found in Repo B. Creating branch...")
            base_ref = repo_b.get_git_ref(f"heads/{base_branch}")
            repo_b.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_ref.object.sha)
            print(f"✅ Branch '{branch_name}' created successfully in Repo B.")
        else:
            raise e


def sync_files_between_repos(repo_a, repo_b, branch_name: str, pr_number: int):
    """
    Fetches changed files from PR in Repo A and commits them into the branch on Repo B.
    """
    pr_a = repo_a.get_pull(pr_number)
    changed_files = pr_a.get_files()

    for file in changed_files:
        file_path = file.filename
        status = file.status  # added, modified, removed

        if status == "removed":
            try:
                existing_file = repo_b.get_contents(file_path, ref=branch_name)
                repo_b.delete_file(
                    path=file_path,
                    message=f"sync: delete {file_path} from Repo A PR #{pr_number}",
                    sha=existing_file.sha,
                    branch=branch_name,
                )
                print(f"🗑️ Deleted {file_path} in Repo B.")
            except GithubException:
                print(f"⚠️ File {file_path} not found in Repo B to delete.")
        else:
            # added or modified
            content_a = repo_a.get_contents(file_path, ref=pr_a.head.sha).decoded_content

            try:
                existing_file = repo_b.get_contents(file_path, ref=branch_name)
                repo_b.update_file(
                    path=file_path,
                    message=f"sync: update {file_path} from Repo A PR #{pr_number}",
                    content=content_a,
                    sha=existing_file.sha,
                    branch=branch_name,
                )
                print(f"📝 Updated {file_path} in Repo B.")
            except GithubException:
                repo_b.create_file(
                    path=file_path,
                    message=f"sync: create {file_path} from Repo A PR #{pr_number}",
                    content=content_a,
                    branch=branch_name,
                )
                print(f"✨ Created {file_path} in Repo B.")


def create_or_update_pr_in_repo_b(repo_b, branch_name: str, pr_title: str, pr_body: str, base_branch: str = "main"):
    """
    Creates a Pull Request in Repo B from the synced branch to base branch.
    """
    # Check if PR already exists
    existing_prs = repo_b.get_pulls(state="open", head=f"{repo_b.owner.login}:{branch_name}", base=base_branch)

    if existing_prs.totalCount > 0:
        pr_b = existing_prs[0]
        print(f"ℹ️ Pull Request already exists in Repo B: #{pr_b.number} - {pr_b.html_url}")
        return pr_b

    # Create new PR in Repo B
    new_pr = repo_b.create_pull(
        title=f"[SYNC] {pr_title}",
        body=f"Automated Sync from Repo A.\n\nOriginal Description:\n{pr_body}",
        head=branch_name,
        base=base_branch,
    )
    print(f"🚀 Pull Request created in Repo B: #{new_pr.number} - {new_pr.html_url}")
    return new_pr


def run_sync_agent(pr_number: int, branch_name: str):
    """
    Executes the sync process from Repo A to Repo B.
    """
    print(f"⚡ Running Sync Agent for PR #{pr_number} on branch '{branch_name}'...")

    repo_a = get_repo_a()
    repo_b = get_repo_b()

    pr_a = repo_a.get_pull(pr_number)

    # 1. Ensure target branch exists in Repo B
    ensure_branch_exists(repo_b, branch_name)

    # 2. Sync file changes from PR A to Repo B branch
    sync_files_between_repos(repo_a, repo_b, branch_name, pr_number)

    # 3. Create or update PR in Repo B
    sync_pr = create_or_update_pr_in_repo_b(
        repo_b=repo_b,
        branch_name=branch_name,
        pr_title=pr_a.title,
        pr_body=pr_a.body or "No description provided.",
    )

    print("✅ Sync Agent execution finished successfully!")
    return sync_pr.html_url