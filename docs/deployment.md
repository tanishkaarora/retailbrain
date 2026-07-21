# Production Deployment Guide: AI Business Decision Copilot

This guide outlines instructions for deploying and maintaining the AI Business Decision Copilot on Streamlit Community Cloud.

## Deployment Steps

To deploy this application to Streamlit Community Cloud, follow these steps:

### 1. Repository Preparation
Ensure your local changes are committed and pushed to your GitHub repository:
```bash
git add .
git commit -m "Configure project for Streamlit Cloud deployment"
git push origin main
```

### 2. Connect to Streamlit Community Cloud
1. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and log in using your GitHub account.
2. Click the **Deploy** button (or **New app**).
3. Select your repository, the active branch (e.g., `main`), and specify the main entrypoint file path as:
   `streamlit_app.py`
4. Click the **Deploy!** button.

### 3. Secrets Configuration
Streamlit Community Cloud requires environment secrets to connect to LLMs.
1. In the Streamlit Cloud dashboard, locate your running app.
2. Click the **Settings** gear icon (or triple dots -> Settings) in the lower right or from your dashboard.
3. Select **Secrets** from the sidebar.
4. Paste the API key settings in TOML format:

```toml
# Streamlit Cloud Secrets (TOML format)
GEMINI_API_KEY = "your_gemini_api_key_here"
GROQ_API_KEY = "your_groq_api_key_here"

# (Optional) Choose the default active provider
USE_GEMINI = "true"
USE_GROQ = "false"
```
5. Click **Save**. Streamlit will automatically restart the app with the new credentials active.

---

## Troubleshooting Common Errors

### 1. Missing Dependencies
* **Error**: `ModuleNotFoundError: No module named 'langchain_groq'`
* **Resolution**: Verify that the package exists in `requirements.txt` and is spelled correctly. Streamlit Cloud automatically reads `requirements.txt` on startup. If you recently added a library, verify it was pushed to GitHub.

### 2. Memory Limits / Container Crashes
* **Error**: App becomes unresponsive or goes into a "Crashed" state when loading datasets or files.
* **Resolution**: Streamlit Community Cloud limits containers to ~1GB of RAM. The embedding model `BAAI/bge-small-en-v1.5` is lightweight (~120MB) and cached in resource memory. If you process very large PDFs (>100 pages) or large CSV files (>100k rows), it might exhaust RAM. Consider using API-based embeddings (OpenAI/Google) by removing sentence-transformers to free up RAM.

### 3. API Key Missing / Unauthorized
* **Error**: `ValueError: GEMINI_API_KEY not found.`
* **Resolution**: Ensure secrets are configured in the Streamlit Cloud Settings panel exactly as shown above. Check for typos or trailing spaces in the TOML string.

---

## Rollback Steps

If a deployment fails or introduces regressions:
1. Identify the last known stable commit hash using git:
   ```bash
   git log --oneline
   ```
2. Revert or reset the repository to that commit:
   ```bash
   git reset --hard <stable_commit_hash>
   ```
3. Force push the stable state back to GitHub:
   ```bash
   git push origin main --force
   ```
4. Streamlit Community Cloud will detect the push and automatically rebuild/rollback to the stable code.

---

## Updating the Deployment

To push new features or updates:
1. Make and test changes locally.
2. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin main
   ```
3. The cloud container will automatically detect the new commits and rebuild the app in place.
