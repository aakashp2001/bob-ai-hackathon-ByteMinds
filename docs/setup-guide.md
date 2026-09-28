# Setup Guide

> **This file is read by the automated evaluation pipeline. Be precise and complete.**

## Prerequisites

Before you begin, ensure you have the following installed:

- [ ] Python 3.10+
- [ ] Node.js 18+
- [ ] IBM Bob with project-local MCP support

## Environment Variables

Copy `src/.env.example` to `.env` if you need to override defaults:

```bash
cp .env.example .env
```

| Variable | Description | Required |
|---|---|---|
| `BACKEND_BASE_URL` | FastAPI backend URL | No, defaults to `http://localhost:8000` |
| `BACKEND_TIMEOUT_MS` | MCP backend request timeout | No, defaults to `10000` |
| `DEFAULT_CASE_NUMBER` | Default fictional case | No, defaults to `MP-2026-0042` |

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/[your-org]/[your-repo].git
cd [your-repo]

# 2. Create and activate the Python environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# 3. Install backend dependencies
python -m pip install -r requirements.txt

# 4. Install MCP dependencies
npm install
```

## Running the Application

```bash
# Start the backend
python -m uvicorn src.backend.app:app --host 127.0.0.1 --port 8000

# In a second terminal, start the MCP server for Bob
npm start
```

The backend will be available at: `http://localhost:8000`.
Bob discovers the MCP server through `.bob/mcp.json` when the repository is
opened at the project root.

## Running Tests

```bash
npm test
```

## Quick Demo (Optional)

If you have a demo script or sample data to showcase the project quickly:

```bash
[e.g.: python demo/seed_demo_data.py]
[e.g.: open http://localhost:8000/demo]
```

## Troubleshooting

| Issue | Solution |
|---|---|
| [e.g., `ModuleNotFoundError`] | [e.g., Run `pip install -r requirements.txt` again] |
| [e.g., Database connection refused] | [e.g., Ensure PostgreSQL is running: `docker compose up db`] |
| [e.g., NVIDIA API 401 error] | Check `NVIDIA_API_KEY` in your local environment. |
