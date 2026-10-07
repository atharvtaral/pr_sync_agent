# """
# Streamlit Dashboard for Dual-Agent GitHub Automation System.
# Provides a visual interface to run, test, and monitor Agent 1 (AI Reviewer) and Agent 2 (Sync Agent).
# """

# import os
# import streamlit as st  # pyright: ignore[reportMissingImports]
# from app.config import config
# from app.github_api.client import get_repo_a, get_repo_b
# from app.review.reviewer_agent import run_reviewer_agent, generate_review
# from app.sync.sync_agent import run_sync_agent

# # Page Configuration
# st.set_page_config(
#     page_title="Dual-Agent GitHub Automation Dashboard",
#     page_icon="🤖",
#     layout="wide",
# )

# st.title("🤖 Dual-Agent GitHub Automation Dashboard")
# st.markdown("Manage and test **Agent 1 (AI Code Reviewer)** and **Agent 2 (Cross-Repo Sync Agent)** in real-time.")

# # Sidebar Configuration
# st.sidebar.header("⚙️ Configuration Overview")

# env_status = {
#     "GitHub Token": bool(config.GITHUB_TOKEN),
#     "Repo A": config.REPO_A_NAME or "Not Set",
#     "Repo B": config.REPO_B_NAME or "Not Set",
#     "Gemini API Key": bool(config.GEMINI_API_KEY),
#     "LLM Model": config.LLM_MODEL_NAME,
# }

# for key, val in env_status.items():
#     if isinstance(val, bool):
#         st.sidebar.write(f"**{key}:** {'✅ Set' if val else '❌ Missing'}")
#     else:
#         st.sidebar.write(f"**{key}:** {val}")

# st.sidebar.divider()
# st.sidebar.info("Ensure all required credentials are standard environment variables or set in `.env`.")






"""
Streamlit Dashboard for Dual-Agent GitHub Automation System.
Provides a visual interface to run, test, and monitor Agent 1 (AI Reviewer) and Agent 2 (Sync Agent).
"""

import os
import streamlit as st  # pyright: ignore[reportMissingImports]
from app.config import config
from app.github_api.client import get_repo_a, get_repo_b
from app.review.reviewer_agent import run_reviewer_agent, generate_review
from app.sync.sync_agent import run_sync_agent


# Helper to read from st.secrets or os.getenv dynamically
def fetch_env(key: str, default: str = "") -> str:
    if key in st.secrets:
        return str(st.secrets[key])
    return os.getenv(key, default)

from app.github_api.client import get_repo_a, get_repo_b
from app.review.reviewer_agent import run_reviewer_agent, generate_review
from app.sync.sync_agent import run_sync_agent

# Page Configuration
st.set_page_config(
    page_title="Dual-Agent GitHub Automation Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Dual-Agent GitHub Automation Dashboard")
st.markdown("Manage and test **Agent 1 (AI Code Reviewer)** and **Agent 2 (Cross-Repo Sync Agent)** in real-time.")

# Sidebar Configuration - Fetch values directly at runtime
st.sidebar.header("⚙️ Configuration Overview")

github_token = fetch_env("GITHUB_TOKEN")
repo_a_name = fetch_env("REPO_A_NAME")
repo_b_name = fetch_env("REPO_B_NAME")
gemini_key = fetch_env("GEMINI_API_KEY")
llm_model = fetch_env("LLM_MODEL_NAME", "gemma-4-26b-a4b-it")

env_status = {
    "GitHub Token": bool(github_token),
    "Repo A": repo_a_name or "Not Set",
    "Repo B": repo_b_name or "Not Set",
    "Gemini API Key": bool(gemini_key),
    "LLM Model": llm_model,
}

for key, val in env_status.items():
    if isinstance(val, bool):
        st.sidebar.write(f"**{key}:** {'✅ Set' if val else '❌ Missing'}")
    else:
        st.sidebar.write(f"**{key}:** {val}")

st.sidebar.divider()
st.sidebar.info("Ensure all required credentials are standard environment variables or set in `.env`.")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["🤖 Agent 1: AI Reviewer", "🔄 Agent 2: Cross-Repo Sync", "🧪 LLM Sandbox"])

