# Solution Overview

## What We Built

[Describe your solution in plain language. Avoid jargon — write as if explaining to a smart colleague unfamiliar with your tech stack.]

## How It Works

[Explain the core mechanism step by step. A numbered list or simple flow works well here.]

1. [Step 1: e.g., "User connects their GitHub repository via OAuth"]
2. The system sends verified case context and deterministic leads to the NVIDIA API for explanations and documents.
3. [Step 3: e.g., "An anomaly score is computed and displayed on the dashboard"]
4. [Step 4: e.g., "Alerts are sent to Slack when the score exceeds a threshold"]

## Architecture Diagram

> See [`architecture.md`](architecture.md) for the detailed diagram.

[Optionally include a simple ASCII or Mermaid diagram here for quick reference.]

```
[User] → [Frontend: React] → [API: FastAPI] → [NVIDIA API] → [Dashboard]
                                    ↓
                             [PostgreSQL DB]
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| NVIDIA API | Generates explanations and documents without changing deterministic backend scores |
| [Decision 2] | [Rationale 2] |
| [Decision 3] | [Rationale 3] |

## IBM Technologies Used

[Explain specifically HOW you used each IBM technology — not just that you used it.]

- **NVIDIA API:** Used through the OpenAI-compatible chat completions endpoint with `openai/gpt-oss-20b` for Bob-generated explanations, public appeals, and structured case files.
- **[IBM Tech 2]:** [How it was used]
