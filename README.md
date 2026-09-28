# 🚀 Missing Person Investigation Assistant

---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | ByteMind |
| **Track** | AI |
| **Team Lead** | Aakash Prajapati - aakash.20042001@gmail.com |
| **Members** | Haard Mehta, Harsh Panchal, Jiregna Tolera |

---

## 🎯 Problem Statement

Build a Bob-powered case coordination tool that takes family-provided data plus mock investigator tip logs and CCTV sighting descriptions. Bob correlates inputs, generates a prioritized list of investigative leads with recommended next actions, drafts a public appeal notice, and auto-fills a police missing person case file.

---

## 💡 Solution

> In 2–3 sentences: What did you build? How does it solve the problem above?

We built a **Bob-powered Missing Person Investigation Assistant** that ingests family-provided case data, mock investigator tips, and CCTV sighting descriptions, then runs a deterministic multi-factor correlation engine (scoring Name 30%, Location 25%, Time 20%, Clothing 15%, Physical 10%) to produce prioritized investigative leads. Bob coordinates the full workflow via a 6-tool MCP server, auto-drafting a broadcast-ready public appeal notice and auto-filling a formal Form 57 police case file (FIR dossier) — all within seconds of case intake.

---

## ✨ Key Features

- **Feature 1:** Bob-generated investigative explanations using the NVIDIA API
- **Feature 2:** Deterministic 0–100 lead scoring engine — fully auditable, court-admissible, zero hallucinated scores
- **Feature 3:** Auto-generated public appeal notice and Form 57 police case file (FIR) in seconds
- **Feature 4:** Native MCP server (6 tools over `stdio` + `sse`) with zero vendor lock-in
- **Feature 5:** Conflict-resilient noise isolation — contradictory tips are automatically flagged and separated from corroborated leads

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python, TypeScript, JavaScript |
| **Frameworks** | FastAPI, Uvicorn, Node.js (MCP server) |
| **AI / Integration** | IBM Bob, Model Context Protocol (MCP v2.2), NVIDIA API (`openai/gpt-oss-20b`) |
| **Databases** | JSON flat-file fixtures (no external DB required) |
| **Other** | UV package manager, python-dotenv, CORS middleware |

---

## 📁 Repository Structure

```
├── src/                  # All source code
├── docs/                 # Written documentation
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/                 # Demo artifacts
│   ├── screenshots/      # App screenshots
│   └── demo-video-link.txt  # Link to demo video
├── presentation/         # Slide deck
└── submission.yaml       # Structured submission metadata
```

---

## ⚡ How to Run

> **Copy these exact steps from your [`docs/setup-guide.md`](docs/setup-guide.md)**

```bash
# 1. Clone the repo
git clone https://github.com/aakashp2001/bob-ai-hackathon-ByteMinds.git
cd bob-ai-hackathon-ByteMinds

# 2. Create and activate the Python environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell

# 3. Install backend dependencies
python -m pip install -r requirements.txt

# 4. Install MCP dependencies
npm install

# 5. Configure environment (optional — defaults work out of the box)
cp src/.env.example .env
# Edit .env: set NVIDIA_API_KEY and NVIDIA_MODEL if using AI generation

# 6. Start the FastAPI backend
python -m uvicorn src.backend.app:app --host 127.0.0.1 --port 8000

# 7. In a second terminal — start the MCP server for Bob
npm start
```

---

## 🖥️ Demo

| Artifact | Link |
|---|---|
| 📹 Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| 🌐 Live Demo | [See demo/live-demo-url.txt](demo/live-demo-url.txt) |
| 🖼️ Screenshots | [See demo/screenshots/](demo/screenshots/) |
| 📊 Presentation | [See presentation/slides.pdf](presentation/) |

---

## ⚠️ Known Limitations

> Be honest — judges appreciate transparency over overclaiming.

- No authentication — the API is open by design for hackathon demo purposes; not production-ready.
- NVIDIA AI generation requires a valid `NVIDIA_API_KEY`; the deterministic backend and MCP tools work fully offline without it.
- Case data uses a single hardcoded fixture (`MP-2026-0042 — Aarav Shah`); multi-case support is not implemented.

---

## 🏅 What We're Most Proud Of

The **deterministic correlation engine** (`src/backend/services/correlation.py`) — it produces fully auditable, weighted 0–100 lead scores with automatic conflict isolation and graph-based sighting clustering, all without any LLM involvement. This means every score is reproducible, explainable, and court-admissible. Pair that with the **6-tool MCP server** that lets IBM Bob orchestrate the entire investigation workflow end-to-end, and you get a system that is both deeply technical and immediately useful in a real emergency.

---