# -------------------------------------------------------------
# TAB 1: Agent 1 (AI Code Reviewer)
# -------------------------------------------------------------
with tab1:
    st.header("Agent 1: AI Code Reviewer")
    st.caption("Fetch PR diffs from Repo A, generate AI reviews, and optionally post them directly as comments.")

    pr_num_input = st.number_input("Enter PR Number from Repo A:", min_value=1, value=config.PR_NUMBER or 1, step=1)
    
    col1, col2 = st.columns(2)
    with col1:
        btn_preview_review = st.button("🔍 Preview Review (Dry Run)", use_container_width=True)
    with col2:
        btn_post_review = st.button("🚀 Run & Post Review to GitHub", type="primary", use_container_width=True)

    if btn_preview_review or btn_post_review:
        try:
            repo_a = get_repo_a()
            pr = repo_a.get_pull(int(pr_num_input))
            st.subheader(f"📌 PR #{pr.number}: {pr.title}")
            
            # Fetch diff
            files = list(pr.get_files())
            diff_text = "\n".join([f"--- {f.filename}\n+++ {f.filename}\n{f.patch}" for f in files if f.patch])

            if btn_preview_review:
                with st.spinner("Generating AI Review preview..."):
                    review_text = generate_review(diff_text)
                    st.success("Review Generated Successfully!")
                    st.markdown("### AI Review Preview:")
                    st.markdown(review_text)

            if btn_post_review:
                with st.spinner("Running Agent 1 and posting comment to GitHub..."):
                    comment_url = run_reviewer_agent(int(pr_num_input))
                    st.success(f"✅ Review posted successfully!")
                    st.markdown(f"🔗 [View Comment on GitHub]({comment_url})")

        except Exception as e:
            st.error(f"Execution Error: {e}")

# -------------------------------------------------------------
# TAB 2: Agent 2 (Cross-Repo Sync Agent)
# -------------------------------------------------------------
with tab2:
    st.header("Agent 2: Cross-Repository Sync Agent")
    st.caption("Replicate branches and PR code changes from Repo A into Repo B.")

    sync_pr_num = st.number_input("Target PR Number (Repo A):", min_value=1, value=config.PR_NUMBER or 1, step=1, key="sync_pr")
    sync_branch_name = st.text_input("Branch Name to Sync:", value=config.BRANCH_NAME or "feature/sync-test")

    if st.button("🔄 Execute Cross-Repo Sync", type="primary", use_container_width=True):
        if not sync_branch_name:
            st.warning("Please specify a valid branch name.")
        else:
            try:
                with st.spinner(f"Syncing PR #{sync_pr_num} ('{sync_branch_name}') from Repo A to Repo B..."):
                    synced_pr_url = run_sync_agent(pr_number=int(sync_pr_num), branch_name=sync_branch_name)
                    st.success("✅ Sync completed successfully!")
                    st.markdown(f"🔗 [View Synced PR in Repo B]({synced_pr_url})")
            except Exception as e:
                st.error(f"Sync Execution Error: {e}")

# -------------------------------------------------------------
# TAB 3: LLM Sandbox
# -------------------------------------------------------------
with tab3:
    st.header("🧪 Custom Code Review Sandbox")
    st.caption("Test the Gemini LLM with custom raw diff snippets without connecting to GitHub.")

    sample_diff = st.text_area(
        "Paste Git Diff Here:",
        height=250,
        value="""diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,3 +1,5 @@
 def process_data(data):
-    return data
+    # Secret key exposed
+    API_KEY = "12345-abcdef"
+    return eval(data)
"""
    )

    if st.button("⚡ Run Custom Review", use_container_width=True):
        if sample_diff.strip():
            with st.spinner("Analyzing custom diff..."):
                try:
                    custom_review = generate_review(sample_diff)
                    st.markdown("### AI Feedback:")
                    st.markdown(custom_review)
                except Exception as e:
                    st.error(f"LLM Error: {e}")
        else:
            st.warning("Please paste a diff to review.")