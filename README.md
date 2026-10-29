# SupportIQ — Context-Aware Customer Support Agent

A full-stack GenAI support workspace: **React + Vite, FastAPI, SQLAlchemy, ChromaDB, Sentence Transformers, and an OpenAI-compatible LLM**.

## Features
- Signup/login with bcrypt password hashing and JWT.
- Per-account ticket and knowledge-document ownership.
- Upload `.pdf`, `.txt`, and `.md` knowledge files; text is chunked and indexed in persistent ChromaDB with local embeddings.
- RAG-based reply drafts grounded in retrieved document passages; source filenames appear with drafts.
- LLM-assisted category and priority suggestions.
- CSV ticket import, ticket creation/editing, and analytics for status, category, priority, and average resolution time.
- Human approval workflow. **Approval marks a draft approved; it does not send an email.**
- Animated, responsive UI with login/signup, overview, tickets, ticket details, and knowledge base.
- SQLite works locally; PostgreSQL can be configured using `DATABASE_URL`.

## Real data
The app works on documents and ticket exports that you upload. `data/sample_tickets.csv` is **synthetic test data**, not real customer data. To use real data, import an authorized export from your support platform and upload company-approved policies, product guides, FAQs, and troubleshooting documents. Only upload data you are permitted to process.

## Requirements
Python 3.11+, Node.js 20+, an LLM API key for generation/classification, and internet on first run to download the embedding model.

## Run on Windows PowerShell

### 1. Backend
```powershell
cd SupportIQ\backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `backend/.env` and set `OPENAI_API_KEY`. Keep `.env` private.

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
API health: http://127.0.0.1:8000/health  
API docs: http://127.0.0.1:8000/docs

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

### 2. Frontend (second terminal)
From the project root:
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```
Open the URL Vite prints (usually http://localhost:5173).

### 3. Add your data
1. Create an account.
2. Open **Knowledge Base** and upload `.pdf`, `.txt`, or `.md` company documents.
3. Open **Tickets**, create a ticket or import an authorized CSV.
4. CSV headers: `subject,description,customer_email,category,priority,status,created_at,resolved_at`.
5. Open a ticket and choose **Generate AI draft**. Review source filenames, edit the draft, and approve it.
6. Approval is not sending. Copy the approved draft to your actual support system after your normal checks.

## PostgreSQL (optional)
Create a PostgreSQL database, then set this in `backend/.env`:
```env
DATABASE_URL=postgresql+psycopg://supportiq_user:your_password@localhost:5432/supportiq
```
Use URL-encoded special characters in passwords. Tables are created at startup; add Alembic migrations before production use.

## LLM configuration
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=
```
For an OpenAI-compatible provider, use its documented base URL and model. If no API key is configured, the app returns a clear configuration error rather than fabricating a response. Knowledge indexing/retrieval is local.

## Publish to GitHub
1. Create an empty repository on GitHub, e.g. `supportiq-genai-customer-support-agent`.
2. Ensure `.env` is not staged (the `.gitignore` excludes it).
3. From the project root:
```powershell
git init
git add .
git status
git commit -m "Build SupportIQ GenAI customer support agent"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/supportiq-genai-customer-support-agent.git
git push -u origin main
```
Replace `YOUR-USERNAME`. Authenticate through GitHub's supported sign-in flow. Never put a token in source code or the remote URL.

## UI screenshots
`docs/architecture.svg` is a project architecture illustration, not a screenshot. After running the app, capture genuine screenshots of login, dashboard, ticket review, and knowledge base. Put them in `docs/screenshots/` and embed them in this README using Markdown image links. Do not label mockups as screenshots of a running application.

## Production checklist
This is an internship MVP, not a production-certified support platform. Before deployment, add HTTPS, a strong JWT secret, rate limiting, account recovery, audit logging, malware/content scanning, database migrations, backups/retention policies, monitoring, and review of your LLM provider's data-handling terms. Scanned PDFs require OCR. No Zendesk/Freshdesk integration or outbound email sending is implemented.


## UI preview

This is a visual preview concept; the values shown are illustrative, not live data from the running application.

![SupportIQ dashboard UI preview](docs/ui-preview.svg)
